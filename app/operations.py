from .exceptions import OperationError
import math


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise OperationError("division by zero is not allowed")
    return a / b

def power(a, b):
    try:
        return math.pow(a, b)
    except ValueError as e:
        raise OperationError(str(e))


def root(a, b):
    if b == 0:
        raise OperationError("0th root is undefined")
    if a < 0 and int(b) % 2 == 0:
        raise OperationError("even root of negative number is not real")
    return (abs(a)) ** (1.0 / float(b)) if a >= 0 else -((abs(a)) ** (1.0 / float(b)))


def modulus(a, b):
    if b == 0:
        raise OperationError("modulus by zero is not allowed")
    return a % b


def int_divide(a, b):
    if b == 0:
        raise OperationError("integer division by zero is not allowed")
    return int(a) // int(b)


def percent(a, b):
    if b == 0:
        raise OperationError("percentage with denominator zero is not allowed")
    return (a / b) * 100.0


def abs_diff(a, b):
    return abs(a - b)


OP_MAP = {
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