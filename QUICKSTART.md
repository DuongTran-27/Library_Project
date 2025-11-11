# Hướng Dẫn Nhanh - Hệ Thống Quản Lý Thư Viện

## 🚀 Bắt Đầu Nhanh Nhất

### Windows
1. Double-click `setup.bat`
2. Sau khi hoàn tất, chạy: `python run.py create_admin`
3. Chạy: `python run.py`
4. Truy cập: http://localhost:5000

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
python run.py create_admin
python run.py
```

---

## 📚 Các Tính Năng Chính

| Tính Năng | Người Dùng | Admin |
|-----------|-----------|-------|
| Tìm kiếm sách | ✅ | ✅ |
| Mượn sách | ✅ | ✅ |
| Trả sách | ✅ | ✅ |
| Gia hạn | ✅ | ✅ |
| Đặt trước | ✅ | ✅ |
| Lịch sử mượn | ✅ | ✅ |
| Quản lý sách | ❌ | ✅ |
| Quản lý độc giả | ❌ | ✅ |
| Báo cáo PDF | ❌ | ✅ |
| Dashboard | ❌ | ✅ |

---

## 🔑 Đăng Nhập Mặc Định (Sau Khi Chạy setup.bat)

**Admin Test Account** (tạo bằng `python run.py create_admin`):
- Username: Nhập khi chạy lệnh
- Password: Nhập khi chạy lệnh

---

## 📱 Điều Hướng

### Người Dùng Thường
```
Trang chủ → Duyệt sách → Mượn sách → Sách của tôi → Lịch sử
                              ↓
                         Đặt trước (nếu hết)
```

### Quản Trị Viên
```
Dashboard → Quản lý sách/độc giả/thể loại → Báo cáo
                ↓
           Sách quá hạn → Xác nhận trả
```

---

## 📧 Cấu Hình Email (Gmail)

1. Mở file `.env`
2. Cấu hình Gmail:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

3. Lấy App Password:
   - Vào https://myaccount.google.com/apppasswords
   - Chọn Mail + Windows Computer
   - Copy password vào .env

---

## 💡 Mẹo Sử Dụng

### Mượn Sách
- Nhấn **"Mượn Sách"** trên trang chi tiết
- Hạn trả tự động = 14 ngày
- Có thể gia hạn 1 lần (thêm 14 ngày)
- Không được mượn quá 5 sách cùng lúc

### Phạt Trễ Hạn
- **5,000 VND/ngày** tính từ ngày quá hạn
- Ví dụ: Quá hạn 3 ngày = 15,000 VND
- Thông báo email 3 ngày trước khi hạn trả

### Đặt Trước
- Nếu sách hết, bạn có thể **Đặt Trước**
- Nhận email khi sách sẵn có
- Có 3 ngày để đến mượn

### Admin Dashboard
- **Thống kê**: Xem tổng sách, sách mượn, sách quá hạn
- **Sách mượn nhiều nhất**: Xem đâu là cuốn sách được yêu thích
- **Độc giả tích cực**: Xem ai mượn sách nhiều nhất
- **Xuất PDF**: Báo cáo thống kê hoặc lịch sử mượn theo độc giả

---

## 🐛 Xử Lý Sự Cố

### Lỗi: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Database bị lỗi
```bash
# Xóa file library.db (nếu có)
rm library.db

# Khởi tạo lại
python run.py init_db
python run.py create_sample_data
```

### Email không gửi
- Kiểm tra `.env` (MAIL_USERNAME, MAIL_PASSWORD)
- Kiểm tra kết nối internet
- Kiểm tra App Password Google là đúng

### Port 5000 đang sử dụng
```bash
# Chỉnh sửa run.py, dòng cuối:
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 🌐 API Endpoints

```
GET    /api/books                  - Danh sách sách
GET    /api/books/<id>             - Chi tiết sách
GET    /api/categories             - Danh sách thể loại
GET    /api/my-borrows             - Sách đang mượn (auth)
POST   /api/borrow/<book_id>       - Mượn sách (auth)
POST   /api/return/<record_id>     - Trả sách (auth)
GET    /api/search?q=<query>       - Tìm kiếm
GET    /api/stats                  - Thống kê
```

---

## 📞 Hỗ Trợ

Nếu gặp lỗi:

1. **Đọc logs** trong terminal
2. **Kiểm tra README.md** đầy đủ
3. **Xem cấu trúc thư mục** trong routes/templates

---

## 🎓 Học Tập

Dự án này giúp bạn học:
- ✅ Flask Framework
- ✅ SQLAlchemy ORM
- ✅ Flask-Login Authentication
- ✅ RESTful API
- ✅ Jinja2 Templates
- ✅ Bootstrap 5
- ✅ Email Notifications
- ✅ PDF Generation

---

**Chúc bạn sử dụng vui vẻ! 🎉**
