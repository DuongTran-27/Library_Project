"""
PDF Service - Stub version without ReportLab
ReportLab requires C++ compilation on Windows
To enable full PDF support, install Visual C++ Build Tools and run:
  pip install reportlab==4.0.4
"""

from io import BytesIO
from datetime import datetime

def generate_borrow_report_pdf(borrow_records, user=None):
    """Generate PDF report for borrow records - STUB version"""
    # Return text report instead of PDF
    text = "BÁOCÁO MƯỢN SÁCH\n"
    text += "=" * 60 + "\n\n"
    
    if user:
        text += f"Độc giả: {user.full_name} ({user.username})\n"
        text += f"Email: {user.email}\n\n"
    
    text += f"Ngày báo cáo: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}\n"
    text += "-" * 60 + "\n\n"
    
    if borrow_records:
        text += "STT | Sách | Tác giả | Mượn ngày | Hạn trả | Trả ngày | Tiền phạt\n"
        text += "-" * 60 + "\n"
        
        for idx, record in enumerate(borrow_records, 1):
            return_date = record.return_date.strftime('%d/%m/%Y') if record.return_date else 'Chưa trả'
            late_fee = f"{record.late_fee:,.0f} VND" if record.late_fee > 0 else '-'
            
            text += f"{idx} | {record.book.title[:15]} | {record.book.author[:10]} | "
            text += f"{record.borrow_date.strftime('%d/%m/%Y')} | "
            text += f"{record.due_date.strftime('%d/%m/%Y')} | {return_date} | {late_fee}\n"
    else:
        text += "Không có bản ghi mượn sách.\n"
    
    text += "\n" + "=" * 60 + "\n"
    text += "Lưu ý: PDF đầy đủ yêu cầu cài đặt ReportLab\n"
    text += "Để sử dụng: pip install reportlab\n"
    
    return text.encode()
def generate_statistics_report_pdf(stats):
    """Generate PDF report for library statistics - STUB version"""
    text = "BÁO CÁO THỐNG KÊ THƯ VIỆN\n"
    text += "=" * 60 + "\n\n"
    
    text += f"Ngày báo cáo: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    text += "THỐNG KÊ CHUNG:\n"
    text += "-" * 60 + "\n"
    text += f"Tổng số sách: {stats.get('total_books', 0)}\n"
    text += f"Sách sẵn có: {stats.get('available_books', 0)}\n"
    text += f"Sách đang mượn: {stats.get('borrowed_books', 0)}\n"
    text += f"Tổng độc giả: {stats.get('total_users', 0)}\n"
    text += f"Sách quá hạn: {stats.get('overdue_books', 0)}\n"
    
    text += "\n" + "=" * 60 + "\n"
    text += "Lưu ý: PDF đầy đủ yêu cầu cài đặt ReportLab\n"
    text += "Để sử dụng: pip install reportlab\n"
    
    return text.encode()
