from collections import defaultdict
import pandas as pd

import csv
import os
import math
import statistics
import requests

import matplotlib.pyplot as plt


current_patch = 13.16

data = pd.read_csv("2023_LoL_esports_match_data_from_OraclesElixir.csv")
# data['kp'] = (data['kills'] + data['assists']) / data['teamkills']
# data['ks'] = data['kills'] / data['teamkills']


def avg_kills(stats: pd.DataFrame) -> dict:
    """
    Weighted Average of kills based on champion pick and patch recency
    """
    result = {}

    win_champ_freq = defaultdict(int)
    win_kills = defaultdict(int)
    win_total_freq = 0

    lose_freq = defaultdict(int)
    lose_kills = defaultdict(int)
    lose_total_freq = 0

    for _, row in stats.iterrows():
        patch = row['patch']
        champ = row['champion']
        kills = row['kills']
        
        if row['result']:
            win_champ_freq[champ] += (1 - 5*(current_patch-patch))
            win_total_freq += (1 - 5*(current_patch - patch))
            
            win_kills[champ] += ((1 - 5*(current_patch-patch))) * kills
        else:
            lose_freq[champ] += (1 - 5*(current_patch-patch))
            lose_total_freq += (1 - 5*(current_patch - patch))
            
            lose_kills[champ] += ((1 - 5*(current_patch-patch))) * kills

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
        
if __name__ == "__main__":
    # while True:
    #     player = input("Enter player name\n")
    #     player_data = data[data['playername'] == player]
        
    #     avg = avg_kills(player_data)

    #     print('3-0: {}'.format(round(avg["Win"]*3, 2)))
    #     print('2-1: {}'.format(round(avg["Win"]*2 + avg["Lose"], 2)))
    #     print('1-2: {}'.format(round(avg["Win"] + avg["Lose"]*2, 2)))
    #     print('0-3: {}'.format(round(avg["Lose"]*3, 2)))

    # filtered = data.loc[data["position"].isin(['top', 'jng', 'mid', 'bot'])]

    corr = data.corr(numeric_only=True)["teamkills"]
    print(corr["gamelength"])

    # plt.scatter(data['teamkills'], data['kills'])
    # plt.xlabel('Feature Values')
    # plt.ylabel('Kills')
    # plt.legend()
    # plt.show()