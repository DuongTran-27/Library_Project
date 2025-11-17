"""Create test borrow data for admin return testing"""
from app import create_app, db
from models import User, Book, BorrowRecord
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("TẠO DỮ LIỆU TEST - SÁCH ĐANG MƯỢN")
    print("="*60 + "\n")
    
    # Get user
    user = User.query.filter_by(username='tranphuocduong').first()
    if not user:
        print("❌ Không tìm user 'tranphuocduong'")
        exit(1)
    
    # Get book
    book = Book.query.first()
    if not book:
        print("❌ Không có sách nào")
        exit(1)
    
    # Delete existing active borrows for this user
    existing = BorrowRecord.query.filter_by(user_id=user.id, return_date=None).all()
    if existing:
        for record in existing:
            db.session.delete(record)
        db.session.commit()
        print(f"🗑️  Xóa {len(existing)} bản ghi mượn cũ\n")
    
    # Create new borrow record
    borrow_date = datetime.utcnow() - timedelta(days=5)
    due_date = borrow_date + timedelta(days=14)
    
    borrow = BorrowRecord(
        user_id=user.id,
        book_id=book.id,
        borrow_date=borrow_date,
        due_date=due_date
    )
    
    db.session.add(borrow)
    db.session.commit()
    
    print(f"✅ Tạo sách mượn thành công:\n")
    print(f"  👤 User: {user.full_name} ({user.username})")
    print(f"  📕 Sách: {book.title}")
    print(f"  📅 Ngày mượn: {borrow_date.strftime('%d/%m/%Y')}")
    print(f"  📅 Hạn trả: {due_date.strftime('%d/%m/%Y')}")
    print(f"  🆔 Record ID: {borrow.id}\n")
    
    print("="*60)
    print("✅ BÂY GIỜ BẠN CÓ THỂ:")
    print("  1. Đăng nhập admin: admin / admin123")
    print("  2. Vào: Admin → Quản Lý Người Dùng")
    print(f"  3. Click vào user: {user.full_name}")
    print("  4. Thấy nút 'Trả' và click để test")
    print("="*60 + "\n")
