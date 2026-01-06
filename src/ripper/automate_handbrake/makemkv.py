from pathlib import Path
import re
from typing import List
from . import external
import os
from datetime import datetime


_PRGV_RE = re.compile(r'^PRGV:(\d+),(\d+),(\d+)')


def _parse_prgv(line: str):
    m = _PRGV_RE.search(line)
    if not m:
        return None
    current = int(m.group(1))
    maximum = int(m.group(3))
    pct = round((current / maximum) * 100, 1) if maximum > 0 else 0.0
    return {"percent": pct, "raw": line}


def find_drives(makemkv_path: str | None = None) -> List[dict]:
    # Implemented as a best-effort: run makemkvcon -r --cache=1 info disc:9999 and parse DRV lines
    mk = makemkv_path or os.environ.get("MAKEMKVCON", "makemkvcon")
    out_file = Path(os.getenv("TEMP", ".")) / f"makemkv_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    try:
        proc = external.run_with_logs([mk, '-r', '--cache=1', 'info', 'disc:9999'], cwd=None, out_log=out_file, err_log=out_file)
        code, out_text, events = external.monitor_progress(proc, out_file, out_file, parser=None, poll_ms=500)
        drives = []
        for line in out_text.splitlines():
            if line.startswith('DRV:'):
                parts = line.split(',', 7)
                # Simple parse; match PS fields
                try:
                    index = int(parts[0].split(':')[1])
                    driveName = parts[5].strip('"') if len(parts) > 5 else ''
                    discName = parts[6].strip('"') if len(parts) > 6 else ''
                except Exception:
                    continue
                drives.append({"Index": index, "DriveName": driveName, "DiscName": discName})
        return drives
    except Exception:
        return []


def list_titles(drive_index: int = 0, makemkv_path: str | None = None) -> List[dict]:
    mk = makemkv_path or os.environ.get("MAKEMKVCON", "makemkvcon")
    out_file = Path(os.getenv("TEMP", ".")) / f"makemkv_titles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    try:
        proc = external.run_with_logs([mk, '-r', 'info', f'disc:{drive_index}'], cwd=None, out_log=out_file, err_log=out_file)
        code, out_text, events = external.monitor_progress(proc, out_file, out_file, parser=None, poll_ms=500)
        titles = {}
        for line in out_text.splitlines():
            m = re.match(r'^TINFO:(\d+),(\d+),\d?,"([^"]*)"', line)
            if m:
                tidx = int(m.group(1))
                attr = int(m.group(2))
                val = m.group(3)
                if tidx not in titles:
                    titles[tidx] = {"Index": tidx, "Name": '', "Duration": '', "Chapters": 0, "Size": '', "FileName": ''}
                if attr == 2:
                    titles[tidx]['Name'] = val
                elif attr == 8:
                    titles[tidx]['Chapters'] = val
                elif attr == 9:
                    titles[tidx]['Duration'] = val
                elif attr == 10:
                    titles[tidx]['Size'] = val
                elif attr == 27:
                    titles[tidx]['FileName'] = val
        return [titles[k] for k in sorted(titles.keys())]
    except Exception:
        return []


def rip_titles(drive_index: int, selection: str, out_dir: str, makemkv_path: str | None = None, poll_ms: int = 500) -> dict:
    if not out_dir:
        raise ValueError('OutDir is required')
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    log_file = out_dir_p / f"makemkv_rip_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    title_numbers = [s.strip() for s in str(selection).split(',') if s.strip()]
    overall_success = True
    mk = makemkv_path or os.environ.get("MAKEMKVCON", "makemkvcon")

    last_out = out_dir_p / "makemkv_last.out"
    last_err = out_dir_p / "makemkv_last.err"

    for title_num in title_numbers:
        args = [mk, '-r', 'mkv', f'disc:{drive_index}', title_num, str(out_dir_p)]
        proc = external.run_with_logs(args, cwd=None, out_log=last_out, err_log=last_err)
        # show progress using rich
        try:
            from .progress import RichProgressReporter
            reporter = RichProgressReporter(description=f"MakeMKV Rip title {title_num}")
            with reporter:
                exit_code, merged, events = external.monitor_progress(proc, last_out, last_err, parser=_parse_prgv, on_event=reporter.handle_event, poll_ms=poll_ms)
        except Exception:
            exit_code, merged, events = external.monitor_progress(proc, last_out, last_err, parser=_parse_prgv, poll_ms=poll_ms)

        # append merged logs to canonical log file
        try:
            with open(log_file, 'a', encoding='utf-8') as lf:
                lf.write(merged)
        except Exception:
            pass

        if exit_code != 0:
            overall_success = False
            break

    # collect mkv files
    mkv_files = [str(p) for p in out_dir_p.glob('*.mkv') if p.is_file()]

    return {"Success": overall_success, "ExitCode": 0, "Log": str(log_file), "Files": mkv_files, "RawOutput": merged}
