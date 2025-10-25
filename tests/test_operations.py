import pytest
from app.operations import add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
from app.exceptions import OperationError


def test_basic_ops():
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(8, 4) == 2
    with pytest.raises(OperationError):
        divide(1, 0)

def test_power_root_mod_intdiv_percent_absdiff():
    assert power(2, 3) == 8
    assert pytest.approx(root(27, 3), rel=1e-9) == 3

    with pytest.raises(OperationError):
        root(-8, 2)

    assert modulus(10, 3) == 1
    with pytest.raises(OperationError):
        modulus(1, 0)

    assert int_divide(7, 2) == 3
    with pytest.raises(OperationError):
        int_divide(1, 0)

    assert percent(50, 200) == 25
    with pytest.raises(OperationError):
        percent(1, 0)

    assert abs_diff(5, 9) == 4