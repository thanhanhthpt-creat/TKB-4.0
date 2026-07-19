# Hướng dẫn đưa AI-TKB lên GitHub

## Cách 1: Dùng GitHub Desktop

1. Giải nén `AI-TKB-GitHub.zip`.
2. Mở GitHub Desktop.
3. Chọn **File → Add Local Repository**.
4. Chọn thư mục vừa giải nén.
5. Nếu được hỏi, chọn **Create a repository**.
6. Commit với nội dung `chore: khởi tạo dự án AI-TKB`.
7. Bấm **Publish repository**.
8. Chọn **Private repository** trong giai đoạn thử nghiệm.

## Cách 2: Dùng dòng lệnh

```bash
git init
git add .
git commit -m "chore: khởi tạo dự án AI-TKB"
git branch -M main
git remote add origin <URL-REPOSITORY>
git push -u origin main
```

## Trước khi công khai

- Không thêm PDF/Excel chứa dữ liệu thật.
- Không đưa tên giáo viên hoặc thông tin nội bộ vào Issue.
- Chạy `git status` để kiểm tra tệp chuẩn bị commit.
- Nên để repository ở chế độ Private khi bộ giải chưa hoàn chỉnh.
