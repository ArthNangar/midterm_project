import pytest
from app.operations import add, subtract, multiply, divide
from app.exceptions import OperationError


def test_basic_ops():
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(8, 4) == 2
    with pytest.raises(OperationError):
        divide(1, 0)
