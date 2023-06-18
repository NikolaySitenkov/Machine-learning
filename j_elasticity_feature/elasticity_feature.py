from scipy import stats
import pandas as pd
import numpy as np


def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    sku_unique = df.sku.unique()

    res_data = []

    for sku in sku_unique:
        qty = df[df["sku"] == sku].qty
        price = df[df["sku"] == sku].price

        result = stats.linregress(np.log(qty + 1), price)

        res_data.append([sku, result.rvalue ** 2])

    return pd.DataFrame(data=res_data, 
                        columns=["sku", "elasticity"])
