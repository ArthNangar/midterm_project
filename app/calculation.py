from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
from .exceptions import OperationError

OP_MAP = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: (_ for _ in ()).throw(OperationError("division by zero is not allowed")) if b == 0 else a / b,
}

@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class OperationFactory:
    @staticmethod
    def create(operation: str, a: float, b: float) -> Calculation:
        func: Callable[[float, float], float] | None = OP_MAP.get(operation)
        if func is None:
            raise OperationError(f"unknown operation: {operation}")
        result = func(a, b)
        return Calculation(operation=operation, a=a, b=b, result=float(result))