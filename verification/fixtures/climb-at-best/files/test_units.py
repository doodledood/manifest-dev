import pytest

from units import to_metres


def test_converts() -> None:
    assert to_metres(2, "km") == 2000.0
    assert to_metres(10, "cm") == pytest.approx(0.1)


def test_unknown_unit_raises() -> None:
    with pytest.raises(KeyError):
        to_metres(1, "yd")
