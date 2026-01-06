from pathlib import Path
import subprocess
from typing import List
import time
from typing import Callable, Any


def run_with_logs(cmd: List[str], cwd: Path | None, out_log: Path, err_log: Path) -> subprocess.Popen:
    out_log.parent.mkdir(parents=True, exist_ok=True)
    # open files in binary mode for redirection
    outf = open(out_log, "wb")
    errf = open(err_log, "wb")
    proc = subprocess.Popen(cmd, cwd=str(cwd) if cwd else None, stdout=outf, stderr=errf)
    # return the process; caller is responsible for monitoring and closing files
    return proc


def monitor_progress(proc: subprocess.Popen, out_log: Path, err_log: Path, parser: Callable[[str], Any] | None = None, on_event: Callable[[Any], None] | None = None, poll_ms: int = 500):
    """Poll the given log files while `proc` runs, optionally parsing lines with `parser`.

    Returns a tuple (exit_code:int, merged_log:str, events:list).
    """
    last_count = 0
    events = []
    try:
        while proc.poll() is None:
            time.sleep(poll_ms / 1000.0)
            lines = []
            try:
                if out_log.exists():
                    lines.extend(out_log.read_text(encoding='utf-8', errors='ignore').splitlines())
                if err_log.exists():
                    lines.extend(err_log.read_text(encoding='utf-8', errors='ignore').splitlines())
            except Exception:
                # ignore transient read errors
                continue

            new_lines = lines[last_count:]
            last_count = len(lines)
            for line in new_lines:
                if parser:
                    try:
                        evt = parser(line)
                    except Exception:
                        evt = None
                else:
                    evt = None
                if evt is not None:
                    events.append(evt)
                    if on_event:
                        try:
                            on_event(evt)
                        except Exception:
                            # swallow exceptions from UI callbacks
                            pass
    finally:
        # Ensure the process has finished
        proc.wait()
        # Merge logs
        out_text = ""
        try:
            parts = []
            if out_log.exists():
                parts.append(out_log.read_text(encoding='utf-8', errors='ignore'))
            if err_log.exists():
                parts.append(err_log.read_text(encoding='utf-8', errors='ignore'))
            out_text = "\n".join(parts)
        except Exception:
            out_text = ""

    return proc.returncode, out_text, events
