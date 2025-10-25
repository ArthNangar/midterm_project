from __future__ import annotations
import sys
from typing import List
import pandas as pd
from colorama import init as colorama_init, Fore, Style  # ✅ For color-coded output

from .config import load_config
from .exceptions import OperationError, ValidationError
from .calculation import OperationFactory, Calculation
from .history import History
from .logger import configure_logger, LoggingObserver, AutoSaveObserver, Event
from .input_validators import validate_numbers


class Calculator:
    def __init__(self):
        self.cfg = load_config()
        self.logger = configure_logger(self.cfg)
        self.history = History(max_size=self.cfg.MAX_HISTORY_SIZE)
        # observers
        self._observers = [
            LoggingObserver(self.logger),
            AutoSaveObserver(self, self.cfg),
        ]

    # --- Observer notifications ---
    def _notify(self, calculation: Calculation) -> None:
        ev = Event(kind="calculation", payload={"calculation": calculation})
        for obs in self._observers:
            obs.update(ev)

    # --- Core operations ---
    def do(self, op: str, a: float, b: float) -> float:
        calc = OperationFactory.create(op, a, b)
        prec = self.cfg.PRECISION
        if prec is not None:
            calc.result = float(f"{calc.result:.{prec}f}")
        self.history.add(calc)
        self._notify(calc)
        return calc.result

    # --- Persistence ---
    def save_history(self) -> None:
        df = self.history.to_dataframe()
        df.to_csv(self.cfg.HISTORY_FILE, index=False, encoding=self.cfg.DEFAULT_ENCODING)

    def load_history(self) -> None:
        try:
            df = pd.read_csv(self.cfg.HISTORY_FILE, encoding=self.cfg.DEFAULT_ENCODING)
        except FileNotFoundError:
            raise ValidationError("History file does not exist")
        except Exception as e:
            raise ValidationError(f"Failed to read history: {e}")
        self.history = History.from_dataframe(df, max_size=self.cfg.MAX_HISTORY_SIZE)


class HelpRegistry:
    def __init__(self):
        self._lines: List[str] = []

    def register(self, line: str):
        self._lines.append(line)

    def text(self) -> str:
        ops = "\n".join(sorted(self._lines))
        return (
            "Commands:\n"
            f"{ops}\n"
            "history: show history\n"
            "clear: clear history\n"
            "undo: undo last operation\n"
            "redo: redo last undone operation\n"
            "exit: quit the program\n"
        )


HELP = HelpRegistry()
for op in (
    "add a b - addition",
    "subtract a b – subtraction",
    "multiply a b – multiplication",
    "divide a b – division",
    "power a b – a^b",
    "root a b – b-th root of a",
    "modulus a b – a % b",
    "int_divide a b – integer division",
    "percent a b – (a/b)*100",
    "abs_diff a b – |a-b|",
):
    HELP.register(op)


# --- REPL with Color-Coded Output using Colorama ---
def repl():  # pragma: no cover (interactive)
    colorama_init(autoreset=True)
    print(Fore.CYAN + "Calculator (color-coded). Type 'help' for commands." + Style.RESET_ALL)
    calc = Calculator()

    while True:
        try:
            line = input(Fore.YELLOW + "calc> " + Style.RESET_ALL).strip()
        except (EOFError, KeyboardInterrupt):
            print(Fore.CYAN + "\nbye!" + Style.RESET_ALL)
            break

        if not line:
            continue

        if line == "help":
            print(Fore.CYAN + HELP.text() + Style.RESET_ALL)
            continue

        if line == "exit":
            print(Fore.CYAN + "bye!" + Style.RESET_ALL)
            break

        # --- Undo / Redo / History / Clear Commands ---
        if line == "undo":
            if calc.history.undo():
                print(Fore.GREEN + "Last operation undone." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Nothing to undo." + Style.RESET_ALL)
            continue

        if line == "redo":
            if calc.history.redo():
                print(Fore.GREEN + "Last operation redone." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Nothing to redo." + Style.RESET_ALL)
            continue

        if line == "history":
            items = calc.history.items
            if not items:
                print(Fore.MAGENTA + "No history yet." + Style.RESET_ALL)
            else:
                print(Fore.CYAN + "History:" + Style.RESET_ALL)
                for c in items:
                    print(Fore.WHITE + f"{c.operation} {c.a} {c.b} = {c.result}" + Style.RESET_ALL)
            continue

        if line == "clear":
            calc.history.clear()
            print(Fore.MAGENTA + "History cleared." + Style.RESET_ALL)
            continue

        # --- Regular Operation Commands ---
        parts = line.split()
        if len(parts) != 3:
            print(Fore.MAGENTA + "usage: <op> <a> <b>" + Style.RESET_ALL)
            continue

        op, a_str, b_str = parts

        try:
            a = float(a_str)
            b = float(b_str)
            result = calc.do(op, a, b)
            print(Fore.GREEN + f"{op} {a} {b} = {result}" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "inputs must be numeric" + Style.RESET_ALL)
        except OperationError as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


if __name__ == "__main__":  # pragma: no cover
    repl()
