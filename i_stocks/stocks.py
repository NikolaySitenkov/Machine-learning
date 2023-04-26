import pandas as pd


def limit_gmv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Перерасчет gmv
    """
    df = df.copy()

    df["gmv"] = (df["gmv"] / df["price"]).astype(int)

    df["gmv"] = df["price"] * df[["gmv", "stock"]].min(axis=1)

    return df
