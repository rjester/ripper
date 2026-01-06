from pathlib import Path


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)
    return p


def longest_title(titles):
    # titles: iterable of dicts with 'Duration' or similar; placeholder
    if not titles:
        return None
    return titles[0]
