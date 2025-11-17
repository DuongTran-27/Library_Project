# 📖 HƯỚNG DẪN TEST CHỨC NĂNG QUÁHẠN SÁCH + PHẠT TIỀN

## ⚙️ CẤU HÌNH HỆ THỐNG

| Thông số | Giá trị |
|---------|--------|
| Thời gian mượn | 14 ngày |
| Tiền phạt/ngày | 5,000 VND |
| Nhắc nhở trước | 3 ngày |

---

## 🚀 BƯỚC 1: SETUP DỮ LIỆU TEST

Chạy lệnh để tạo 3 sách quá hạn:

```bash
python setup_overdue_test.py
```

**Kết quả:**
- Sách 1: Quá hạn 4 ngày → Phạt 20,000 VND
- Sách 2: Quá hạn 8 ngày → Phạt 40,000 VND  
- Sách 3: Quá hạn 21 ngày → Phạt 105,000 VND

---

## 🌐 BƯỚC 2: TEST GIAO DIỆN USER

### 2.1 Xem sách quá hạn

1. **Đăng nhập:**
   - URL: http://localhost:5000
   - Username: `tranphuocduong`
   - Password: `123456`

2. **Click "Sách của tôi"**

3. **Mong đợi thấy:**
   - ✅ 3 cuốn sách đang mượn
   - ⚠️ Badge **"QUÁHẠN"** (màu đỏ) cho mỗi sách
   - 💰 Hiển thị **tiền phạt** dưới tên sách
   - 📅 Hiển thị **ngày hạn trả**
   - 🔴 Background sách quá hạn là màu nhạt

**Giao diện ví dụ:**
```
[Sách 1] ⚠️ QUÁHẠN
Hạn trả: 15/11/2025
Tiền phạt: 20,000 VND
[Gia hạn]  [Liên hệ admin để trả sách]
```

### 2.2 Kiểm tra trang lịch sử

1. Click **"Lịch sử mượn"**
2. Mong đợi thấy các sách đã trả với tiền phạt

---

## 👨‍💼 BƯỚC 3: TEST GIAO DIỆN ADMIN

### 3.1 Xem sách quá hạn của user

1. **Đăng nhập admin:**
   - Username: `admin`
   - Password: `admin123`

2. **Admin Dashboard → Quản Lý Người Dùng**

3. **Click vào user: "Trần Phước Dương"**

4. **Mong đợi thấy:**
   - ✅ Phần "Sách Đang Mượn"
   - ⚠️ 3 sách với badge "Quá hạn" (màu đỏ)
   - 💰 Hiển thị tiền phạt
   - 🔘 Nút **"Trả"** cho mỗi sách

**Giao diện ví dụ:**
```
[Sách Đang Mượn] (3)
┌─────────────────────────────────────────────┐
│ Tên Sách      │ Hạn Trả    │ Trạng Thái │ HĐ │
├─────────────────────────────────────────────┤
│ [Sách 1]      │ 15/11/2025 │ Quá hạn    │ Trả│
│ [Sách 2]      │ 15/11/2025 │ Quá hạn    │ Trả│
│ [Sách 3]      │ 15/11/2025 │ Quá hạn    │ Trả│
└─────────────────────────────────────────────┘
```

### 3.2 Xác nhận trả sách & tính tiền phạt

1. **Admin click nút "Trả"** cho sách 1

2. **Mong đợi:**
   - ✅ Sách biến mất khỏi "Sách Đang Mượn"
   - ✅ Sách xuất hiện ở "Lịch Sử Mượn" với tiền phạt
   - ✅ Flash message: "Sách đã được trả thành công"
   - ✅ Hiển thị tiền phạt: "Tiền phạt: 20,000 VND"

3. **Kiểm tra "Lịch Sử Mượn":**
   - Thấy sách 1 với `Tiền Phạt: 20,000 VND`

---

## 📧 BƯỚC 4: TEST EMAIL THÔNG BÁO

### 4.1 Kiểm tra logs email

1. **Mở file:** `logs/` hoặc kiểm tra terminal Flask

2. **Mong đợi thấy logs:**
   ```
   📧 Email sent to tranphuocduong2704@gmail.com
   Subject: Thông báo trả sách - Quá hạn
   Body: Bạn có sách quá hạn, vui lòng trả sách trong 3 ngày...
   ```

### 4.2 Cấu hình email (nếu muốn test thực)

Tạo file `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

Nếu không cấu hình, hệ thống sẽ log thay vì gửi thực.

---

## 🔍 BƯỚC 5: DEBUG & KIỂM CHỨNG

### 5.1 Kiểm tra database

```bash
python
```

Trong Python shell:
```python
from app import create_app, db
from models import User, BorrowRecord

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='tranphuocduong').first()
    
    # Sách đang mượn
    active = BorrowRecord.query.filter_by(user_id=user.id, return_date=None).all()
    print(f"Sách đang mượn: {len(active)}")
    for b in active:
        print(f"  - {b.book.title}")
        print(f"    Quá hạn? {b.is_overdue()}")
        print(f"    Tiền phạt: {b.calculate_late_fee():,} VND")
        print(f"    Ngày còn: {b.get_days_remaining()} ngày\n")
    
    # Lịch sử
    history = BorrowRecord.query.filter_by(user_id=user.id).filter(BorrowRecord.return_date.isnot(None)).all()
    print(f"\nSách đã trả: {len(history)}")
    for b in history:
        print(f"  - {b.book.title}: {b.late_fee:,} VND")

exit()
```

### 5.2 Kiểm tra tính toán tiền phạt

```python
from app import create_app
from models import BorrowRecord
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    borrow = BorrowRecord.query.first()
    
    print(f"Sách: {borrow.book.title}")
    print(f"Ngày mượn: {borrow.borrow_date}")
    print(f"Hạn trả: {borrow.due_date}")
    print(f"Hôm nay: {datetime.utcnow()}")
    print(f"\nQuá hạn? {borrow.is_overdue()}")
    print(f"Ngày quá: {(datetime.utcnow() - borrow.due_date).days} ngày")
    print(f"Tiền phạt: {borrow.calculate_late_fee():,} VND")

exit()
```

---

## ✅ CHECKLIST TEST HOÀN CHỈNH

- [ ] Chạy `python setup_overdue_test.py` thành công
- [ ] User xem "Sách của tôi" thấy 3 sách quá hạn
- [ ] Mỗi sách có badge ⚠️ "QUÁHẠN"
- [ ] Mỗi sách hiển thị tiền phạt đúng:
  - [ ] Sách 1: 20,000 VND (4 ngày)
  - [ ] Sách 2: 40,000 VND (8 ngày)
  - [ ] Sách 3: 105,000 VND (21 ngày)
- [ ] User không thấy nút "Trả" (chỉ "Gia hạn")
- [ ] Admin xem được sách quá hạn của user
- [ ] Admin click "Trả" thành công
- [ ] Sách chuyển sang "Lịch Sử Mượn"
- [ ] Tiền phạt được lưu và hiển thị
- [ ] Email/log thông báo được gửi
- [ ] Công thức tính tiền phạt chính xác

---

## 🧮 CÔNG THỨC TÍNH TIỀN PHẠT

```
Quá hạn (ngày) = Ngày hôm nay - Ngày hạn trả
Tiền phạt (VND) = Quá hạn (ngày) × 5,000 VND/ngày

Ví dụ:
  Hạn trả: 15/11/2025 10:00
  Hôm nay: 17/11/2025 10:00
  Quá hạn: 2 ngày
  Tiền phạt: 2 × 5,000 = 10,000 VND
```

---

## 🎬 TEST FLOW HOÀN CHỈNH (Tóm tắt)

```
1️⃣ python setup_overdue_test.py
   ↓
2️⃣ User đăng nhập → "Sách của tôi"
   → Thấy 3 sách quá hạn + tiền phạt
   ↓
3️⃣ Admin đăng nhập → Quản Lý Người Dùng
   → Click user → Thấy nút "Trả"
   ↓
4️⃣ Admin click "Trả"
   → Tính tiền phạt tự động
   → Gửi email thông báo
   → Sách chuyển sang lịch sử
   ↓
5️⃣ ✅ TEST PASS
```

---

## 💡 Tips Hữu Ích

1. **Để reset test:** Xóa database `instance/library.db` rồi chạy `init_fresh_db.py`
2. **Để xem logs chi tiết:** Set `DEBUG = True` trong `config.py`
3. **Để test email:** Kiểm tra terminal Flask hoặc log file
4. **Để tính toán nhanh:** Dùng Python shell để kiểm tra công thức

---

**Bạn sẵn sàng test chưa? 🚀**
