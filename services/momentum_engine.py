import pandas as pd


def calculate_momentum(df):

    # 🔥 safety check
    if "Close" not in df.columns:
        raise ValueError(f"Missing Close column. Got: {df.columns}")

    df = df.copy().reset_index(drop=True)

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # 🔥 shorter lookbacks (important fix)
    df["return_1y"] = df["Close"] / df["Close"].shift(180) - 1
    df["return_6m"] = df["Close"] / df["Close"].shift(90) - 1
    df["return_3m"] = df["Close"] / df["Close"].shift(45) - 1

    df = df.dropna()

    # 🔥 momentum score
    df["momentum_score"] = (
        0.5 * df["return_1y"] +
        0.3 * df["return_6m"] +
        0.2 * df["return_3m"]
    )

    # 🔥 normalize (VERY IMPORTANT FOR RANKING)
    df["momentum_score"] = (
        df["momentum_score"] - df["momentum_score"].mean()
    ) / df["momentum_score"].std()

    return df.sort_values("momentum_score", ascending=False)
