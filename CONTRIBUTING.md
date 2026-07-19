# Đóng góp cho AI-TKB

## Quy trình

1. Tạo nhánh từ `main`.
2. Mỗi nhánh chỉ xử lý một chức năng hoặc một lỗi.
3. Viết hoặc cập nhật kiểm thử.
4. Chạy kiểm thử trước khi tạo Pull Request.
5. Không đưa dữ liệu thật của giáo viên, học sinh hoặc nhà trường lên kho mã.

## Quy ước nhánh

- `feature/...`: chức năng mới
- `fix/...`: sửa lỗi
- `docs/...`: tài liệu
- `test/...`: kiểm thử
- `refactor/...`: tái cấu trúc

## Quy ước commit

Ví dụ:

```text
feat: thêm kiểm tra trùng lịch giáo viên
fix: sửa lỗi đọc tên sheet Excel
docs: cập nhật hướng dẫn cài đặt Windows
```

## Dữ liệu bảo mật

Tất cả PDF, Excel, Word và tệp xuất của nhà trường phải để ngoài Git. Kho mã đã
cấu hình `.gitignore` để loại trừ các định dạng này.
