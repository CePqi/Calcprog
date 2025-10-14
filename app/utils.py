from pathlib import Path

def load_key(path: Path) -> bytes:
    with open(path, "rb") as f:
        return f.read()