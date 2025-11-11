@echo off
REM Script to setup and run the Library Management System (Windows)

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Hệ Thống Quản Lý Thư Viện Trực Tuyến
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Tạo virtual environment...
    python -m venv venv
)

REM Activate venv
echo Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Cài đặt dependencies...
pip install -r requirements.txt > nul 2>&1

REM Copy .env if not exists
if not exist ".env" (
    echo Tạo file .env...
    copy .env.example .env
    echo ✓ File .env đã được tạo. Vui lòng chỉnh sửa cấu hình email.
)

REM Create database
echo Khởi tạo cơ sở dữ liệu...
python run.py init_db > nul 2>&1

REM Create sample data
echo Tạo dữ liệu mẫu...
python run.py create_sample_data > nul 2>&1

echo.
echo ========================================
echo ✓ Thiết lập hoàn tất!
echo ========================================
echo.
echo Để tạo tài khoản admin:
echo   python run.py create_admin
echo.
echo Để chạy ứng dụng:
echo   python run.py
echo.
echo Ứng dụng sẽ chạy tại: http://localhost:5000
echo.
pause
