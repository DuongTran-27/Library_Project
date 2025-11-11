# 🎯 CHẠY ỨNG DỤNG LẦN ĐẦUU

## 📋 Các Bước (Windows)

### 1️⃣ Double-click `setup.bat`
```
Nó sẽ tự động:
- Tạo virtual environment
- Cài đặt dependencies
- Khởi tạo database
- Tạo dữ liệu mẫu
```

### 2️⃣ Tạo tài khoản Admin
```bash
python run.py create_admin
```

Nhập:
- Username: `admin` (hoặc tùy chọn)
- Email: `admin@library.com`
- Password: `admin123` (hoặc tùy chọn)

### 3️⃣ Chạy ứng dụng
```bash
python run.py
```

### 4️⃣ Truy cập
```
http://localhost:5000
```

---

## 📋 Các Bước (Linux/Mac)

```bash
# 1. Làm executable
chmod +x setup.sh

# 2. Chạy setup
./setup.sh

# 3. Tạo admin
python run.py create_admin

# 4. Chạy ứng dụng
python run.py
```

---

## 🧪 Test Nhanh

Sau khi ứng dụng chạy, thử:

### Độc Giả Mẫu (Auto-created)
- Username: `user`
- Email: `user@example.com`
- Password: `password`

### Admin Mẫu (Bạn tạo)
- Username: (tùy chọn)
- Email: (tùy chọn)
- Password: (tùy chọn)

### Sách Mẫu (Auto-created)
- "Chiếc lá cuối cùng"
- "Nhà giả kim"
- "Bắc Mỹ độc lập"

---

## 🌐 URLs Quan Trọng

### Công Khai
- `http://localhost:5000/` - Trang chủ
- `http://localhost:5000/books` - Danh sách sách
- `http://localhost:5000/auth/login` - Đăng nhập
- `http://localhost:5000/auth/register` - Đăng ký

### Cần Đăng Nhập
- `http://localhost:5000/borrow/my-books` - Sách của tôi
- `http://localhost:5000/profile` - Hồ sơ
- `http://localhost:5000/profile/reservations` - Đặt trước

### Admin Only
- `http://localhost:5000/admin/dashboard` - Dashboard
- `http://localhost:5000/admin/users` - Quản lý độc giả
- `http://localhost:5000/admin/books` - Quản lý sách
- `http://localhost:5000/admin/categories` - Quản lý thể loại

### API
- `http://localhost:5000/api/books` - API: Danh sách sách
- `http://localhost:5000/api/categories` - API: Danh sách thể loại
- `http://localhost:5000/api/stats` - API: Thống kê

---

## ✨ Tính Năng Để Thử

### Người Dùng Thường
1. ✅ Đăng ký tài khoản mới
2. ✅ Tìm kiếm sách
3. ✅ Xem chi tiết sách
4. ✅ Mượn sách
5. ✅ Xem "Sách của tôi"
6. ✅ Gia hạn sách
7. ✅ Trả sách (tính tiền phạt)
8. ✅ Đặt trước sách hết
9. ✅ Xem hồ sơ
10. ✅ Đổi mật khẩu

### Admin
1. ✅ Dashboard xem thống kê
2. ✅ Thêm sách mới
3. ✅ Sửa/xóa sách
4. ✅ Thêm thể loại
5. ✅ Quản lý độc giả
6. ✅ Xem sách quá hạn
7. ✅ Xuất báo cáo PDF
8. ✅ Xem lịch sử mượn theo độc giả
9. ✅ Khóa/kích hoạt tài khoản
10. ✅ Quản lý đặt trước

---

## 🐛 Xử Lý Sự Cố

### Lỗi: Port 5000 đang sử dụng
```bash
# Chỉnh sửa file run.py
# Thay đổi dòng cuối cùng:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Database
```bash
# Xóa file database
rm library.db

# Khởi tạo lại
python run.py init_db
python run.py create_sample_data
```

### Email không gửi
1. Kiểm tra `.env` (MAIL_USERNAME, MAIL_PASSWORD)
2. Kiểm tra App Password Google
3. Kiểm tra kết nối internet

---

## 🔧 Tùy Chỉnh Cấu Hình

Mở file `.env`:

```ini
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///library.db

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📞 Cần Giúp?

1. **Kiểm tra README.md** - Tài liệu đầy đủ
2. **Kiểm tra QUICKSTART.md** - Hướng dẫn nhanh
3. **Kiểm tra FEATURES.md** - Danh sách tính năng
4. **Xem logs** - Kiểm tra thông báo lỗi
5. **Tìm kiếm code** - Xem cách triển khai

---

**Chúc bạn thành công! 🎉**

Nếu gặp lỗi, hãy đọc logs trong terminal để tìm nguyên nhân.
