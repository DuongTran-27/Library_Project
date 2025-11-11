#!/bin/bash
# Script to setup and run the Library Management System

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Hệ Thống Quản Lý Thư Viện Trực Tuyến${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Tạo virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate venv
echo -e "${BLUE}Kích hoạt virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Cài đặt dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Tạo file .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ File .env đã được tạo. Vui lòng chỉnh sửa cấu hình email.${NC}"
fi

# Create database
echo -e "${BLUE}Khởi tạo cơ sở dữ liệu...${NC}"
python run.py init_db > /dev/null 2>&1

# Create sample data
echo -e "${BLUE}Tạo dữ liệu mẫu...${NC}"
python run.py create_sample_data > /dev/null 2>&1

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Thiết lập hoàn tất!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Để tạo tài khoản admin:${NC}"
echo -e "  ${GREEN}python run.py create_admin${NC}"
echo ""
echo -e "${BLUE}Để chạy ứng dụng:${NC}"
echo -e "  ${GREEN}python run.py${NC}"
echo ""
echo -e "${BLUE}Ứng dụng sẽ chạy tại: http://localhost:5000${NC}"
echo ""
