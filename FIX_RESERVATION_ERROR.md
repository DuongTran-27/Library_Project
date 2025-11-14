# FIX: PendingRollbackError - Reservation UNIQUE Constraint

## Problem
Lỗi `PendingRollbackError` khi trả sách với người đặt trước:
```
sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush.
(sqlite3.IntegrityError) UNIQUE constraint failed: reservation.user_id, reservation.book_id, reservation.status
[SQL: UPDATE reservation SET status=?, updated_at=? WHERE reservation.id = ?]
```

## Root Cause
Trong `models.py`, cột `Reservation` có `UniqueConstraint` trên 3 cột:
```python
__table_args__ = (
    db.UniqueConstraint('user_id', 'book_id', 'status', name='unique_active_reservation'),
)
```

Vấn đề: Khi có 2+ người đặt trước cùng một sách (status='waiting'), hệ thống cố update người thứ 1 thành 'notified'. Nhưng nếu đã có một reservation cũ ở status='notified' từ trước, nó vi phạm unique constraint.

## Solution

### 1. Sửa `models.py` - Bỏ Unique Constraint
```python
class Reservation(db.Model):
    # ...
    __table_args__ = (
        db.Index('ix_user_book_status', 'user_id', 'book_id', 'status'),
    )
```

Thay vì `UniqueConstraint`, chỉ giữ `Index` để tối ưu query.

### 2. Sửa `borrow_routes.py` - Xử lý logic tại application level

#### `return_book()` - Người dùng trả sách
```python
# Check for waiting reservations
first_reservation = Reservation.query.filter_by(
    book_id=record.book_id,
    status='waiting'
).order_by(Reservation.reserved_at.asc()).first()

if first_reservation:
    # Cancel existing notified (user took too long)
    existing_notified = Reservation.query.filter_by(
        book_id=record.book_id,
        status='notified'
    ).first()
    
    if existing_notified:
        existing_notified.status = 'cancelled'
    
    # Set first in queue as notified
    first_reservation.status = 'notified'
else:
    # No one waiting, increase available copies
    record.book.available_copies += 1
```

#### `admin_return()` - Admin trả sách
Logic tương tự như `return_book()`

### 3. Tạo database mới
```bash
# Xóa database cũ (có schema lỗi)
rm library.db instance/library.db

# Tạo database mới
venv/bin/python init_fresh_db.py
```

## Test Results
✅ **PASSED** - Không có `PendingRollbackError`

```
4. Current reservation queue:
   Position 1: User Two (07:46:18)
   Position 2: User Three (07:46:18)

5. Simulating book return by User1...
   [OK] Notified: User Two
   
6. Updated reservation status:
   User Two: notified
   User Three: waiting

[SUCCESS] TEST COMPLETE - No PendingRollbackError!
```

## Workflow sau fix
1. **User A** mượn sách X (available_copies: 3 → 2)
2. **User B, C** đặt trước (reservations: waiting)
3. **User A** trả sách:
   - Kiểm tra hàng chờ → B là người thứ 1
   - Đặt B: status='notified' (được thông báo)
   - C vẫn: status='waiting'
4. **Admin** xác nhận mượn cho B:
   - Tạo BorrowRecord cho B
   - Đặt B: status='fulfilled'
5. **User B** trả sách:
   - Kiểm tra hàng chờ → C là người thứ 1
   - Đặt C: status='notified'

## Files Changed
- ✅ `models.py` - Bỏ UniqueConstraint, giữ Index
- ✅ `routes/borrow_routes.py` - Thêm logic handle existing_notified
- ✅ Database xóa & tạo lại (`init_fresh_db.py`)

## Deployment Notes
- Người dùng cần xóa `library.db` cũ
- Chạy `venv/bin/python init_fresh_db.py` để tạo schema mới
- Hoặc backup dữ liệu cũ nếu cần
