from dataclasses import dataclass

@dataclass
class Memento:
    """Stores the calculator's state for undo/redo functionality."""
    state: list
