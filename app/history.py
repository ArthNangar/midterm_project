from __future__ import annotations
from dataclasses import dataclass
from typing import List
import pandas as pd
from app.calculation import Calculation
from app.calculator_memento import Memento


@dataclass
class History:
    max_size: int

    def __post_init__(self):
        self._items: List[Calculation] = []
        self._undo_stack: List[Memento] = []
        self._redo_stack: List[Memento] = []

    # --- Internal state management ---
    def _snapshot(self) -> Memento:
        return Memento(state=list(self._items))

    def _restore(self, memento: Memento) -> None:
        self._items = list(memento.state)

    def add(self, calculation: Calculation) -> None:
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self._items.append(calculation)
        if len(self._items) > self.max_size:
            self._items.pop(0)

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        prev = self._undo_stack.pop()
        self._redo_stack.append(self._snapshot())
        self._restore(prev)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        nxt = self._redo_stack.pop()
        self._undo_stack.append(self._snapshot())
        self._restore(nxt)
        return True

    def clear(self) -> None:
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self._items.clear()

    # --- DataFrame serialization ---
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "operation": c.operation,
                    "a": c.a,
                    "b": c.b,
                    "result": c.result,
                    "timestamp": c.timestamp.isoformat(),
                }
                for c in self._items
            ]
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, max_size: int) -> "History":
        items: list[Calculation] = []
        for _, row in df.iterrows():
            try:
                ts = (
                    row["timestamp"]
                    if isinstance(row["timestamp"], str)
                    else row["timestamp"].isoformat()
                )
            except Exception:
                ts = None
            items.append(
                Calculation(
                    operation=str(row["operation"]),
                    a=float(row["a"]),
                    b=float(row["b"]),
                    result=float(row["result"]),
                    timestamp=pd.to_datetime(ts).to_pydatetime() if ts else None,
                )
            )

        h = cls(max_size=max_size)
        h._items = items
        return h

    # Expose read-only view
    @property
    def items(self) -> list[Calculation]:
        return list(self._items)
