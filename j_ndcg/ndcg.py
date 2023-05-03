from typing import List

import numpy as np


def discounted_cumulative_gain(relevance: List[float], k: int, method: str = "standard") -> float:
    """Discounted Cumulative Gain

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    if method == "standard":
        relevance = np.array(relevance)
    else:
        relevance = (2 ** np.array(relevance)) - 1
    log_num = np.log2(np.arange(1, relevance.shape[0] + 1) + 1)
    score = np.sum((relevance / log_num)[:k])
    return score


def normalized_dcg(relevance: List[float], k: int, method: str = "standard") -> float:
    """Normalized Discounted Cumulative Gain.

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    dcg = discounted_cumulative_gain(relevance, k, method)
    sorted_rel = sorted(relevance, key=lambda x: -x)
    idel_dcg = discounted_cumulative_gain(sorted_rel, k, method)
    score = dcg / idel_dcg
    return score
