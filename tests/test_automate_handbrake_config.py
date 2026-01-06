import json
from pathlib import Path
import tomli


def test_migrate_legacy_config(tmp_path):
    legacy = tmp_path / "config.json"
    legacy_data = {
        "MakeMKVPath": "C:\\mk\\makemkvcon.exe",
        "HandBrakePath": "C:\\hb\\HandBrakeCLI.exe",
        "PresetFile": "C:\\presets\\presets.json",
        "DefaultOutputPath": str(tmp_path / "output"),
        "DefaultTempPath": str(tmp_path / "temp"),
    }
    legacy.write_text(json.dumps(legacy_data), encoding="utf-8")

    dest = tmp_path / "config.toml"

    from ripper.automate_handbrake.config import migrate_legacy_config

    res = migrate_legacy_config(legacy, dest)
    assert res.exists()

    # backup created
    backups = list(legacy.parent.glob("config.json.bak.*"))
    assert backups, "backup file not created"

    # dest content contains expected keys
    with open(dest, "rb") as f:
        data = tomli.load(f)
    for k in ("MakeMKVPath", "HandBrakePath", "PresetFile", "DefaultOutputPath", "DefaultTempPath"):
        assert k in data
