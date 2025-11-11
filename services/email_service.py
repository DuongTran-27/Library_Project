from flask_mail import Mail, Message
from datetime import datetime, timedelta
from config import Config

mail = Mail()

def send_email(subject, recipients, text_body=None, html_body=None):
    """Send email"""
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_overdue_reminder(user, borrow_records):
    """Send overdue reminder email"""
    subject = "[Thư viện] Nhắc nhở: Sách quá hạn trả"
    
    overdue_books = []
    for record in borrow_records:
        if record.is_overdue():
            late_fee = record.calculate_late_fee()
            overdue_books.append({
                'title': record.book.title,
                'author': record.book.author,
                'due_date': record.due_date.strftime('%d/%m/%Y'),
                'days_overdue': (datetime.utcnow() - record.due_date).days,
                'late_fee': f"{late_fee:,.0f} VND"
            })
    
    html_body = f"""
    <html>
    <head></head>
    <body>
        <h2>Nhắc nhở trả sách quá hạn</h2>
        <p>Xin chào {user.full_name},</p>
        <p>Bạn có những cuốn sách sau đây đã quá hạn trả:</p>
        <table border="1" cellpadding="10">
            <tr>
                <th>Tên sách</th>
                <th>Tác giả</th>
                <th>Hạn trả</th>
                <th>Quá hạn (ngày)</th>
                <th>Tiền phạt</th>
            </tr>
    """
    
    for book in overdue_books:
        html_body += f"""
            <tr>
                <td>{book['title']}</td>
                <td>{book['author']}</td>
                <td>{book['due_date']}</td>
                <td>{book['days_overdue']}</td>
                <td>{book['late_fee']}</td>
            </tr>
        """
    
    html_body += """
        </table>
        <p>Vui lòng trả sách sớm để tránh tiền phạt tăng thêm.</p>
        <p>Trân trọng,<br>Hệ thống Quản lý Thư viện</p>
    </body>
    </html>
    """
    
    send_email(subject, [user.email], html_body=html_body)

def send_reservation_notification(user, book):
    """Send email when reserved book is available"""
    subject = f"[Thư viện] Sách '{book.title}' sẵn sàng để mượn"
    
    html_body = f"""
    <html>
    <head></head>
    <body>
        <h2>Sách bạn đặt trước đã sẵn sàng</h2>
        <p>Xin chào {user.full_name},</p>
        <p>Cuốn sách <strong>{book.title}</strong> của tác giả <strong>{book.author}</strong> 
        mà bạn đã đặt trước hiện đã sẵn sàng để mượn.</p>
        <p>Vui lòng đến thư viện để mượn sách trong vòng 3 ngày.</p>
        <p>Trân trọng,<br>Hệ thống Quản lý Thư viện</p>
    </body>
    </html>
    """
    
    send_email(subject, [user.email], html_body=html_body)

def send_borrow_confirmation(user, book, due_date):
    """Send borrow confirmation email"""
    subject = f"[Thư viện] Xác nhận mượn sách: {book.title}"
    
    html_body = f"""
    <html>
    <head></head>
    <body>
        <h2>Xác nhận mượn sách</h2>
        <p>Xin chào {user.full_name},</p>
        <p>Bạn vừa mượn cuốn sách sau:</p>
        <ul>
            <li><strong>Tên sách:</strong> {book.title}</li>
            <li><strong>Tác giả:</strong> {book.author}</li>
            <li><strong>Hạn trả:</strong> {due_date.strftime('%d/%m/%Y')}</li>
        </ul>
        <p>Vui lòng trả sách đúng hạn để tránh tiền phạt.</p>
        <p>Trân trọng,<br>Hệ thống Quản lý Thư viện</p>
    </body>
    </html>
    """
    
    send_email(subject, [user.email], html_body=html_body)

def send_return_confirmation(user, book):
    """Send return confirmation email"""
    subject = f"[Thư viện] Xác nhận trả sách: {book.title}"
    
    html_body = f"""
    <html>
    <head></head>
    <body>
        <h2>Xác nhận trả sách</h2>
        <p>Xin chào {user.full_name},</p>
        <p>Bạn vừa trả cuốn sách sau:</p>
        <ul>
            <li><strong>Tên sách:</strong> {book.title}</li>
            <li><strong>Tác giả:</strong> {book.author}</li>
        </ul>
        <p>Cảm ơn bạn đã sử dụng dịch vụ của thư viện.</p>
        <p>Trân trọng,<br>Hệ thống Quản lý Thư viện</p>
    </body>
    </html>
    """
    
    send_email(subject, [user.email], html_body=html_body)
