import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def playerkills(df: pd.DataFrame):
    # Split the data into features (X) and the target variable (y)
    X = df[['kp', 'ks', 'teamkills']].fillna(0)
    y = df['kills'] 

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a Random Forest Regression model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    return model, X_test, y_test

if __name__ == "__main__":
    data = pd.read_csv("2023_LoL_esports_match_data_from_OraclesElixir.csv")
    nonsup = data.loc[data["position"].isin(['top', 'jng', 'mid', 'bot'])].copy()
    nonsup['kp'] = (nonsup['kills'] + nonsup['assists']) / nonsup['teamkills']
    nonsup['ks'] = nonsup['kills'] / nonsup['teamkills']

    rf_model, X_test, y_test = playerkills(nonsup)
    y_pred = rf_model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Now you can use the trained model to predict kills for new data
    # Example: Predict kills for a player with kp=10, ks=5, and teamkills=50
    new_data = pd.DataFrame({'kp': [0.702], 'ks': [0.274], 'teamkills': [24]})
    predicted_kills = rf_model.predict(new_data)
    print(f"Predicted Kills: {predicted_kills[0]}")