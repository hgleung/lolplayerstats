from collections import defaultdict
import pandas as pd
from teamkillmodel import *
from playerkillmodel import *
from winprob import *


current_patch = 13.16


data = pd.read_csv("2023_LoL_esports_match_data_from_OraclesElixir.csv")
data['kp'] = (data['kills'] + data['assists']) / data['teamkills']
data['kp'].fillna(0, inplace=True)
data['ks'] = data['kills'] / data['teamkills']
data['ks'].fillna(0, inplace=True)



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
    pk = playerkills(data)[0]
    tk = teamkills(data)[0]

    teams = data[data['position'] == 'team']
    g2_data = teams[teams['teamname'] == 'G2 Esports']
    mad_data = teams[teams['teamname'] == 'MAD Lions']
    agt = (g2_data['gamelength'].mean() + mad_data['gamelength'].mean()) / 2
    ckpm = (g2_data['ckpm'].mean() + mad_data['ckpm'].mean()) / 2


    tk_new = pd.DataFrame({'gamelength': [agt], 'ckpm': [ckpm], 'result': [0.2124]})
    predicted_tk = tk.predict(tk_new)[0]
    
    caps_data = data[data['playername'] == 'Carzzy']
    average_kp = caps_data['kp'].mean()
    average_ks = caps_data['ks'].mean()

    pk_new = pd.DataFrame({'kp': [average_kp], 'ks': [average_ks], 'teamkills': [predicted_tk]})
    predicted_pk = pk.predict(pk_new)[0]

    print(f"Predicted Kills: {predicted_pk}")
