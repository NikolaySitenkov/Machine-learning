import numpy as np

def turnover_error(y_true: np.array, y_pred: np.array) -> float:

    f_err = (y_true - y_pred) / y_pred
    error = np.mean(f_err ** 2)

    return error
