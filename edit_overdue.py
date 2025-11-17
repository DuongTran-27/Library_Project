"""
Script để chỉnh sửa ngày mượn sách làm cho nó quá hạn
Điều chỉnh linh hoạt theo nhu cầu test
"""
from app import create_app, db
from models import BorrowRecord
from datetime import datetime, timedelta

app = create_app()

def edit_borrow_record(record_id, days_overdue):
    """
    Chỉnh sửa bản ghi mượn để tạo quá hạn
    
    Args:
        record_id: ID của bản ghi mượn
        days_overdue: Số ngày quá hạn (vd: 5 = quá 5 ngày)
    """
    with app.app_context():
        print("\n" + "="*70)
        print("✏️  CHỈNH SỬA NGÀY MƯỢN - TẠO QUÁHẠN SÁCH")
        print("="*70 + "\n")
        
        record = BorrowRecord.query.get(record_id)
        if not record:
            print(f"❌ Không tìm thấy bản ghi ID: {record_id}")
            return False
        
        if record.return_date:
            print(f"❌ Sách này đã được trả rồi (ngày trả: {record.return_date})")
            return False
        
        # Tính ngày mượn mới để tạo quá hạn
        # Công thức: Hôm nay - (14 + days_overdue) = Ngày mượn
        days_borrowed = 14 + days_overdue
        new_borrow_date = datetime.utcnow() - timedelta(days=days_borrowed)
        new_due_date = new_borrow_date + timedelta(days=14)
        
        print(f"📚 Sách: {record.book.title}")
        print(f"👤 User: {record.user.full_name}\n")
        
        print("🔴 TRƯỚC:")
        print(f"  Ngày mượn: {record.borrow_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Hạn trả: {record.due_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Quá hạn? {record.is_overdue()}")
        if record.is_overdue():
            print(f"  Tiền phạt: {record.calculate_late_fee():,} VND\n")
        else:
            print()
        
        # Cập nhật
        record.borrow_date = new_borrow_date
        record.due_date = new_due_date
        db.session.commit()
        
        print("🟢 SAU:")
        print(f"  Ngày mượn: {record.borrow_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Hạn trả: {record.due_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Quá hạn? {record.is_overdue()}")
        print(f"  Tiền phạt: {record.calculate_late_fee():,} VND\n")
        
        print("="*70)
        print("✅ CHỈNH SỬA THÀNH CÔNG!")
        print("="*70 + "\n")
        
        return True


def list_all_borrows():
    """Liệt kê tất cả sách đang mượn"""
    with app.app_context():
        print("\n" + "="*70)
        print("📋 DANH SÁCH SÁCH ĐANG MƯỢN")
        print("="*70 + "\n")
        
        records = BorrowRecord.query.filter_by(return_date=None).all()
        
        if not records:
            print("(Không có sách đang mượn)\n")
            return
        
        for record in records:
            status = "⚠️ QUÁHẠN" if record.is_overdue() else "✅ BÌNH THƯỜNG"
            late_fee = record.calculate_late_fee() if record.is_overdue() else 0
            
            print(f"🆔 ID: {record.id}")
            print(f"   📕 Sách: {record.book.title}")
            print(f"   👤 User: {record.user.full_name}")
            print(f"   📅 Hạn trả: {record.due_date.strftime('%d/%m/%Y')}")
            print(f"   Trạng thái: {status}")
            if record.is_overdue():
                print(f"   💰 Tiền phạt: {late_fee:,} VND")
            print()
        
        print("="*70 + "\n")


if __name__ == '__main__':
    import sys
    
    # Liệt kê tất cả sách đang mượn
    list_all_borrows()
    
    # Ví dụ: Chỉnh sửa record ID 1 để quá hạn 5 ngày
    if len(sys.argv) > 2:
        record_id = int(sys.argv[1])
        days_overdue = int(sys.argv[2])
        edit_borrow_record(record_id, days_overdue)
    else:
        print("\n💡 CÁCH SỬ DỤNG:")
        print("   python edit_overdue.py <record_id> <days_overdue>\n")
        print("   Ví dụ:")
        print("   python edit_overdue.py 1 5    (Sách ID 1 quá hạn 5 ngày)")
        print("   python edit_overdue.py 2 10   (Sách ID 2 quá hạn 10 ngày)")
        print("   python edit_overdue.py 3 20   (Sách ID 3 quá hạn 20 ngày)\n")
