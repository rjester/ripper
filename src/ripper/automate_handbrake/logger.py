from pathlib import Path
from datetime import datetime
import sys

_LOG_PATH: Path | None = None


def initialize_logger(log_dir: str | None = None) -> Path:
    global _LOG_PATH
    base = Path(log_dir) if log_dir else Path.cwd() / "logs"
    base.mkdir(parents=True, exist_ok=True)
    file = base / f"automate_handbrake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file.touch(exist_ok=True)
    _LOG_PATH = file
    return file


def get_log_path() -> Path | None:
    return _LOG_PATH


def write_log(message: str, level: str = "INFO") -> None:
    global _LOG_PATH
    if _LOG_PATH is None:
        initialize_logger()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{time}] [{level}] {message}\n"
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        # best-effort: write to stderr
        sys.stderr.write(line)
