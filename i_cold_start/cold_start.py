import pandas as pd


def fillna_with_mean(
    df: pd.DataFrame, target: str, group: str
) -> pd.DataFrame:

    df = df.copy()
    df[target] = df.groupby(group)[target].apply(lambda x: x.fillna(x.mean()))
    df[target] = df[target].round()

    return df
