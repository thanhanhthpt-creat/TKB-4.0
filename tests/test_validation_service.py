from pathlib import Path

from app.services.validation_service import validate_input_files


def test_missing_files_are_errors() -> None:
    messages = validate_input_files(None, None, None)
    assert sum(item.level == "ERROR" for item in messages) == 3


def test_valid_extensions(tmp_path: Path) -> None:
    assignment = tmp_path / "assignment.pdf"
    template = tmp_path / "template.xlsx"
    totals = tmp_path / "totals.pdf"
    for path in (assignment, template, totals):
        path.write_bytes(b"test")

    messages = validate_input_files(assignment, template, totals)
    assert not any(item.level == "ERROR" for item in messages)
