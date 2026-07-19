from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_constraints(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_constraints(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_ai_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"api_key": ""}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"api_key": ""}


def save_ai_config(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
