import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass
from .config import Config


LOGGER_NAME = "calculator"


def configure_logger(cfg: Config) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:  # already configured (avoid duplicate handlers in tests)
        return logger

    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(cfg.LOG_FILE, maxBytes=512_000, backupCount=3)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


# --- Observer pattern ---
@dataclass
class Event:
    kind: str
    payload: dict


class Observer:
    def update(self, event: Event) -> None:  # pragma: no cover (interface)
        pass


class LoggingObserver(Observer):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def update(self, event: Event) -> None:
        if event.kind == "calculation":
            c = event.payload["calculation"]
            self._logger.info(
                "op=%s a=%s b=%s result=%s", c.operation, c.a, c.b, c.result
            )


class AutoSaveObserver(Observer):
    def __init__(self, calculator, cfg: Config):
        self.calculator = calculator
        self.cfg = cfg

    def update(self, event: Event) -> None:
        if event.kind == "calculation" and self.cfg.AUTO_SAVE:
            try:
                self.calculator.save_history()
            except Exception as e:  # pragma: no cover (logged but not fatal)
                self.calculator.logger.warning("AutoSave failed: %s", e)
