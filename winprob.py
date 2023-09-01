import pandas as pd
from trueskill import TrueSkill, Rating, rate_1vs1


def predicted_win_probability(team_ratings, team1, team2, scaling_factor=1):
    delta_mu = team_ratings[team1].mu - team_ratings[team2].mu
    delta_sigma = ((team_ratings[team1].sigma ** 2) + (team_ratings[team2].sigma ** 2)) ** 0.5
    scaled_delta_mu = delta_mu * scaling_factor

    return TrueSkill().cdf(scaled_delta_mu / delta_sigma)


def find_scaling_factor(team_ratings, desired_prob, team1, team2):
    delta_mu = team_ratings[team1].mu - team_ratings[team2].mu
    delta_sigma = ((team_ratings[team1].sigma ** 2) + (team_ratings[team2].sigma ** 2)) ** 0.5
    
    scaling_factor = TrueSkill().ppf(desired_prob)  # Inverse of CDF
    scaling_factor = scaling_factor * delta_sigma / delta_mu
    return scaling_factor


def trueskill(df: pd.DataFrame) -> {str: Rating}:
    """
    This function implements the TrueSkill algorithm.

    Args:
        df: A pandas dataframe where "teamname" represents the winning team and "opp_teamname" represents the losing team.

    Returns:
        A dictionary of team names to TrueSkill ratings.
    """

    # Initialize the ratings for each team.
    ratings = {}

    for _, row in df.iterrows():
        team1 = row["teamname"]
        team2 = row["opp_teamname"]

        if team1 not in ratings:
            ratings[team1] = Rating()

        if team2 not in ratings:
            ratings[team2] = Rating()

        # Simulate a match where team1 wins and team2 loses
        team1_rating, team2_rating = rate_1vs1(ratings[team1], ratings[team2])

        # Update ratings dictionary with new ratings
        ratings[team1] = team1_rating
        ratings[team2] = team2_rating
    
    return ratings


def get_winning_teams(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a pandas DataFrame as input and returns a new DataFrame with one row of data per pair of rows
    where the "gameid" value is the same, and the "result" value is 1 for one row and 0 for the other row.
    The new DataFrame will have two columns: "teamname" and "opp_teamname".

    Args:
        df: The pandas DataFrame to be processed.

    Returns:
        A new pandas DataFrame with the winning team and corresponding opponent team per game.
    """

    winners = df[df["result"] == 1].copy()

    for index, row in winners.iterrows():
        gameid = row['gameid']
    
        # Filter df based on gameid and result condition
        filtered_df = df[(df['gameid'] == gameid) & (df['result'] == 0)]
        
        # Get the opp_teamname value from the filtered_df
        opp_teamname = filtered_df['teamname'].iloc[0] if not filtered_df.empty else None
        
        # Set the 'opp_teamname' value in winners DataFrame using .iloc indexer
        winners.loc[index, 'opp_teamname'] = opp_teamname

    return winners


def rank_league(df: pd.DataFrame, league: str) -> {str: Rating}:
    data = df.loc[df['league'] == league]
    data = data.loc[data["position"] == "team"]

    # print(trueskill(data))

    data = get_winning_teams(data)
    elo = trueskill(data)

    return elo


if __name__ == "__main__":
    data = pd.read_csv("2023_LoL_esports_match_data_from_OraclesElixir.csv")

    elo = rank_league(data, "LEC")
    
    ranking = sorted(elo.keys(), key=lambda team: elo[team].mu, reverse=True)

    team1 = "Team BDS"
    team2 = "Fnatic"

    scaling_factor = 0.37443501077648916  # Scaling factor to control the impact of skill difference

    win_probability = predicted_win_probability(elo, team1, team2, scaling_factor)

    print(f"The predicted win probability of {team1} beating {team2} is: {win_probability:.2%}")    
        

        
 