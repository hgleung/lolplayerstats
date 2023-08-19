import csv
from collections import defaultdict
import math
from reference import *
from playerscraper import str_to_ref

current_patch = 13.14

def weighted_average_kills(reg: str, player: str) -> dict:
    """
    Reads all lines of data from the CSV file and returns a weighted average of kills based on patch and frequency of champ.

    Args:
        csv_file: The path to the CSV file.

    Returns:
        The weighted average of kills.
    """
    
    result = {}

    win_champ_freq = defaultdict(int)
    win_kills = defaultdict(int)
    win_total_freq = 0

    lose_freq = defaultdict(int)
    lose_kills = defaultdict(int)
    lose_total_freq = 0

    with open(f"players/{reg}/{player}.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        
        for row in reader:
            if row[3] == "Win":
                patch = float(row[2])
                champ = row[7]
                kills = int(row[8])
        
                win_champ_freq[champ] += (1 - (current_patch-patch))
                win_total_freq += (1 - (current_patch - patch))
                
                win_kills[champ] += ((1 - (current_patch-patch))) * kills
            else:
                patch = float(row[2])
                champ = row[7]
                kills = int(row[8])
        
                lose_freq[champ] += (1 - (current_patch-patch))
                lose_total_freq += (1 - (current_patch - patch))
                
                lose_kills[champ] += ((1 - (current_patch-patch))) * kills

        for champ in win_champ_freq:
            win_champ_freq[champ] /= win_total_freq
            win_kills[champ] /= win_total_freq

        for champ in lose_freq:
            lose_freq[champ] /= lose_total_freq
            lose_kills[champ] /= lose_total_freq

        win_weighted_kills = 0
        win_total_weight = 0

        lose_weighted_kills = 0
        lose_total_weight = 0

        for champ, weighted_kill in win_kills.items():
            win_weighted_kills += weighted_kill
            win_total_weight += win_champ_freq[champ]

        for champ, weighted_kill in lose_kills.items():
            lose_weighted_kills += weighted_kill
            lose_total_weight += lose_freq[champ]

    if win_total_weight == 0:
        result["Win"] = 0
    else:
        result["Win"] = win_weighted_kills / win_total_weight

    if lose_total_weight == 0:
        result["Lose"] = 0
    else:
        result["Lose"] = lose_weighted_kills / lose_total_weight

    return result

while __name__ == "__main__":
    region_name = input("Enter region name: ")
    region = str_to_ref(region_name.lower())

    teams = input("Enter team names: ").split()
    if teams[0] == "exit":
        exit()
    else:
        for team in teams:
            for player in region[1][team_conversion[team.lower()]]:
                try:
                    print(player.split('_')[0])
                    projections = weighted_average_kills(region[2], player)
                    print('3-0:', round(projections['Win']*3, 2))
                    print('2-1:', round(projections['Win']*2 + projections['Lose'], 2))
                    print('1-2:', round(projections['Win'] + projections['Lose']*2, 2))
                    print('0-3:', round(projections['Lose']*3, 2))
                except FileNotFoundError or KeyError:
                    print("Player not found")
    