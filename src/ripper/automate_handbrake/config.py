from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import shutil
import os
from datetime import datetime
import tomli
import tomli_w

LEGACY_PATH = Path(r"C:\SourceCode\AutomateHandbrake\src\config.json")


@dataclass
class Config:
    MakeMKVPath: str | None = None
    HandBrakePath: str | None = None
    PresetFile: str | None = None
    DefaultOutputPath: str = str(Path.cwd() / "output")
    DefaultTempPath: str | None = None


def get_user_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "automate_handbrake" / "config.toml"
    else:
        return Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "automate_handbrake" / "config.toml"


def load_config(path: Path | str | None = None) -> dict:
    target = Path(path) if path else get_user_config_path()
    if target.exists():
        try:
            with open(target, "rb") as f:
                data = tomli.load(f)
            return data
        except Exception:
            pass
    # If no user config, try migrating legacy
    if LEGACY_PATH.exists():
        migrate_legacy_config(LEGACY_PATH, target)
        try:
            with open(target, "rb") as f:
                return tomli.load(f)
        except Exception:
            pass
    # Fallback defaults
    cfg = Config()
    return asdict(cfg)


def save_config(cfg: dict | Config, path: Path | str | None = None) -> Path:
    target = Path(path) if path else get_user_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    data = cfg if isinstance(cfg, dict) else asdict(cfg)
    with open(target, "wb") as f:
        f.write(tomli_w.dumps(data).encode("utf-8"))
    return target


def migrate_legacy_config(legacy_path: Path | str, dest_path: Path | None = None) -> Path:
    legacy = Path(legacy_path)
    if not legacy.exists():
        # Nothing to migrate
        return get_user_config_path() if dest_path is None else Path(dest_path)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = legacy.parent / f"config.json.bak.{stamp}"
    shutil.copy2(legacy, backup)

    # load legacy JSON and convert to TOML structure
    with open(legacy, "r", encoding="utf-8") as f:
        j = json.load(f)

    # ensure some defaults exist
    cfg = {
        "MakeMKVPath": j.get("MakeMKVPath"),
        "HandBrakePath": j.get("HandBrakePath"),
        "PresetFile": j.get("PresetFile"),
        "DefaultOutputPath": j.get("DefaultOutputPath") or str(Path.cwd() / "output"),
        "DefaultTempPath": j.get("DefaultTempPath"),
    }

    dest = Path(dest_path) if dest_path else get_user_config_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(tomli_w.dumps(cfg).encode("utf-8"))

    return dest
