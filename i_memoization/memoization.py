from typing import Callable


def memoize(func: Callable) -> Callable:
    """Memoize function"""

    inp_lst = []
    out_lst = []
    def wrapper(*args, **kwargs):
        try:
            idx = inp_lst.index(tuple([args, kwargs]))
            return out_lst[idx]
        except ValueError:
            res = func(*args, **kwargs)
            inp_lst.append(tuple([args, kwargs]))
            out_lst.append(res)
        return res
    return wrapper
