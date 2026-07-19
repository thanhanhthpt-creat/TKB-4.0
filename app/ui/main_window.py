from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QUrl

from app.models.project_state import ProjectState
from app.scheduler.engine import SchedulerEngine
from app.services.config_service import load_constraints, save_constraints, load_ai_config, save_ai_config
from app.services.excel_service import ExcelService
from app.services.validation_service import validate_input_files


class MainWindow(QMainWindow):
    def __init__(self, project_root: Path):
        super().__init__()
        self.project_root = project_root
        self.state = ProjectState()
        self.engine = SchedulerEngine()
        self.constraint_boxes: dict[str, QCheckBox] = {}

        self.setWindowTitle("AI Thời Khóa Biểu Tiểu Học - Phiên bản 2.0")
        self.resize(1080, 760)

        self._build_menu()
        self._build_ui()
        self._load_default_constraints()
        self._load_ai_config()

    def _build_menu(self) -> None:
        menu_file = self.menuBar().addMenu("&Tệp")

        action_open_export = QAction("Mở thư mục xuất", self)
        action_open_export.triggered.connect(self._open_export_folder)
        menu_file.addAction(action_open_export)

        action_exit = QAction("Thoát", self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        menu_help = self.menuBar().addMenu("&Trợ giúp")
        action_about = QAction("Giới thiệu", self)
        action_about.triggered.connect(self._about)
        menu_help.addAction(action_about)

    def _build_ui(self) -> None:
        tabs = QTabWidget()
        tabs.addTab(self._build_input_tab(), "1. Dữ liệu")
        tabs.addTab(self._build_constraints_tab(), "2. Ràng buộc")
        tabs.addTab(self._build_results_tab(), "3. Kết quả")
        tabs.addTab(self._build_log_tab(), "4. Nhật ký")
        tabs.addTab(self._build_ai_tab(), "5. Cấu hình AI")
        self.setCentralWidget(tabs)

    def _build_input_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("AI XẾP THỜI KHÓA BIỂU TIỂU HỌC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 700; padding: 12px;")
        layout.addWidget(title)

        form_box = QGroupBox("Thông tin dự án")
        form = QFormLayout(form_box)

        self.school_year = QLineEdit("2026-2027")
        form.addRow("Năm học:", self.school_year)

        self.assignment_edit = self._add_file_row(
            form, "Phân công chuyên môn:", self._choose_assignment
        )
        self.template_edit = self._add_file_row(
            form, "Khung thời khóa biểu:", self._choose_template
        )
        self.subject_totals_edit = self._add_file_row(
            form, "Tổng hợp số tiết:", self._choose_subject_totals
        )
        layout.addWidget(form_box)

        buttons = QHBoxLayout()
        validate_button = QPushButton("KIỂM TRA DỮ LIỆU")
        validate_button.clicked.connect(self._validate)
        buttons.addWidget(validate_button)

        schedule_button = QPushButton("XẾP THỜI KHÓA BIỂU")
        schedule_button.setStyleSheet("font-weight: 700; padding: 10px;")
        schedule_button.clicked.connect(self._schedule)
        buttons.addWidget(schedule_button)
        layout.addLayout(buttons)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        layout.addStretch()
        return page

    def _add_file_row(self, form: QFormLayout, label: str, callback) -> QLineEdit:
        line = QLineEdit()
        line.setReadOnly(True)
        button = QPushButton("Chọn...")
        button.clicked.connect(callback)
        wrapper = QWidget()
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(line)
        row.addWidget(button)
        form.addRow(label, wrapper)
        return line

    def _build_constraints_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        box = QGroupBox("Ràng buộc của nhà trường")
        grid = QGridLayout(box)

        definitions = [
            ("lock_monday_hdt", "Sáng thứ 2 tiết 1: HĐTN"),
            ("lock_friday_hdt", "Sáng thứ 6 tiết 4: HĐTN"),
            ("friday_afternoon_off", "Chiều thứ 6 nghỉ học"),
            ("one_math_per_session", "Một buổi không xếp 2 tiết Toán"),
            ("grade1_vietnamese_max3", "Lớp 1 tối đa 3 tiết Tiếng Việt/ngày"),
            ("grade2_vietnamese_max2", "Lớp 2 tối đa 2 tiết Tiếng Việt/ngày"),
            ("grade345_vietnamese_pair", "Lớp 3-5: tiết TV thứ 4, 5 cùng ngày"),
            ("teacher_ba_two_afternoons", "Thầy Ba dạy trong 2 buổi chiều"),
            ("teacher_my_one_afternoon", "Cô My dạy trong 1 buổi chiều"),
            ("no_teacher_collision", "Không trùng lịch giáo viên"),
            ("no_class_collision", "Không trùng lịch lớp"),
            ("preserve_assignment", "Không thay đổi phân công chuyên môn"),
        ]

        for index, (key, label) in enumerate(definitions):
            checkbox = QCheckBox(label)
            self.constraint_boxes[key] = checkbox
            grid.addWidget(checkbox, index // 2, index % 2)

        layout.addWidget(box)

        save_button = QPushButton("LƯU CẤU HÌNH RÀNG BUỘC")
        save_button.clicked.connect(self._save_constraints)
        layout.addWidget(save_button)
        layout.addStretch()
        return page

    def _build_results_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.status_label = QLabel("Trạng thái: Chưa chạy")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(self.status_label)

        self.score_label = QLabel("Điểm phương án: --/100")
        layout.addWidget(self.score_label)

        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)

        row = QHBoxLayout()
        open_file_button = QPushButton("MỞ FILE KẾT QUẢ")
        open_file_button.clicked.connect(self._open_output_file)
        row.addWidget(open_file_button)

        open_folder_button = QPushButton("MỞ THƯ MỤC XUẤT")
        open_folder_button.clicked.connect(self._open_export_folder)
        row.addWidget(open_folder_button)
        layout.addLayout(row)

        self.warning_text = QPlainTextEdit()
        self.warning_text.setReadOnly(True)
        self.warning_text.setPlaceholderText("Cảnh báo và ghi chú sẽ hiển thị tại đây.")
        layout.addWidget(self.warning_text)
        return page

    def _build_log_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        return page

    def _build_ai_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        
        box = QGroupBox("Cấu hình API Key Gemini")
        form = QFormLayout(box)
        
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("Nhập Google Gemini API Key tại đây...")
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        form.addRow("API Key:", self.api_key_edit)
        
        link_label = QLabel("<a href='https://aistudio.google.com/app/apikey'>Lấy API Key tại Google AI Studio</a>")
        link_label.setOpenExternalLinks(True)
        form.addRow("", link_label)
        
        layout.addWidget(box)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("LƯU CẤU HÌNH AI")
        save_btn.clicked.connect(self._save_ai_config)
        btn_layout.addWidget(save_btn)
        
        test_btn = QPushButton("KIỂM TRA KẾT NỐI")
        test_btn.clicked.connect(self._test_ai_connection)
        btn_layout.addWidget(test_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        return page

    def _choose_assignment(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Chọn phân công chuyên môn", "", "PDF (*.pdf);;Tất cả (*.*)"
        )
        if path:
            self.state.assignment_file = Path(path)
            self.assignment_edit.setText(path)

    def _choose_template(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Chọn khung TKB", "", "Excel (*.xlsx *.xlsm)"
        )
        if path:
            self.state.template_file = Path(path)
            self.template_edit.setText(path)

    def _choose_subject_totals(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Chọn tổng hợp số tiết", "", "PDF (*.pdf);;Tất cả (*.*)"
        )
        if path:
            self.state.subject_totals_file = Path(path)
            self.subject_totals_edit.setText(path)

    def _load_default_constraints(self) -> None:
        path = self.project_root / "config" / "constraints.json"
        try:
            data = load_constraints(path)
        except Exception as exc:
            self._log(f"Không tải được cấu hình mặc định: {exc}")
            data = {}

        for key, checkbox in self.constraint_boxes.items():
            checkbox.setChecked(bool(data.get(key, True)))
        self.state.constraints = data

    def _load_ai_config(self) -> None:
        path = self.project_root / "config" / "ai_config.json"
        data = load_ai_config(path)
        self.state.ai_api_key = data.get("api_key", "")
        if hasattr(self, "api_key_edit"):
            self.api_key_edit.setText(self.state.ai_api_key)

    def _save_ai_config(self) -> None:
        key = self.api_key_edit.text().strip()
        self.state.ai_api_key = key
        path = self.project_root / "config" / "ai_config.json"
        save_ai_config(path, {"api_key": key})
        QMessageBox.information(self, "Thành công", "Đã lưu API Key Gemini thành công!")

    def _test_ai_connection(self) -> None:
        key = self.api_key_edit.text().strip()
        if not key:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập API Key trước khi kiểm tra.")
            return
            
        self._log("Bắt đầu kiểm tra kết nối AI...")
        try:
            from app.services.ai_service import AIService
            svc = AIService(api_key=key)
            result = svc.call_gemini("Chào bạn, hãy trả lời ngắn gọn: 'Kết nối thành công!'")
            self._log(f"[AI RESPONSE] {result}")
            QMessageBox.information(self, "Kết quả AI", f"Kết nối thành công!\nPhản hồi: {result}")
        except Exception as e:
            self._log(f"[AI ERROR] {e}")
            QMessageBox.critical(self, "Lỗi kết nối", f"Chi tiết lỗi:\n{e}")

    def _current_constraints(self) -> dict:
        return {
            key: checkbox.isChecked()
            for key, checkbox in self.constraint_boxes.items()
        }

    def _save_constraints(self) -> None:
        data = self._current_constraints()
        path = self.project_root / "config" / "constraints.json"
        save_constraints(path, data)
        self.state.constraints = data
        QMessageBox.information(self, "Đã lưu", f"Đã lưu cấu hình tại:\n{path}")

    def _validate(self) -> bool:
        self.progress.setValue(15)
        messages = validate_input_files(
            self.state.assignment_file,
            self.state.template_file,
            self.state.subject_totals_file,
        )

        has_error = False
        for item in messages:
            self._log(f"[{item.level}] {item.message}")
            if item.level == "ERROR":
                has_error = True

        if not has_error and self.state.template_file:
            try:
                sheets = ExcelService.inspect_workbook(self.state.template_file)
                self._log("Các sheet trong khung TKB: " + ", ".join(sheets))
            except Exception as exc:
                has_error = True
                self._log(f"[ERROR] Không đọc được file Excel: {exc}")

        self.progress.setValue(35 if not has_error else 0)
        if has_error:
            QMessageBox.warning(self, "Dữ liệu chưa hợp lệ", "Vui lòng xem Nhật ký.")
            return False

        QMessageBox.information(self, "Hợp lệ", "Dữ liệu đầu vào đã được kiểm tra.")
        return True

    def _schedule(self) -> None:
        if not self._validate():
            return

        self.progress.setValue(45)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = self.project_root / "exports" / f"TKB_XUAT_{timestamp}.xlsx"

        try:
            result = self.engine.solve(
                template_file=self.state.template_file,
                output_file=output,
                constraints=self._current_constraints(),
                log=self._log,
            )
        except Exception as exc:
            self.progress.setValue(0)
            QMessageBox.critical(self, "Lỗi lập lịch", str(exc))
            self._log(f"[ERROR] {exc}")
            return

        self.progress.setValue(100)
        self.state.output_file = result.output_file
        self.status_label.setText(f"Trạng thái: {result.status}")
        self.score_label.setText(f"Điểm phương án: {result.score}/100")
        self.output_edit.setText(str(result.output_file))
        self.warning_text.setPlainText("\n".join(f"- {x}" for x in result.warnings))
        QMessageBox.information(
            self,
            "Hoàn thành giai đoạn 2",
            f"Đã tạo tệp kết quả:\n{result.output_file}",
        )

    def _open_output_file(self) -> None:
        if self.state.output_file and self.state.output_file.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.state.output_file)))
        else:
            QMessageBox.warning(self, "Chưa có kết quả", "Chưa có file kết quả để mở.")

    def _open_export_folder(self) -> None:
        folder = self.project_root / "exports"
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.appendPlainText(f"{stamp}  {message}")

    def _about(self) -> None:
        QMessageBox.information(
            self,
            "Giới thiệu",
            "AI Thời Khóa Biểu Tiểu Học\nPhiên bản 2.0\n"
            "Giao diện quản lý dữ liệu, ràng buộc, kiểm tra và xuất Excel.",
        )
