import subprocess
import os
import sys
import shutil
import csv
from pathlib import Path

MAKEMKV_CANDIDATES = ("makemkvcon64.exe", "makemkvcon.exe", "makemkvcon")


def _find_makemkv_exe() -> str:
    for name in MAKEMKV_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    return ""


def run_makemkv_command(args):
    """Run a MakeMKV command and return stdout.

    Raises SystemExit with a helpful diagnostic message on failure.
    """
    exe = _find_makemkv_exe()
    if not exe:
        sys.exit("❌ MakeMKV is not installed or not in PATH. Looked for: " + ", ".join(MAKEMKV_CANDIDATES))

    try:
        result = subprocess.run(
            [exe] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Provide full diagnostics: returncode, stdout, stderr
        msg_lines = [f"❌ MakeMKV error (exit code {getattr(e, 'returncode', '?')})"]
        if getattr(e, 'stdout', None):
            msg_lines.append("--- stdout ---")
            msg_lines.append(e.stdout)
        if getattr(e, 'stderr', None):
            msg_lines.append("--- stderr ---")
            msg_lines.append(e.stderr)
        sys.exit("\n".join(msg_lines))

def list_drives():
    """List available drives."""
    output = run_makemkv_command(["-r", "info", "--cache=1", "disc:9999"]) or ""
    drives = []
    if not output:
        return drives

    for line in output.splitlines():
        if not line.startswith("DRV:"):
            continue
        # use csv to respect quoted fields
        try:
            reader = csv.reader([line])
            parts = next(reader)
        except Exception:
            parts = line.split(",")

        # parts[0] is like 'DRV:<index>'
        try:
            drive_index = parts[0].split(":", 1)[1]
        except Exception:
            drive_index = ""

        # drive name is commonly at index 5, fall back to 4 or empty
        drive_name = ""
        if len(parts) > 5:
            drive_name = parts[5]
        elif len(parts) > 4:
            drive_name = parts[4]

        drive_name = drive_name.strip('"')
        drives.append((drive_index, drive_name))

    return drives

def list_titles(drive_index):
    """List titles on the disc."""
    output = run_makemkv_command(["-r", "info", f"dev:{drive_index}"])
    titles = []
    for line in output.splitlines():
        if line.startswith("TINFO"):
            parts = line.split(",")
            if parts[2] == "27":  # 27 = title name
                title_id = parts[0].split(":")[1]
                title_name = parts[3].strip('"')
                titles.append((title_id, title_name))
    return titles

def rip_titles(drive_index, output_dir, min_length=120):
    """Rip all titles from the drive."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"📀 Ripping from drive {drive_index} to {output_dir}...")
    run_makemkv_command([
        "mkv", f"dev:{drive_index}", output_dir,
        f"--minlength={min_length}"
    ])
    print("✅ Ripping complete.")

if __name__ == "__main__":
    print("🔍 Detecting drives...")
    drives = list_drives()
    if not drives:
        sys.exit("❌ No drives found.")

    print("\nAvailable Drives:")
    for idx, (drive_index, drive_name) in enumerate(drives):
        print(f"{idx}: {drive_name} (index {drive_index})")

    try:
        choice = int(input("\nSelect drive number: "))
        drive_index = drives[choice][0]
    except (ValueError, IndexError):
        sys.exit("❌ Invalid selection.")

    print("\n📄 Listing titles...")
    titles = list_titles(drive_index)
    for tid, tname in titles:
        print(f"Title {tid}: {tname}")

    output_dir = input("\nEnter output folder path: ").strip()
    if not output_dir:
        sys.exit("❌ Output folder cannot be empty.")

    rip_titles(drive_index, output_dir)
    print("All done!")