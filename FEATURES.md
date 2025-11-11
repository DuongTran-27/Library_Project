# 📚 Hệ Thống Quản Lý Thư Viện Trực Tuyến - Tóm Tắt Hoàn Chỉnh

## ✨ Giới Thiệu Dự Án

**Hệ Thống Quản Lý Thư Viện Trực Tuyến** là ứng dụng web hiện đại được xây dựng bằng **Flask** để quản lý mượn/trả sách, tìm kiếm sách và quản lý độc giả. Ứng dụng có giao diện thân thiện, responsive trên tất cả thiết bị, và hỗ trợ đầy đủ các tính năng quản lý thư viện chuyên nghiệp.

---

## 🎯 Mục Tiêu Dự Án

✅ Quản lý toàn bộ quy trình mượn/trả sách
✅ Tìm kiếm sách nhanh chóng và dễ dàng
✅ Tính phạt trễ hạn tự động
✅ Hệ thống thông báo email
✅ Dashboard thống kê chi tiết
✅ Xuất báo cáo PDF
✅ Responsive design cho mobile

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|----------|---------|
| Flask | 2.3.3 | Framework web chính |
| SQLAlchemy | 2.0.21 | ORM quản lý database |
| Flask-Login | 0.6.2 | Xác thực người dùng |
| Flask-Mail | 0.9.1 | Gửi email |
| Flask-RESTful | 0.3.10 | Xây dựng API |
| Alembic | 1.12.1 | Migration database |

### Frontend
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|----------|---------|
| Bootstrap | 5.3.0 | CSS Framework |
| Jinja2 | 3.1.2 | Template engine |
| Font Awesome | 6.4.0 | Icons |
| JavaScript | ES6 | Interactivity |

### Database
| Database | Mục Đích |
|----------|---------|
| SQLite | Development/Testing |
| PostgreSQL | Production (tùy chọn) |

### Công Cụ Khác
| Công Cụ | Phiên Bản | Mục Đích |
|---------|----------|---------|
| ReportLab | 4.0.4 | Tạo PDF |
| python-dotenv | 1.0.0 | Quản lý environment |
| Werkzeug | 2.3.7 | Mã hóa mật khẩu |

---

## 📁 Cấu Trúc Dự Án

```
library_project/
│
├── app.py                      # Application factory
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── run.py                      # Entry point & CLI commands
│
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Full documentation
├── QUICKSTART.md               # Quick start guide
├── FEATURES.md                 # This file
│
├── setup.sh                    # Setup script (Linux/Mac)
├── setup.bat                   # Setup script (Windows)
│
├── routes/                     # Application routes
│   ├── __init__.py
│   ├── auth_routes.py          # Authentication
│   ├── book_routes.py          # Book management
│   ├── borrow_routes.py        # Borrow/return
│   ├── user_routes.py          # User profile
│   ├── admin_routes.py         # Admin panel
│   └── api_routes.py           # REST API
│
├── services/                   # Business logic
│   ├── __init__.py
│   ├── email_service.py        # Email notifications
│   └── pdf_service.py          # PDF generation
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── book/
│   │   ├── index.html          # Book list
│   │   ├── detail.html         # Book detail
│   │   ├── create.html         # Create book
│   │   └── edit.html           # Edit book
│   ├── borrow/
│   │   ├── my_books.html       # My borrows
│   │   └── history.html        # Borrow history
│   ├── user/
│   │   ├── profile.html        # User profile
│   │   ├── edit_profile.html
│   │   ├── change_password.html
│   │   └── reservations.html
│   └── admin/
│       ├── dashboard.html
│       ├── users.html
│       ├── user_detail.html
│       ├── books.html
│       ├── categories.html
│       ├── create_category.html
│       ├── edit_category.html
│       ├── overdue_books.html
│       ├── reservations.html
│       └── reports.html
│
└── static/                     # Static files (Optional)
    ├── css/
    ├── js/
    └── images/
```

---

## 🚀 Tính Năng Chi Tiết

### 1️⃣ Quản Lý Sách

#### Tìm Kiếm & Duyệt
- 🔍 Tìm kiếm theo tên sách, tác giả, ISBN
- 📂 Lọc theo thể loại
- 📄 Phân trang (10 sách/trang)
- 📊 Hiển thị số lượng sẵn có

#### Quản Lý Sách (Admin)
- ➕ Thêm sách mới với ISBN, nhà xuất bản, năm xuất bản
- ✏️ Chỉnh sửa thông tin sách
- 🗑️ Xóa sách
- 🏷️ Gán thể loại
- 📷 Hỗ trợ ảnh bìa (link)

#### Thể Loại
- 📚 Tạo thể loại mới
- 🔄 Gán sách vào thể loại
- 📊 Xem số sách trong mỗi thể loại

---

### 2️⃣ Hệ Thống Mượn/Trả

#### Mượn Sách
- ✅ Mượn sách sẵn có
- ⏰ Hạn mượn mặc định: **14 ngày**
- 🚫 Giới hạn: **Tối đa 5 sách/lần**
- 🚷 Không được mượn nếu có sách quá hạn
- ✉️ Nhận xác nhận qua email

#### Trả Sách
- ✅ Xác nhận trả sách
- 💰 Tính phạt trễ hạn tự động
  - **5,000 VND/ngày**
  - Ví dụ: Quá 3 ngày = 15,000 VND
- ✉️ Nhận xác nhận qua email

#### Gia Hạn
- 🔄 Gia hạn 1 lần (thêm 14 ngày)
- 🚫 Không gia hạn nếu quá hạn
- ✨ Tối ưu cho độc giả đọc chậm

#### Lịch Sử Mượn
- 📋 Xem tất cả sách đã mượn
- 🕐 Ngày mượn, ngày trả
- 💰 Tiền phạt đã trả

---

### 3️⃣ Hệ Thống Đặt Trước

#### Đặt Trước Sách
- 📅 Đặt trước khi sách hết
- ⏳ Chờ sách sẵn có
- ✉️ Nhận email khi sách có
- ⏱️ Có 3 ngày để đến mượn
- ❌ Hủy đặt trước nếu cần

#### Danh Sách Chờ
- 👥 Xem vị trí trong danh sách chờ
- 📊 Xem số người chờ của từng sách

---

### 4️⃣ Xác Thực & Phân Quyền

#### Đăng Ký
- 📝 Form đăng ký đơn giản
- 🔒 Mật khẩu tối thiểu 6 ký tự
- ✉️ Xác thực email độc lập

#### Đăng Nhập
- 🔐 Đăng nhập an toàn
- 🔒 Mật khẩu được mã hóa Werkzeug
- 🍪 Session management
- ↩️ Redirect về trang yêu cầu sau login

#### Phân Quyền
| Quyền | User Thường | Admin |
|------|-----------|-------|
| Xem sách | ✅ | ✅ |
| Mượn sách | ✅ | ✅ |
| Trả sách | ✅ | ✅ |
| Quản lý sách | ❌ | ✅ |
| Quản lý độc giả | ❌ | ✅ |
| Quản lý thể loại | ❌ | ✅ |
| Xem báo cáo | ❌ | ✅ |

---

### 5️⃣ Hồ Sơ Người Dùng

#### Xem Hồ Sơ
- 👤 Thông tin cá nhân
- 📚 Sách đang mượn
- ⚠️ Số sách quá hạn
- 💰 Tổng tiền phạt

#### Chỉnh Sửa
- ✏️ Cập nhật tên, điện thoại, địa chỉ
- 🔑 Đổi mật khẩu
- 🔒 Bảo mật tài khoản

---

### 6️⃣ Dashboard Admin

#### Thống Kê Tổng Quát
- 📊 Tổng số sách
- ✅ Sách sẵn có
- 📤 Sách đang mượn
- ⚠️ Sách quá hạn
- 👥 Tổng độc giả

#### Biểu Đồ & Thống Kê
- 🔥 Sách mượn nhiều nhất (Top 5)
- ⭐ Độc giả tích cực (Top 5)
- 📉 Xu hướng mượn sách

---

### 7️⃣ Quản Lý Độc Giả

#### Danh Sách Độc Giả
- 🔍 Tìm kiếm theo tên, email, username
- 📋 Xem danh sách phân trang
- 🔓 Khóa/kích hoạt tài khoản

#### Chi Tiết Độc Giả
- 👤 Thông tin cá nhân
- 📚 Sách đang mượn
- 📊 Lịch sử mượn sách
- 💰 Tổng tiền phạt
- 📥 Xác nhận trả sách

---

### 8️⃣ Báo Cáo & Xuất Dữ Liệu

#### Báo Cáo Thống Kê PDF
- 📊 Tổng sách, sách sẵn có, sách mượn
- 🔥 Sách mượn nhiều nhất
- ⭐ Độc giả tích cực
- 📅 Ngày tạo báo cáo

#### Lịch Sử Mượn PDF
- 📋 Lịch sử mượn sách của độc giả
- 💰 Tiền phạt trả
- 📅 Ngày mượn, ngày trả
- 📩 Gửi email khách hàng

---

### 9️⃣ Email Notifications

#### Loại Email
- ✉️ **Xác nhận mượn**: Hạn trả sách
- ✉️ **Xác nhận trả**: Sách đã nhận
- ✉️ **Nhắc nhở quá hạn**: 3 ngày trước
- ✉️ **Sách sẵn có**: Sách bạn đặt có sẵn
- ✉️ **Thông báo phạt**: Tiền phạt

---

### 🔟 API RESTful

#### Endpoints Book
```
GET    /api/books                  # Danh sách sách
GET    /api/books/<id>             # Chi tiết sách
GET    /api/categories             # Danh sách thể loại
```

#### Endpoints User
```
GET    /api/my-borrows             # Sách đang mươn (auth)
POST   /api/borrow/<book_id>       # Mượn sách (auth)
POST   /api/return/<record_id>     # Trả sách (auth)
```

#### Endpoints Search & Stats
```
GET    /api/search?q=<query>       # Tìm kiếm
GET    /api/stats                  # Thống kê thư viện
```

---

## 💻 Giao Diện Người Dùng

### Responsive Design
- 📱 **Mobile**: < 576px (full width)
- 📱 **Tablet**: 576px - 992px (2 cột)
- 🖥️ **Desktop**: > 992px (3+ cột)
- 🎨 **Bootstrap 5** Grid System

### Themes & Colors
- 🎨 **Primary**: #1f4788 (xanh đậm)
- 🟢 **Success**: #28a745
- 🟡 **Warning**: #ffc107
- 🔴 **Danger**: #dc3545
- 🔵 **Info**: #17a2b8

### User Experience
- ⚡ Giao diện nhanh chóng
- 🎯 Navigation rõ ràng
- 📱 Mobile-friendly
- ♿ Accessible
- 🌗 Dark mode (optional)

---

## 📊 Database Schema

### Bảng Users
```sql
- id (PK)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- full_name
- phone
- address
- is_active
- is_admin
- created_at, updated_at
```

### Bảng Books
```sql
- id (PK)
- title
- author
- isbn (UNIQUE)
- publisher
- published_year
- description
- total_copies
- available_copies
- cover_image
- created_at, updated_at
```

### Bảng BorrowRecords
```sql
- id (PK)
- user_id (FK)
- book_id (FK)
- borrow_date
- due_date
- return_date
- late_fee
- notes
- created_at, updated_at
```

### Bảng Reservations
```sql
- id (PK)
- user_id (FK)
- book_id (FK)
- reserved_at
- status (waiting/notified/fulfilled)
- notes
- created_at, updated_at
```

### Bảng Categories
```sql
- id (PK)
- name (UNIQUE)
- description
- created_at
```

---

## 🔒 Bảo Mật

### Authentication
- 🔐 Mật khẩu được mã hóa Werkzeug
- 🍪 Session-based authentication
- 🔑 Flask-Login decorator
- ✅ CSRF protection

### Authorization
- 🚷 Role-based access control
- 👤 User vs Admin permissions
- 🔓 Login required decorator
- ⚠️ Khóa tài khoản

### Data Protection
- 🛡️ SQL Injection prevention (SQLAlchemy ORM)
- 🛡️ XSS protection (Jinja2 escaping)
- 🛡️ Secure password storage
- 🛡️ Environment variables

---

## 📈 Hiệu Suất

### Optimizations
- 📦 Database indexing trên columns hay query
- 💾 Query caching (SQLAlchemy)
- ⚡ Lazy loading relationships
- 🔄 Efficient pagination

### Scalability
- 🗄️ PostgreSQL hỗ trợ cho production
- 🔄 Connection pooling
- 📊 Database backup
- 🚀 Horizontal scaling ready

---

## 🧪 Testing

### Chưa Implement
- [ ] Unit tests
- [ ] Integration tests
- [ ] API tests
- [ ] UI tests

### Cách Thêm Tests (Future)
```python
# tests/test_models.py
# tests/test_routes.py
# tests/test_api.py
pytest  # Chạy tests
```

---

## 📋 Checklist Tính Năng

### Core Features
- ✅ Quản lý sách (CRUD)
- ✅ Quản lý mượn/trả
- ✅ Gia hạn sách
- ✅ Đặt trước sách
- ✅ Tính phạt trễ hạn
- ✅ Dashboard thống kê
- ✅ Email notifications
- ✅ Xuất báo cáo PDF
- ✅ RESTful API
- ✅ Responsive UI

### Nice-to-Have (Future)
- [ ] SMS notifications
- [ ] QR code scan
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Dark theme
- [ ] Social features

---

## 🤝 Contribution

Dự án này là cho mục đích học tập. Bạn có thể:
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🧪 Add tests

---

## 📄 Giấy Phép

MIT License - Miễn phí sử dụng, sửa đổi, phân phối

---

## 🎓 Học Tập

Dự án này giúp bạn học:
- ✅ **Backend**: Flask, SQLAlchemy, ORM
- ✅ **Frontend**: Bootstrap, Jinja2, HTML/CSS
- ✅ **Database**: SQL, PostgreSQL, SQLite
- ✅ **API**: RESTful design, JSON
- ✅ **Email**: SMTP, Flask-Mail
- ✅ **PDF**: ReportLab
- ✅ **Security**: Authentication, Authorization
- ✅ **DevOps**: Environment variables, Deployment

---

## 📞 Support

Nếu cần trợ giúp:
1. Đọc README.md đầy đủ
2. Xem QUICKSTART.md
3. Kiểm tra logs trong terminal
4. Tìm kiếm trong codebase

---

**Tạo bởi: Nhà phát triển Python**
**Ngày: 2025**
**Phiên bản: 1.0.0**

---
