from typing import List
import numpy as np


def get_sorted(labels: List[int], scores: List[float]) -> np.array:

    labels = np.array(labels)
    scores = np.array(scores)

    idx = np.argsort(scores)[::-1]

    return labels[idx]

def recall_at_k(labels: List[int], scores: List[float], k=5) -> float:

    labels = get_sorted(labels, scores)
        
    tp_v = labels[:k].sum()
    fn_v = labels[k:].sum()
    rc_v = tp_v / (tp_v + fn_v)

    return rc_v


def precision_at_k(labels: List[int], scores: List[float], k=5) -> float:

    labels = get_sorted(labels, scores)

    tp_v = labels[:k].sum()
    fp_v = labels[:k].shape[0] - labels[:k].sum()
    pr_v = tp_v / (tp_v + fp_v)

    return pr_v


def specificity_at_k(labels: List[int], scores: List[float], k=5) -> float:

    labels = get_sorted(labels, scores)

    tn_v = labels[k:].shape[0] - labels[k:].sum()
    fp_v = labels[:k].shape[0] - labels[:k].sum()
    sp_v = tn_v / (tn_v + fp_v)
    if tn_v + fp_v == 0:
        return 0

    return sp_v


def f1_at_k(labels: List[int], scores: List[float], k=5) -> float:

    pr_v = precision_at_k(labels, scores, k)
    rc_v = recall_at_k(labels, scores, k)
    if pr_v + rc_v == 0:
        return 0
    f1_v = 2 * pr_v * rc_v / (pr_v + rc_v)

    return f1_v
