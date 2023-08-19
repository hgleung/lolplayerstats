import requests
from bs4 import BeautifulSoup
import re
from reference import *
from collections import defaultdict
import csv
from tqdm import tqdm

pattern = r"title=\"(.*?)\""

def str_to_ref(region: str):
    if region == "pcs":
        return (pcs_teams, pcs_players, "PCS")
    if region == "lck":
        return (lck_teams, lck_players, "LCK")
    if region == "lec":
        return (lec_teams, lec_players, "LEC")
    if region == "lcs":
        return (lcs_teams, lcs_players, "LCS")


def get_match_history(player: str) -> list:
    url = "https://lol.fandom.com/wiki/" + player + "/Match_History"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")

    result = []
    for row in rows[4:54]:
        cells = row.find_all("td")
        if not str(cells[2].text).startswith("13"):
            break
        data = []
        
        for i in range(5):
            data.append(cells[i].text)
        
        data.append((re.search(pattern, str(cells[6]))).group(1))
        
        data.append(cells[7].text)

        data.append((re.search(pattern, str(cells[8]))).group(1))

        for i in range(10, 13):
            data.append(cells[i].text)

        result.append(data)
    
    return result
        
def get_player_roster(team: str) -> list:
    url = "https://lol.fandom.com/wiki/" + team
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")

    player_roster = []
    for row in rows[1:]:
        cells = row.find_all("td")
        name = re.search(pattern, str(cells[2])).group(1).replace(" ", "_")
        position = cells[4].text
        player_roster.append((name, position))

    return player_roster

def convert_to_csv(player_name, region):
    """Converts a list of lists into a .csv file.

    Args:
        player_roster: A list of lists containing the player data.
        file_name: The name of the .csv file.
    """

    with open(f"players/{region}/{player_name}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["Date", "Tournament", "Patch", "Result", "Side", "Opponent", "Game Duration", "Champ", "Kills", "Deaths", "Assists"])
        match_history = get_match_history(player_name)
        for game in match_history:
            writer.writerow(game)

if __name__ == "__main__":
    region_name = input("Enter region name: ")
    region = str_to_ref(region_name.lower())
    for team in tqdm(region[0]):
        for player in region[1][team]:
            try:
                convert_to_csv(player, region[2])
            except AttributeError:
                pass