from typing import List, Tuple
from scipy import stats
import numpy as np


def ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
) -> Tuple[float, bool]:
    """Two-sample t-test for the means of two independent samples"""
    _, p_value = stats.ttest_ind(np.array(control), np.array(experiment))

    return p_value, bool(p_value < alpha)
