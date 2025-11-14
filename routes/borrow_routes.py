"""Borrowing and returning routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db, BorrowRecord, Book, Reservation, User
from routes.auth_routes import login_required, admin_required
from services.email_service import send_borrow_confirmation, send_return_confirmation
from datetime import datetime, timedelta
from config import Config

borrow_bp = Blueprint('borrow', __name__, url_prefix='/borrow')

@borrow_bp.route('/my-books')
@login_required
def my_books():
    """View user's borrowed books"""
    page = request.args.get('page', 1, type=int)
    
    # Active borrows
    active_borrows = current_user.borrow_records.filter_by(return_date=None).paginate(
        page=page, per_page=10
    )
    
    # Calculate late fees for active borrows
    total_late_fee = 0
    for record in active_borrows.items:
        if record.is_overdue():
            record.late_fee = record.calculate_late_fee(Config.LATE_FEE_PER_DAY)
            total_late_fee += record.late_fee
    
    return render_template('borrow/my_books.html', borrows=active_borrows, 
                         total_late_fee=total_late_fee)

@borrow_bp.route('/history')
@login_required
def history():
    """View user's borrow history"""
    page = request.args.get('page', 1, type=int)
    
    history = current_user.borrow_records.filter(
        BorrowRecord.return_date.isnot(None)
    ).order_by(BorrowRecord.return_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('borrow/history.html', history=history)

@borrow_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow(book_id):
    """Borrow book"""
    book = Book.query.get_or_404(book_id)
    
    # Check if book is available
    if not book.is_available():
        flash('Sách này hiện không sẵn có.', 'warning')
        return redirect(url_for('book.detail', book_id=book_id))
    
    # Check max borrow limit
    active_count = current_user.borrow_records.filter_by(return_date=None).count()
    if active_count >= Config.MAX_BORROW_BOOKS:
        flash(f'Bạn đã đạt tới giới hạn mượn {Config.MAX_BORROW_BOOKS} sách.', 'danger')
        return redirect(url_for('borrow.my_books'))
    
    # Check overdue books
    overdue = current_user.borrow_records.filter(
        BorrowRecord.return_date.isnot(None) == False,
        BorrowRecord.due_date < datetime.utcnow()
    ).first()
    
    if overdue:
        flash('Bạn có sách quá hạn. Vui lòng trả sách trước khi mượn sách khác.', 'warning')
        return redirect(url_for('borrow.my_books'))
    
    # Create borrow record
    due_date = datetime.utcnow() + timedelta(days=Config.BORROW_DURATION_DAYS)
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date
    )
    
    # Decrease available copies
    book.available_copies -= 1
    
    db.session.add(borrow_record)
    db.session.commit()
    
    # Send confirmation email
    try:
        send_borrow_confirmation(current_user, book, due_date)
    except Exception as e:
        print(f"Error sending email: {e}")
    
    # Check for reservations
    reservations = Reservation.query.filter_by(book_id=book_id, status='waiting').all()
    if reservations:
        for res in reservations[:1]:  # Notify first person in queue
            res.status = 'notified'
        db.session.commit()
    
    flash(f'Mượn sách "{book.title}" thành công! Hạn trả: {due_date.strftime("%d/%m/%Y")}', 'success')
    return redirect(url_for('borrow.my_books'))

@borrow_bp.route('/return/<int:record_id>', methods=['POST'])
@login_required
def return_book(record_id):
    """Return book"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.user_id != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền trả sách này.', 'danger')
        return redirect(url_for('borrow.my_books'))
    
    if record.return_date is not None:
        flash('Sách này đã được trả rồi.', 'warning')
        return redirect(url_for('borrow.my_books'))
    
    # Calculate late fee
    late_fee = record.calculate_late_fee(Config.LATE_FEE_PER_DAY)
    
    # Update return record
    record.return_date = datetime.utcnow()
    record.late_fee = late_fee
    
    # Check for waiting reservations (first in queue by reserved_at)
    first_reservation = Reservation.query.filter_by(
        book_id=record.book_id,
        status='waiting'
    ).order_by(Reservation.reserved_at.asc()).first()
    
    if first_reservation:
        # AUTO-BORROW: Create borrow record for first person in queue
        due_date = datetime.utcnow() + timedelta(days=Config.BORROW_DURATION_DAYS)
        auto_borrow = BorrowRecord(
            user_id=first_reservation.user_id,
            book_id=record.book_id,
            due_date=due_date,
            notes='Tự động mượn từ đặt trước'
        )
        
        # Mark reservation as fulfilled
        first_reservation.status = 'fulfilled'
        
        db.session.add(auto_borrow)
        db.session.commit()
        
        # Send confirmation email to reserved user
        try:
            send_borrow_confirmation(first_reservation.user, record.book, due_date)
        except Exception as e:
            print(f"Error sending email: {e}")
        
        # Check for next person in queue
        next_reservation = Reservation.query.filter_by(
            book_id=record.book_id,
            status='waiting'
        ).order_by(Reservation.reserved_at.asc()).first()
        
        if next_reservation:
            # Notify next person
            next_reservation.status = 'notified'
            db.session.commit()
            
            try:
                from services.email_service import send_reservation_ready_notification
                send_reservation_ready_notification(next_reservation.user, record.book)
            except Exception as e:
                print(f"Error sending email: {e}")
    else:
        # No one waiting, increase available copies
        record.book.available_copies += 1
        db.session.commit()
    
    # Send return confirmation email
    try:
        send_return_confirmation(current_user, record.book)
    except Exception as e:
        print(f"Error sending email: {e}")
    
    # Show messages
    if first_reservation:
        flash(f'Sách "{record.book.title}" đã được trả thành công.', 'success')
        flash(f'{first_reservation.user.full_name} tự động được nhận sách và đã được gửi thông báo.', 'info')
        if next_res := Reservation.query.filter_by(
            book_id=record.book_id,
            status='notified'
        ).first():
            flash(f'Người tiếp theo ({next_res.user.full_name}) đang chờ trong hàng.', 'info')
        if late_fee > 0:
            flash(f'Tiền phạt: {late_fee:,.0f} VND', 'warning')
    else:
        flash(f'Sách "{record.book.title}" đã được trả thành công.', 'success')
        if late_fee > 0:
            flash(f'Tiền phạt: {late_fee:,.0f} VND', 'warning')
    
    return redirect(url_for('borrow.my_books'))

@borrow_bp.route('/renew/<int:record_id>', methods=['POST'])
@login_required
def renew(record_id):
    """Renew borrowed book"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.user_id != current_user.id:
        flash('Bạn không có quyền gia hạn sách này.', 'danger')
        return redirect(url_for('borrow.my_books'))
    
    if record.return_date is not None:
        flash('Bạn chỉ có thể gia hạn sách chưa trả.', 'warning')
        return redirect(url_for('borrow.my_books'))
    
    # Check if overdue
    if record.is_overdue():
        flash('Bạn không thể gia hạn sách quá hạn.', 'danger')
        return redirect(url_for('borrow.my_books'))
    
    # Check if already renewed (max 1 renewal)
    if (record.due_date - record.borrow_date).days > Config.BORROW_DURATION_DAYS:
        flash('Bạn chỉ được gia hạn một lần.', 'warning')
        return redirect(url_for('borrow.my_books'))
    
    # Renew
    record.due_date = record.due_date + timedelta(days=Config.BORROW_DURATION_DAYS)
    db.session.commit()
    
    flash(f'Gia hạn sách "{record.book.title}" thành công! Hạn trả mới: {record.due_date.strftime("%d/%m/%Y")}', 'success')
    return redirect(url_for('borrow.my_books'))

@borrow_bp.route('/admin/borrow/<int:user_id>/<int:book_id>', methods=['POST'])
@admin_required
def admin_borrow(user_id, book_id):
    """Admin borrow book for user"""
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)
    
    if not book.is_available():
        flash('Sách này hiện không sẵn có.', 'warning')
        return redirect(url_for('admin.users'))
    
    due_date = datetime.utcnow() + timedelta(days=Config.BORROW_DURATION_DAYS)
    borrow_record = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        due_date=due_date
    )
    
    book.available_copies -= 1
    db.session.add(borrow_record)
    db.session.commit()
    
    flash(f'Mượn sách cho {user.full_name} thành công!', 'success')
    return redirect(url_for('admin.users'))

@borrow_bp.route('/admin/return/<int:record_id>', methods=['POST'])
@admin_required
def admin_return(record_id):
    """Admin return book for user"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.return_date is not None:
        flash('Sách này đã được trả rồi.', 'warning')
        return redirect(url_for('admin.users'))
    
    late_fee = record.calculate_late_fee(Config.LATE_FEE_PER_DAY)
    
    record.return_date = datetime.utcnow()
    record.late_fee = late_fee
    
    # Check for waiting reservations (first in queue by reserved_at)
    first_reservation = Reservation.query.filter_by(
        book_id=record.book_id,
        status='waiting'
    ).order_by(Reservation.reserved_at.asc()).first()
    
    if first_reservation:
        # AUTO-BORROW: Create borrow record for first person in queue
        due_date = datetime.utcnow() + timedelta(days=Config.BORROW_DURATION_DAYS)
        auto_borrow = BorrowRecord(
            user_id=first_reservation.user_id,
            book_id=record.book_id,
            due_date=due_date,
            notes='Tự động mượn từ đặt trước'
        )
        
        # Mark reservation as fulfilled
        first_reservation.status = 'fulfilled'
        
        db.session.add(auto_borrow)
        db.session.commit()
        
        # Send confirmation email to reserved user
        try:
            send_borrow_confirmation(first_reservation.user, record.book, due_date)
        except Exception as e:
            print(f"Error sending email: {e}")
        
        # Check for next person in queue
        next_reservation = Reservation.query.filter_by(
            book_id=record.book_id,
            status='waiting'
        ).order_by(Reservation.reserved_at.asc()).first()
        
        if next_reservation:
            # Notify next person
            next_reservation.status = 'notified'
            db.session.commit()
            
            try:
                from services.email_service import send_reservation_ready_notification
                send_reservation_ready_notification(next_reservation.user, record.book)
            except Exception as e:
                print(f"Error sending email: {e}")
            
            flash(f'Trả sách cho {record.user.full_name} thành công!', 'success')
            flash(f'{first_reservation.user.full_name} tự động được nhận sách và đã được gửi thông báo.', 'info')
            flash(f'Người tiếp theo ({next_reservation.user.full_name}) đang chờ trong hàng.', 'info')
        else:
            flash(f'Trả sách cho {record.user.full_name} thành công!', 'success')
            flash(f'{first_reservation.user.full_name} tự động được nhận sách và đã được gửi thông báo.', 'info')
    else:
        # No one waiting, increase available copies
        record.book.available_copies += 1
        flash(f'Trả sách cho {record.user.full_name} thành công!', 'success')
    
    db.session.commit()
    
    return redirect(url_for('admin.users'))
