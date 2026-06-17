import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save(filename: str, data: list[dict]) -> None:
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, default=str)
        handle.write("\n")
