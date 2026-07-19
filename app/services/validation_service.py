from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationMessage:
    level: str
    message: str


def validate_input_files(
    assignment_file: Path | None,
    template_file: Path | None,
    subject_totals_file: Path | None,
) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []

    required = [
        ("Phân công chuyên môn", assignment_file),
        ("Khung thời khóa biểu", template_file),
        ("Tổng hợp số tiết", subject_totals_file),
    ]

    for label, path in required:
        if path is None:
            messages.append(ValidationMessage("ERROR", f"Chưa chọn: {label}."))
        elif not path.exists():
            messages.append(ValidationMessage("ERROR", f"Không tìm thấy: {path}"))
        else:
            messages.append(ValidationMessage("OK", f"Đã nhận: {label}."))

    if assignment_file and assignment_file.suffix.lower() != ".pdf":
        messages.append(
            ValidationMessage(
                "WARNING",
                "Phân công chuyên môn hiện được thiết kế ưu tiên cho tệp PDF.",
            )
        )

    if subject_totals_file and subject_totals_file.suffix.lower() != ".pdf":
        messages.append(
            ValidationMessage(
                "WARNING",
                "Tổng hợp số tiết hiện được thiết kế ưu tiên cho tệp PDF.",
            )
        )

    if template_file and template_file.suffix.lower() not in {".xlsx", ".xlsm"}:
        messages.append(
            ValidationMessage("ERROR", "Khung TKB phải là tệp Excel .xlsx/.xlsm.")
        )

    return messages
