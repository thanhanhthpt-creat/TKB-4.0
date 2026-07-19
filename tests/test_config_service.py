from pathlib import Path

from app.services.config_service import load_constraints, save_constraints


def test_save_and_load_constraints(tmp_path: Path) -> None:
    path = tmp_path / "constraints.json"
    expected = {"no_teacher_collision": True, "friday_afternoon_off": True}
    save_constraints(path, expected)
    assert load_constraints(path) == expected
