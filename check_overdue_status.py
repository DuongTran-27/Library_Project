"""
Kiểm tra kết quả quá hạn sách từ database
- Xem sách quá hạn
- Tính tiền phạt
- Kiểm tra email notifications
"""
from app import create_app, db
from models import User, BorrowRecord
from datetime import datetime

app = create_app()

def check_overdue_status():
    with app.app_context():
        print("\n" + "="*80)
        print("🔍 KIỂM TRA TRẠNG THÁI QUÁHẠN SÁCH")
        print("="*80 + "\n")
        
        # 1. Lấy user
        user = User.query.filter_by(username='tranphuocduong').first()
        if not user:
            print("❌ Không tìm user 'tranphuocduong'")
            return
        
        print(f"👤 User: {user.full_name} ({user.email})\n")
        
        # 2. Lấy sách đang mượn
        active_borrows = BorrowRecord.query.filter_by(
            user_id=user.id, 
            return_date=None
        ).all()
        
        print(f"📚 SÁCH ĐANG MƯỢN: {len(active_borrows)} cuốn\n")
        
        if not active_borrows:
            print("   (Không có sách đang mượn)\n")
        else:
            total_late_fee = 0
            
            for idx, record in enumerate(active_borrows, 1):
                is_overdue = record.is_overdue()
                late_fee = record.calculate_late_fee() if is_overdue else 0
                days_remaining = record.get_days_remaining()
                
                total_late_fee += late_fee
                
                status_icon = "⚠️ QUÁHẠN" if is_overdue else "✅ BÌNH THƯỜNG"
                
                print(f"[{idx}] {record.book.title}")
                print(f"     Ngày mượn: {record.borrow_date.strftime('%d/%m/%Y %H:%M')}")
                print(f"     Hạn trả: {record.due_date.strftime('%d/%m/%Y %H:%M')}")
                print(f"     Trạng thái: {status_icon}")
                
                if is_overdue:
                    overdue_days = (datetime.utcnow() - record.due_date).days
                    print(f"     Quá hạn: {overdue_days} ngày")
                    print(f"     Tiền phạt: {late_fee:,} VND")
                else:
                    print(f"     Còn lại: {days_remaining} ngày")
                
                print()
            
            print(f"💰 TỔNG TIỀN PHẠT: {total_late_fee:,} VND\n")
        
        # 3. Lịch sử mượn (đã trả)
        history = BorrowRecord.query.filter_by(user_id=user.id).filter(
            BorrowRecord.return_date.isnot(None)
        ).all()
        
        print(f"📖 LỊCH SỬ MƯỢN (ĐÃ TRẢ): {len(history)} cuốn\n")
        
        if history:
            total_fees_paid = 0
            
            for idx, record in enumerate(history, 1):
                total_fees_paid += record.late_fee if record.late_fee else 0
                
                print(f"[{idx}] {record.book.title}")
                print(f"     Ngày trả: {record.return_date.strftime('%d/%m/%Y %H:%M')}")
                print(f"     Tiền phạt: {record.late_fee:,} VND" if record.late_fee > 0 else "     Tiền phạt: Không")
                print()
            
            print(f"💵 TỔNG TIỀN PHẠT ĐÃ THU: {total_fees_paid:,} VND\n")
        
        # 4. Summary
        print("="*80)
        print("📊 TÓMLẠI:")
        print(f"  • Sách đang mượn: {len(active_borrows)} cuốn")
        print(f"  • Sách đã trả: {len(history)} cuốn")
        
        active_overdue = sum(1 for b in active_borrows if b.is_overdue())
        print(f"  • Sách quá hạn: {active_overdue} cuốn")
        print("="*80 + "\n")

if __name__ == '__main__':
    check_overdue_status()
