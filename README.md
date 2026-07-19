# AI Thời Khóa Biểu Tiểu Học

Ứng dụng desktop hỗ trợ Ban giám hiệu nhập dữ liệu, quản lý ràng buộc và từng
bước tự động hóa việc lập thời khóa biểu tiểu học.

> Trạng thái hiện tại: **phiên bản 0.2.0 — giao diện và nền tảng dữ liệu**.
> Bộ giải OR-Tools hoàn chỉnh chưa được tích hợp; ứng dụng hiện chưa tự điền
> toàn bộ thời khóa biểu.

## Chức năng hiện có

- Giao diện Windows bằng PySide6.
- Chọn file phân công chuyên môn, khung Excel và tổng hợp số tiết.
- Kiểm tra đường dẫn, định dạng và sheet của khung Excel.
- Bật/tắt, lưu bộ ràng buộc của nhà trường.
- Nhật ký thao tác, trạng thái và điểm phương án.
- Tạo bản sao an toàn của khung TKB, không ghi đè tệp gốc.
- Điểm tích hợp sẵn cho Google OR-Tools.

## Ràng buộc đã khai báo

- HĐTN sáng thứ 2 tiết 1.
- HĐTN sáng thứ 6 tiết 4.
- Chiều thứ 6 nghỉ học.
- Một buổi không xếp hai tiết Toán.
- Lớp 1 tối đa ba tiết Tiếng Việt/ngày.
- Lớp 2 tối đa hai tiết Tiếng Việt/ngày.
- Lớp 3–5 có cặp tiết Tiếng Việt thứ 4 và 5 trong cùng ngày.
- Thầy Ba dạy trong hai buổi chiều.
- Cô My dạy trong một buổi chiều.
- Không trùng giáo viên, không trùng lớp, không đổi phân công.

## Cài đặt

Yêu cầu Python 3.11 hoặc 3.12.

```bash
git clone <URL-KHO-CUA-BAN>
cd AI-TKB
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
python main.py
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
python main.py
```

## Kiểm thử

```bash
ruff check .
pytest -q
```

## Đóng gói Windows

```bat
build_exe.bat
```

Kết quả được tạo trong thư mục `dist`.

## Đưa dự án lên GitHub

Tạo một repository trống trên GitHub, sau đó chạy:

```bash
git init
git add .
git commit -m "chore: khởi tạo dự án AI-TKB"
git branch -M main
git remote add origin <URL-REPOSITORY>
git push -u origin main
```

## Bảo mật dữ liệu

Không commit dữ liệu thật của nhà trường. `.gitignore` đã loại trừ PDF, Excel,
Word, thư mục dữ liệu, tệp xuất và nhật ký. Khi báo lỗi, chỉ dùng dữ liệu giả.

## Lộ trình

- [x] Giao diện và quản lý cấu hình.
- [x] Kiểm tra dữ liệu đầu vào.
- [x] Cấu trúc CI và kiểm thử.
- [ ] Chuẩn hóa phân công PDF thành bảng dữ liệu.
- [ ] Mô hình CP-SAT bằng OR-Tools.
- [ ] Xuất TKB theo lớp và giáo viên.
- [ ] Điều chỉnh cục bộ và khóa tiết.
- [ ] Đóng gói bộ cài Windows.

## Giấy phép

MIT — xem tệp `LICENSE`.
