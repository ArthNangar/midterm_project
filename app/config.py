from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class Config:
    LOG_DIR: Path
    HISTORY_DIR: Path
    LOG_FILE: Path
    HISTORY_FILE: Path
    MAX_HISTORY_SIZE: int
    AUTO_SAVE: bool
    PRECISION: int
    MAX_INPUT_VALUE: float
    DEFAULT_ENCODING: str


def _bool(val: str | None, default: bool) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> Config:
    load_dotenv(override=False)

    log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "./logs")).resolve()
    history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "./history")).resolve()

    log_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
    history_file = history_dir / os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")

    try:
        max_hist = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000"))
        precision = int(os.getenv("CALCULATOR_PRECISION", "6"))
        max_input = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e12"))
    except ValueError:
        # Fallback to safe defaults if env is malformed
        max_hist, precision, max_input = 1000, 6, 1e12

    auto_save = _bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"), True)
    encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

    # Clamp precision to [0, 12] to avoid weird formatting
    precision = max(0, min(12, precision))

    return Config(
        LOG_DIR=log_dir,
        HISTORY_DIR=history_dir,
        LOG_FILE=log_file,
        HISTORY_FILE=history_file,
        MAX_HISTORY_SIZE=max_hist,
        AUTO_SAVE=auto_save,
        PRECISION=precision,
        MAX_INPUT_VALUE=max_input,
        DEFAULT_ENCODING=encoding,
    )
