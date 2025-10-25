from app.history import History
from app.calculation import Calculation


def _calc(n):
    return Calculation("add", n, n, result=float(n * 2))


def test_push_undo_redo_clear():
    h = History(max_size=5)
    for i in range(3):
        h.add(_calc(i))  

    assert len(h.items) == 3

    assert h.undo() is True
    assert len(h.items) == 2
    assert h.redo() is True
    assert len(h.items) == 3

    h.clear()
    assert len(h.items) == 0


def test_max_size_evicts_oldest():
    h = History(max_size=2)
    h.add(_calc(1))
    h.add(_calc(2))
    h.add(_calc(3))
    assert len(h.items) == 2
    assert h.items[0].a == 2
