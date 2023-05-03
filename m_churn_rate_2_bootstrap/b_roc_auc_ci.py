from typing import Tuple

import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.metrics import roc_auc_score


def roc_auc_ci(
    classifier: ClassifierMixin,
    X: np.ndarray,
    y: np.ndarray,
    conf: float = 0.95,
    n_bootstraps: int = 10_000,
) -> Tuple[float, float]:
    """Returns confidence bounds of the ROC-AUC"""

    roc_lst = []

    if np.unique(y).shape[0] < 3:
        preds = classifier.predict_proba(X)[:, 1]
    else:
        preds = classifier.predict_proba(X)
    shp = y.shape[0]

    for _ in range(n_bootstraps):
        b_ind = np.random.choice(shp, size=shp, replace=True)
        try:
            roc_lst.append(roc_auc_score(y[b_ind], preds[b_ind], multi_class="ovr"))
        except Exception:
            pass

    roc_arr = np.array(roc_lst)
    left_ci = (1 - conf) / 2
    right_ci = 1 - (1 - conf) / 2
    lcb = np.quantile(roc_arr, left_ci)
    ucb = np.quantile(roc_arr, right_ci)

    return lcb, ucb
