"""
Setup test data cho chức năng quá hạn sách
- Tạo sách quá hạn
- Kiểm tra tính tiền phạt
- Test gửi email thông báo
"""
from app import create_app, db
from models import User, Book, BorrowRecord
from datetime import datetime, timedelta

app = create_app()

def setup_overdue_test():
    with app.app_context():
        print("\n" + "="*70)
        print("🧪 SETUP TEST DỮ LIỆU - QUÁHẠN SÁCH + PHẠT TIỀN")
        print("="*70 + "\n")
        
        # 1. Lấy user
        user = User.query.filter_by(username='tranphuocduong').first()
        if not user:
            print("❌ Không tìm user 'tranphuocduong'")
            return False
        
        print(f"👤 User: {user.full_name} ({user.email})\n")
        
        # 2. Lấy 3 cuốn sách
        books = Book.query.limit(3).all()
        if len(books) < 3:
            print(f"❌ Cần ít nhất 3 sách, chỉ có {len(books)}")
            return False
        
        # 3. Xóa bản ghi cũ
        old_records = BorrowRecord.query.filter_by(user_id=user.id, return_date=None).all()
        if old_records:
            print(f"🗑️  Xóa {len(old_records)} bản ghi mượn cũ\n")
            for record in old_records:
                db.session.delete(record)
            db.session.commit()
        
        # 4. Tạo 3 scenario quá hạn khác nhau
        scenarios = [
            {
                'days_borrowed': 18,
                'label': 'Quá hạn 4 ngày',
                'description': 'Mượn 18 ngày = quá 4 ngày'
            },
            {
                'days_borrowed': 22,
                'label': 'Quá hạn 8 ngày',
                'description': 'Mượn 22 ngày = quá 8 ngày'
            },
            {
                'days_borrowed': 35,
                'label': 'Quá hạn 21 ngày',
                'description': 'Mượn 35 ngày = quá 21 ngày'
            }
        ]
        
        print("📚 Tạo 3 sách quá hạn:\n")
        
        for idx, scenario in enumerate(scenarios, 1):
            book = books[idx - 1]
            days = scenario['days_borrowed']
            
            borrow_date = datetime.utcnow() - timedelta(days=days)
            due_date = borrow_date + timedelta(days=14)
            overdue_days = (datetime.utcnow() - due_date).days
            late_fee = overdue_days * 5000
            
            borrow = BorrowRecord(
                user_id=user.id,
                book_id=book.id,
                borrow_date=borrow_date,
                due_date=due_date
            )
            db.session.add(borrow)
            db.session.commit()
            
            print(f"  [{idx}] ✅ {scenario['label']}")
            print(f"      📕 Sách: {book.title}")
            print(f"      📅 {scenario['description']}")
            print(f"      🗓️  Ngày mượn: {borrow_date.strftime('%d/%m/%Y %H:%M')}")
            print(f"      🔴 Hạn trả: {due_date.strftime('%d/%m/%Y %H:%M')} (quá {overdue_days} ngày)")
            print(f"      💰 Tiền phạt: {late_fee:,} VND ({overdue_days} ngày × 5,000 VND)\n")
        
        print("="*70)
        print("✅ SETUP HOÀN THÀNH!")
        print("="*70 + "\n")
        
        return True

if __name__ == '__main__':
    setup_overdue_test()
