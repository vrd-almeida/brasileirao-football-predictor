from sklearn.linear_model import LogisticRegression
import pandas as pd


def predict_winner(
    df: pd.DataFrame,
    home_as_home_avg_scored: float | None,
    home_as_home_avg_conceded: float | None,
    home_as_away_avg_scored: float | None,
    home_as_away_avg_conceded: float | None,
    team_home: str | None,
    team_away: str | None,
) -> str:

    # Build real training data
    X_train = []
    y_train = []

    for idx, row in df.iterrows():
        # Only train on past matches
        if pd.isna(row["Date"]):
            continue

        past_matches = df[df["Date"] < row["Date"]]

        home = row["Home"]
        away = row["Away"]

        if pd.isna(home) or pd.isna(away):
            continue

        home_home_matches = past_matches[past_matches["Home"] == home]
        away_away_matches = past_matches[past_matches["Away"] == away]

        if len(home_home_matches) >= 3 and len(away_away_matches) >= 3:
            features = [
                home_home_matches["HG"].mean(),
                home_home_matches["AG"].mean(),
                away_away_matches["AG"].mean(),
                away_away_matches["HG"].mean(),
            ]

            # Only append if label and all features are valid
            if (
                all(pd.notna(val) for val in features)
                and pd.notna(row["Res"])
                and row["Res"] in ["H", "D", "A"]
            ):
                X_train.append(features)
                y_train.append(row["Res"])

    if len(X_train) < 10:
        return "Not enough data to train model"

    model = LogisticRegression(multi_class="multinomial", max_iter=1000)
    model.fit(X_train, y_train)

    # Predict the current matchup
    X_pred = pd.DataFrame(
        [
            [
                home_as_home_avg_scored,
                home_as_home_avg_conceded,
                home_as_away_avg_scored,
                home_as_away_avg_conceded,
            ]
        ],
        columns=["home_gs", "home_gc", "away_gs", "away_gc"],
    )

    if X_pred.isna().any(axis=None):
        return "Missing input stats for prediction"

    pred = model.predict(X_pred)[0]

    if pred == "H":
        return team_home
    elif pred == "A":
        return team_away
    else:
        return "Draw"
