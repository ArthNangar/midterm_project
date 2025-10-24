import pytest

from app.calculation import OperationFactory
from app.exceptions import OperationError


def test_factory_known():
    for op in ["add", "subtract", "multiply", "divide"]:
        c = OperationFactory.create(op, 6, 3)
        assert c.operation == op
        assert isinstance(c.result, float)


def test_factory_unknown():
    with pytest.raises(OperationError):
        OperationFactory.create("nope", 1, 2)
