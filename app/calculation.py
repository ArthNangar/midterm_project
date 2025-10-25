from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
from .exceptions import OperationError
from .operations import (
    add,
    subtract,
    multiply,
    divide,
    power,
    root,
    modulus,
    int_divide,
    percent,
    abs_diff,
)


@dataclass
class Calculation:
    """Represents a single arithmetic calculation record."""
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


# Operation mapping (Factory Pattern)
OP_MAP: dict[str, Callable[[float, float], float]] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "root": root,
    "modulus": modulus,
    "int_divide": int_divide,
    "percent": percent,
    "abs_diff": abs_diff,
}


class OperationFactory:
    """Factory for creating Calculation objects based on operation name."""

    @staticmethod
    def create(operation: str, a: float, b: float) -> Calculation:
        func = OP_MAP.get(operation)
        if func is None:
            raise OperationError(f"unknown operation: {operation}")
        try:
            result = func(a, b)
        except Exception as e:
            # wrap lower-level math or logic errors into OperationError
            raise OperationError(str(e))
        return Calculation(operation=operation, a=a, b=b, result=float(result))
