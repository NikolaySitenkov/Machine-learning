import metrics


def test_profit() -> None:
    """Check profit function"""
    assert metrics.profit([1, 2, 3], [1, 1, 1]) == 3


def test_margin() -> None:
    """Check margin function"""
    assert metrics.margin([1, 2, 3], [1, 1, 1]) == 0.5


def test_markup() -> None:
    """Check markup function"""
    assert metrics.markup([1, 2, 3], [1, 1, 1]) == 1
