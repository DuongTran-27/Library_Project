# Cải thiện: Tự động mượn sách cho người đặt trước

## 📋 Quy trình mới

```
A mượn sách X
  ↓
B, C đặt trước (waiting)
  ↓
A trả sách X → B tự động được mượn + gửi email thông báo "Đã nhận sách"
              → C được notified (chờ tiếp)
  ↓
B trả sách X → C tự động được mượn + gửi email thông báo "Đã nhận sách"
              → D (nếu có) được notified
```

## 🔧 Thay đổi code

### 1. `borrow_routes.py` - Hàm `return_book()` (khi user trả sách)

**Logic mới:**
```python
# Tìm người đặt đầu tiên
first_reservation = Reservation.query.filter_by(
    book_id=record.book_id,
    status='waiting'
).order_by(Reservation.reserved_at.asc()).first()

if first_reservation:
    # TỰ ĐỘNG MƯỢN: Tạo borrow record cho người đặt đầu
    due_date = datetime.utcnow() + timedelta(days=Config.BORROW_DURATION_DAYS)
    auto_borrow = BorrowRecord(
        user_id=first_reservation.user_id,
        book_id=record.book_id,
        due_date=due_date,
        notes='Tự động mượn từ đặt trước'
    )
    
    # Đánh dấu reservation = fulfilled (đã mượn)
    first_reservation.status = 'fulfilled'
    
    # Gửi email thông báo đã nhận sách
    send_borrow_confirmation(first_reservation.user, record.book, due_date)
    
    # Kiểm tra người tiếp theo
    next_reservation = Reservation.query.filter_by(
        book_id=record.book_id,
        status='waiting'
    ).order_by(Reservation.reserved_at.asc()).first()
    
    if next_reservation:
        next_reservation.status = 'notified'  # Gửi thông báo chờ
        send_reservation_ready_notification(next_reservation.user, record.book)
else:
    # Không ai đặt → tăng available_copies
    record.book.available_copies += 1
```

### 2. `borrow_routes.py` - Hàm `admin_return()` (khi admin trả sách)

**Logic giống với `return_book()`**

### 3. `templates/admin/reservations.html` - Cập nhật UI

```html
<!-- Status badges -->
{% if res.status == 'notified' %}
    <span class="badge bg-success">
        <i class="fas fa-check-circle"></i> Tự động được mượn
    </span>
{% endif %}

<!-- Buttons -->
{% if res.status == 'waiting' %}
    <!-- Nút Hủy -->
    <button class="btn btn-danger">Hủy</button>
{% elif res.status == 'notified' %}
    <!-- Nút Chờ (disabled) -->
    <button class="btn btn-info" disabled>Chờ nhận</button>
    <!-- Nút Hủy -->
    <button class="btn btn-danger">Hủy</button>
{% endif %}
```

### 4. `templates/user/reservations.html` - Cập nhật UI

```html
<!-- User thấy "Đã nhận sách!" thay vì "Sách đã sẵn" -->
{% if res.status == 'notified' %}
    <span class="badge bg-success">
        <i class="fas fa-check-circle"></i> Đã nhận sách!
    </span>
{% endif %}
```

## 📊 Trạng thái Reservation

| Status    | Ý nghĩa | Hành động |
|-----------|---------|----------|
| `waiting` | Chờ sách được trả | Khi sách trả → chuyển sang fulfilled/notified |
| `notified` | Đã được mượn tự động | Người dùng có thể xem sách trong "Sách của tôi" |
| `fulfilled` | Hoàn tất | Đã mượn xong |
| `cancelled` | Đã hủy | Hủy đặt trước |

## ✉️ Email gửi

1. **Khi được mượn tự động:**
   - Hàm: `send_borrow_confirmation()`
   - Nội dung: "Đã nhận sách {title}, hạn trả: {date}"

2. **Khi chờ trong hàng:**
   - Hàm: `send_reservation_ready_notification()`
   - Nội dung: "Bạn đang chờ trong hàng, vị trí: 2"

## 🎯 Lợi ích

✅ **Tự động hóa hoàn toàn** - Không cần admin xác nhận
✅ **Nhanh chóng** - Người đặt trước nhận sách ngay
✅ **Công bằng** - Hàng chờ FIFO (First In First Out)
✅ **Rõ ràng** - Hiển thị trạng thái "Đã nhận sách"
✅ **Thông báo** - Email tự động gửi đến người nhận

## 🧪 Test

```bash
# Run test script
venv/bin/python test_reservation.py

# Kết quả:
# - User1 mượn sách
# - User2, User3 đặt trước (waiting)
# - User1 trả sách
# - User2 tự động được mượn (fulfilled)
# - User3 chờ (notified/waiting)
```

## 📁 Files đã sửa

- ✅ `routes/borrow_routes.py` - Auto-borrow logic
- ✅ `templates/admin/reservations.html` - UI admin
- ✅ `templates/user/reservations.html` - UI user
- ✅ Server đang chạy ✅

**Status: READY TO USE** 🚀
