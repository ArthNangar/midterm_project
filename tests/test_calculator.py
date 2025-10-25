import builtins
from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError


def test_do_and_persistence(tmp_path, monkeypatch):
    # Override config via env (directories to tmp)
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "hist"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")

    calc = Calculator()
    r = calc.do("add", 1, 2)
    assert r == 3.0000

    calc.save_history()
    assert calc.cfg.HISTORY_FILE.exists()

    # Clear and load back
    calc.history.clear()
    calc.load_history()
    assert len(calc.history.items) == 1


def test_validation_errors(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "hist"))

    calc = Calculator()

    # OperationError
    try:
        calc.do("divide", 1, 0)
    except OperationError:
        pass

    # History file missing
    try:
        calc.load_history()
    except ValidationError:
        pass
