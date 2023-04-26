import numpy as np

def ltv_error(y_true: np.array, y_pred: np.array) -> float:

    f_err = np.abs((y_true - y_pred) * y_pred)
    error = np.mean(f_err)

    return error
