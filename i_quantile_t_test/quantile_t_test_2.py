from typing import List
from typing import Tuple

import numpy as np
from scipy.stats import ttest_ind


def quantile_ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
    quantile: float = 0.95,
    n_bootstraps: int = 1000,
) -> Tuple[float, bool]:
    """
    Bootstrapped t-test for quantiles of two samples.
    """

    control = np.array(control)
    shp_control = control.shape[0]
    experiment = np.array(experiment)
    shp_experiment = experiment.shape[0]

    res_control = []
    res_experiment = []

    for _ in range(n_bootstraps):

        ch_control = np.random.choice(control, size=shp_control, replace=True)
        ch_experiment = np.random.choice(experiment, size=shp_experiment, replace=True)

        qn_control = np.quantile(ch_control, quantile)
        qn_experiment = np.quantile(ch_experiment, quantile)

        res_control.append(qn_control)
        res_experiment.append(qn_experiment)

    _, p_value = ttest_ind(np.array(res_control), np.array(res_experiment))

    return p_value, bool(p_value < alpha)
