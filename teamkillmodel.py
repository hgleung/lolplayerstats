import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def teamkills(df: pd.DataFrame):
    # Split the data into features (X) and the target variable (y)
    data = df.loc[df["position"] == "team"]

    X = data[['gamelength', 'ckpm', 'result']]
    y = data['teamkills'] 

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a Random Forest Regression model
    model = LinearRegression()

    # Fit the model to the training data
    model.fit(X_train, y_train)

    return model, X_test, y_test

if __name__ == "__main__":
    data = pd.read_csv("2023_LoL_esports_match_data_from_OraclesElixir.csv")
    
    data = data.loc[data["league"].isin(["LPL", "LCK", "LCS", "LEC", "PCS"])]

    rf_model, X_test, y_test = teamkills(data)
    y_pred = rf_model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Now you can use the trained model to predict kills for new data
    # Example: Predict kills for a player with kp=10, ks=5, and teamkills=50
    ckpm = 32 / 1587 * 60
    print(ckpm)
    new_data = pd.DataFrame({'gamelength': [1587], 'ckpm': [ckpm], 'result': [1]})
    predicted_kills = rf_model.predict(new_data)
    print(f"Predicted Kills: {predicted_kills[0]}")