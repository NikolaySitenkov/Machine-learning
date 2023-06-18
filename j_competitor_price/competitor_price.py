import numpy as np
import pandas as pd


def get_res_row(inp_data):

    func_dict = {"avg": np.mean,
                 "med": np.median,
                 "min": np.min,
                 "max": np.max,
                 "rnk": lambda x: inp_data[inp_data["rank"] == np.min(x)].comp_price.values[0]}

    agg = inp_data["agg"].values[0]
    sku = inp_data["sku"].values[0]
    base_price = inp_data["base_price"].values[0]
    rank = inp_data["rank"].values
    comp_price = inp_data["comp_price"].values

    if agg == "rnk":
        if len(rank) == 1 and rank[0] == -1:
            if comp_price is not np.nan:
                calc_comp_price = comp_price[0]
        else:
            calc_comp_price = func_dict[agg](rank)
    else:
        calc_comp_price = func_dict[agg](comp_price)

    low_b, up_b = 0.8 * base_price, 1.2 * base_price
    if low_b <= calc_comp_price and up_b >= calc_comp_price:
        new_price = calc_comp_price
    else:
        new_price = base_price

    return [sku, agg, base_price, calc_comp_price, new_price]

def agg_comp_price(X: pd.DataFrame) -> pd.DataFrame:

    out_cols = ["sku", "agg", "base_price", "comp_price", "new_price"]
    out_lst = []

    for i in X.groupby(["sku", "agg", "base_price"], as_index=False):
        out_lst.append(get_res_row(i[1]))

    return pd.DataFrame(data=out_lst, columns=out_cols)
