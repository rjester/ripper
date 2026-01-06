DEFAULT_PRESETS = {
    "Fast 1080p30": {"description": "Built-in HandBrake preset"},
}


def preset_exists(name: str, imported_text: str | None = None) -> bool:
    if name in DEFAULT_PRESETS:
        return True
    if imported_text and name in imported_text:
        return True
    return False
