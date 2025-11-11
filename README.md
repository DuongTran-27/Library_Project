# Hệ Thống Quản Lý Thư Viện Trực Tuyến

Một ứng dụng web hiện đại để quản lý mượn/trả sách, tìm kiếm sách và quản lý độc giả với giao diện thân thiện và dễ sử dụng.

## ✨ Tính Năng Chính

### Quản Lý Sách
- ✅ Thêm, sửa, xóa sách
- ✅ Tìm kiếm theo tên, tác giả, thể loại
- ✅ Quản lý số lượng sách và bản có sẵn
- ✅ Phân loại sách theo thể loại
- ✅ Hiển thị chi tiết sách

### Quản Lý Mượn/Trả
- ✅ Mượn sách với hạn trả tự động (14 ngày)
- ✅ Trả sách với tính phạt trễ hạn (5,000 VND/ngày)
- ✅ Gia hạn sách (1 lần duy nhất)
- ✅ Lịch sử mượn chi tiết
- ✅ Theo dõi sách quá hạn

### Hệ Thống Đặt Trước
- ✅ Đặt trước sách đang được mượn hết
- ✅ Danh sách chờ tự động
- ✅ Thông báo email khi sách sẵn có

### Xác Thực & Phân Quyền
- ✅ Đăng ký/Đăng nhập người dùng
- ✅ Phân quyền Admin và User thường
- ✅ Khóa tài khoản người dùng
- ✅ Quản lý thông tin cá nhân

### Dashboard Thống Kê
- ✅ Tổng sách, sách sẵn có, sách đang mượn
- ✅ Sách mượn nhiều nhất
- ✅ Độc giả tích cực
- ✅ Sách quá hạn
- ✅ Xuất báo cáo PDF

### RESTful API
- ✅ Lấy danh sách sách
- ✅ Tìm kiếm sách
- ✅ Mượn/Trả sách qua API
- ✅ Thống kê thư viện
- ✅ Hỗ trợ phân trang

### Giao Diện
- ✅ Responsive design (Mobile/Tablet/Desktop)
- ✅ Bootstrap 5 CSS Framework
- ✅ Giao diện hiện đại & thân thiện
- ✅ Dark mode support

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM để quản lý database
- **Flask-Login** - Xác thực người dùng
- **Flask-Mail** - Gửi email
- **Flask-RESTful** - Xây dựng RESTful API

### Frontend
- **Bootstrap 5** - CSS Framework
- **Jinja2** - Template engine
- **Font Awesome** - Icons

### Database
- **SQLite** - Mặc định (phát triển)
- **PostgreSQL** - Tùy chọn (production)

### Công Cụ Khác
- **ReportLab** - Tạo PDF báo cáo
- **python-dotenv** - Quản lý biến môi trường

## 📋 Yêu Cầu Hệ Thống

- Python 3.8+
- pip (Python package manager)
- PostgreSQL (tùy chọn)

## 🚀 Hướng Dẫn Cài Đặt

### 1. Clone Repository
```bash
cd d:\library_project
```

### 2. Tạo Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu Hình Biến Môi Trường
```bash
# Copy file .env.example thành .env
cp .env.example .env

# Chỉnh sửa .env với cấu hình của bạn
```

### 5. Khởi Tạo Database
```bash
# Tạo cơ sở dữ liệu
python run.py

# Hoặc chạy lệnh CLI
flask db init
flask db migrate
flask db upgrade

# Tạo dữ liệu mẫu
python run.py create_sample_data
```

### 6. Tạo Tài Khoản Admin
```bash
python run.py create_admin
```

### 7. Chạy Ứng Dụng
```bash
python run.py
```

Ứng dụng sẽ chạy tại: **http://localhost:5000**

## 📚 Cấu Trúc Thư Mục

```
library_project/
├── app.py                 # Flask application factory
├── config.py              # Cấu hình ứng dụng
├── models.py              # Database models
├── run.py                 # Entry point
├── requirements.txt       # Dependencies
├── .env.example           # Biến môi trường mẫu
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── auth/              # Authentication pages
│   ├── book/              # Book pages
│   ├── borrow/            # Borrow pages
│   ├── user/              # User pages
│   └── admin/             # Admin pages
├── static/                # Static files (CSS, JS, images)
├── routes/                # Route blueprints
│   ├── auth_routes.py     # Xác thực
│   ├── book_routes.py     # Quản lý sách
│   ├── borrow_routes.py   # Mượn/Trả
│   ├── user_routes.py     # Hồ sơ người dùng
│   ├── admin_routes.py    # Quản trị viên
│   └── api_routes.py      # RESTful API
└── services/              # Services
    ├── email_service.py   # Email notifications
    └── pdf_service.py     # PDF generation
```

## 📖 Hướng Dẫn Sử Dụng

### Người Dùng Thường
1. Đăng ký tài khoản mới
2. Tìm kiếm và xem chi tiết sách
3. Mượn sách (tối đa 5 sách/lần)
4. Theo dõi hạn trả và tiền phạt
5. Gia hạn sách (1 lần)
6. Trả sách
7. Đặt trước sách nếu hết

### Quản Trị Viên
1. Đăng nhập bằng tài khoản admin
2. Dashboard: Xem thống kê thư viện
3. Quản lý sách: Thêm, sửa, xóa sách
4. Quản lý độc giả: Khóa/kích hoạt tài khoản
5. Quản lý mượn: Xem lịch sử, tính phạt
6. Quản lý thể loại: Thêm, sửa, xóa thể loại
7. Báo cáo: Xuất báo cáo PDF

## 🔌 RESTful API Endpoints

### Books
- `GET /api/books` - Danh sách sách
- `GET /api/books/<id>` - Chi tiết sách
- `GET /api/categories` - Danh sách thể loại

### User
- `GET /api/my-borrows` - Sách đang mượn
- `POST /api/borrow/<book_id>` - Mượn sách
- `POST /api/return/<record_id>` - Trả sách

### Statistics
- `GET /api/search?q=<query>` - Tìm kiếm
- `GET /api/stats` - Thống kê thư viện

## 📧 Cấu Hình Email (Gmail)

1. Bật 2-Step Verification trên tài khoản Google
2. Tạo App Password: https://myaccount.google.com/apppasswords
3. Copy App Password vào `.env`:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🔐 Bảo Mật

- Mật khẩu được mã hóa với Werkzeug
- CSRF protection
- SQL Injection prevention với SQLAlchemy ORM
- XSS protection với Jinja2 template escaping

## 📝 Phí Trễ Hạn

- **5,000 VND/ngày** cho mỗi ngày trễ
- Tính từ ngày hạn trả cho đến ngày trả thực tế
- Thông báo email 3 ngày trước khi hạn trả

## 🚦 Giới Hạn Mượn

- **Tối đa 5 sách** đang mượn
- **Hạn mượn: 14 ngày**
- **Gia hạn: 1 lần** (thêm 14 ngày)

## 🐛 Troubleshooting

### Database Error
```bash
# Xóa database cũ
rm library.db

# Khởi tạo lại
python run.py
```

### Email không gửi được
- Kiểm tra cấu hình `.env`
- Kiểm tra kết nối internet
- Kiểm tra App Password Google

### Import Error
```bash
# Cài lại dependencies
pip install -r requirements.txt --force-reinstall
```

## 📄 Giấy Phép

MIT License

## 👥 Tác Giả

Dự án được phát triển cho mục đích học tập và ứng dụng quản lý thư viện.

## 📞 Hỗ Trợ

Nếu gặp lỗi, vui lòng:
1. Kiểm tra logs
2. Đọc documentation
3. Liên hệ quản trị viên

---

**Developed with ❤️ using Flask**
