import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from reference import *

def get_players():
    result = defaultdict(list)

    url = "https://lol.fandom.com/wiki/LCS/2023_Season/Summer_Season/Team_Rosters"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", {"class": "wikitable"})

    for num, table in enumerate(tables):
        rows = table.find_all("tr")
        for row in rows[1:]:
            name_element = row.find('a', class_='catlink-players pWAG pWAN to_hasTooltip')
            try:
                result[lcs_teams[num]].append(name_element.text)
            except AttributeError:
                pass
    return result

if __name__ == "__main__":
    print(get_players())