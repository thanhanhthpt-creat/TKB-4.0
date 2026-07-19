@echo off
chcp 65001 > nul
python -m pip install -r requirements.txt
pyinstaller --noconfirm --clean --windowed ^
  --name "AI_Thoi_Khoa_Bieu" ^
  --add-data "config;config" ^
  main.py
echo.
echo File EXE nam trong thu muc dist\AI_Thoi_Khoa_Bieu
pause
