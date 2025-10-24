from __future__ import annotations
from .calculation import OperationFactory
from .exceptions import OperationError

# Define the help string clearly, using triple quotes for multi-line text
HELP = (
    "Commands:\n"
    "add a b | subtract a b | multiply a b | divide a b\n"
    "help | exit\n"
)

def repl():  # pragma: no cover (interactive)
    print("Calculator (basic). Type 'help' for commands.")
    
    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")
            break
            
        if not line:
            continue
            
        if line == "help":
            print(HELP)
            continue
            
        if line == "exit":
            print("bye!")
            break
            
        parts = line.split()
        
        if len(parts) != 3:
            print("usage: <op> <a> <b>")
            continue
            
        op, a_str, b_str = parts
        
        try:
            
            a = float(a_str)
            b = float(b_str)
            
            calc = OperationFactory.create(op, a, b)
            
            print(f"{op} {a} {b} = {calc.result}")
            
        except ValueError:
            print("inputs must be numeric")
        except OperationError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":  # pragma: no cover
    repl()