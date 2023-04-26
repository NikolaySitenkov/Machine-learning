import numpy as np


def smape(y_true: np.array, y_pred: np.array) -> float:
    """
    Рассчет sMAPE
    """

    # Считаем исходное количество элементов в массиве
    sz_arr = y_true.shape[0]

    # Копирование объектов, чтобы не изменялись входные
    y_true = y_true.copy()
    y_pred = y_pred.copy()

    # Если есть nan то заменяем их на 0
    y_true[np.isnan(y_true)] = 0
    y_pred[np.isnan(y_pred)] = 0

    # Нахождение суммы положительных чисел
    s_ar = np.abs(y_true) + np.abs(y_pred)
    # Если суммы каких-то пар равны 0, то следует исключить 0,
    # Так как это в любом случае приведет к необределенности 0/0
    mask_ar = s_ar != 0

    # Если в маске не окозалось объектов, то возвращаем 0
    if mask_ar.shape[0] == 0:
        return 0.0

    # Забираем значения согласно маске
    y_true = y_true[mask_ar]
    y_pred = y_pred[mask_ar]

    res = np.sum(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) / sz_arr

    return res
