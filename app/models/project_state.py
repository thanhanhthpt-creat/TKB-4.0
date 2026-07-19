from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProjectState:
    school_year: str = "2026-2027"
    assignment_file: Path | None = None
    template_file: Path | None = None
    subject_totals_file: Path | None = None
    output_file: Path | None = None
    constraints: dict[str, Any] = field(default_factory=dict)
    ai_api_key: str = ""
