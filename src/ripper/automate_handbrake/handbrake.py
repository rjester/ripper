from pathlib import Path
from typing import List
import re
import os
from . import external
from .progress import RichProgressReporter
from datetime import datetime


_HB_PROGRESS_RE = re.compile(r'"Progress"\s*:\s*(\d+(?:\.\d+)?)')


def _parse_handbrake_line(line: str):
    m = _HB_PROGRESS_RE.search(line)
    if not m:
        return None
    progress = float(m.group(1))
    pct = round(progress * 100, 1)
    return {"percent": pct, "raw": line}


def list_presets(handbrake_path: str | None = None) -> str | None:
    hb = handbrake_path or os.environ.get("HANDBRAKE_CLI", "HandBrakeCLI")
    out_file = Path(os.getenv("TEMP", ".")) / f"handbrake_presets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    try:
        proc = external.run_with_logs([hb, '-z'], cwd=None, out_log=out_file, err_log=out_file)
        code, out_text, events = external.monitor_progress(proc, out_file, out_file, parser=None, poll_ms=500)
        return out_text
    except Exception:
        return None


def encode(input_file: str, output_file: str, preset_file: str | None = None, preset_name: str | None = None, container: str = 'mp4', handbrake_path: str | None = None, poll_ms: int = 500) -> dict:
    hb = handbrake_path or os.environ.get("HANDBRAKE_CLI", "HandBrakeCLI")
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    log_file = out_path.parent / f"handbrake_{out_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    out_log = out_path.parent / (out_path.stem + ".out")
    err_log = out_path.parent / (out_path.stem + ".err")

    # If a preset file is provided, attempt import first
    if preset_file and Path(preset_file).exists():
        try:
            import subprocess
            subprocess.run([hb, '--preset-import-file', str(preset_file), '-z'], check=False)
        except Exception:
            # proceed and let HandBrake fallback to built-in presets
            pass

    handbrake_args = []
    if preset_file and Path(preset_file).exists():
        handbrake_args += ["--preset-import-file", str(preset_file)]
    if preset_name:
        handbrake_args += ["-Z", str(preset_name)]
    handbrake_args += ["-i", str(input_file), "-o", str(output_file)]
    handbrake_args += ["-f", "av_mp4" if container == 'mp4' else 'av_mkv']
    handbrake_args += ["--json"]

    cmd = [hb] + handbrake_args

    proc = external.run_with_logs(cmd, cwd=None, out_log=out_log, err_log=err_log)
    # display live progress with rich
    try:
        reporter = RichProgressReporter(description="HandBrake Encode")
        with reporter:
            exit_code, merged, events = external.monitor_progress(proc, out_log, err_log, parser=_parse_handbrake_line, on_event=reporter.handle_event, poll_ms=poll_ms)
    except Exception:
        exit_code, merged, events = external.monitor_progress(proc, out_log, err_log, parser=_parse_handbrake_line, poll_ms=poll_ms)

    # write merged log
    try:
        with open(log_file, 'w', encoding='utf-8') as lf:
            lf.write(merged)
    except Exception:
        pass

    return {"Success": exit_code == 0, "ExitCode": exit_code, "Log": str(log_file), "Output": merged}


def encode_batch(input_files: List[str], output_dir: str, **kwargs) -> List[dict]:
    results = []
    for f in input_files:
        out = Path(output_dir) / (Path(f).stem + "." + (kwargs.get('container') or 'mp4'))
        results.append(encode(f, str(out), kwargs.get('preset_file'), kwargs.get('preset_name'), kwargs.get('container', 'mp4'), kwargs.get('handbrake_path')))
        if not results[-1]["Success"]:
            break
    return results
