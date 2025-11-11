"""Admin routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, Book, Category, BorrowRecord, Reservation
from routes.auth_routes import admin_required
from services.pdf_service import generate_statistics_report_pdf, generate_borrow_report_pdf
from datetime import datetime, timedelta
from sqlalchemy import func
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    # Calculate statistics
    total_books = Book.query.count()
    available_books = db.session.query(func.sum(Book.available_copies)).scalar() or 0
    borrowed_books = db.session.query(func.sum(
        Book.total_copies - Book.available_copies
    )).scalar() or 0
    
    total_users = User.query.filter_by(is_admin=False).count()
    overdue_books = BorrowRecord.query.filter(
        BorrowRecord.return_date.is_(None),
        BorrowRecord.due_date < datetime.utcnow()
    ).count()
    
    # Most borrowed books
    most_borrowed = db.session.query(
        Book,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord).group_by(Book.id).order_by(
        func.count(BorrowRecord.id).desc()
    ).limit(5).all()
    
    # Active readers
    active_readers = db.session.query(
        User,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord).filter(User.is_admin == False).group_by(
        User.id
    ).order_by(func.count(BorrowRecord.id).desc()).limit(5).all()
    
    stats = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_users': total_users,
        'overdue_books': overdue_books,
        'most_borrowed': [(b[0], b[1]) for b in most_borrowed],
        'active_readers': [(u[0], u[1]) for u in active_readers]
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query.filter_by(is_admin=False)
    
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    users = query.paginate(page=page, per_page=10)
    
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route('/user/<int:user_id>')
@admin_required
def user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    
    active_borrows = user.borrow_records.filter_by(return_date=None).all()
    borrow_history = user.borrow_records.filter(
        BorrowRecord.return_date.isnot(None)
    ).order_by(BorrowRecord.return_date.desc()).limit(10).all()
    
    return render_template('admin/user_detail.html', 
                         user=user,
                         active_borrows=active_borrows,
                         borrow_history=borrow_history)

@admin_bp.route('/user/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Bạn không thể khóa tài khoản admin.', 'danger')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'được kích hoạt' if user.is_active else 'được khóa'
    flash(f'Tài khoản người dùng đã {status}.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))

@admin_bp.route('/categories')
@admin_required
def categories():
    """Manage categories"""
    page = request.args.get('page', 1, type=int)
    
    categories = Category.query.paginate(page=page, per_page=10)
    
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/category/create', methods=['GET', 'POST'])
@admin_required
def create_category():
    """Create category"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Tên thể loại là bắt buộc.', 'danger')
            return redirect(url_for('admin.create_category'))
        
        if Category.query.filter_by(name=name).first():
            flash('Thể loại này đã tồn tại.', 'danger')
            return redirect(url_for('admin.create_category'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'Thể loại "{name}" đã được tạo thành công.', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/create_category.html')

@admin_bp.route('/category/<int:cat_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_category(cat_id):
    """Edit category"""
    category = Category.query.get_or_404(cat_id)
    
    if request.method == 'POST':
        name = request.form.get('name', category.name)
        description = request.form.get('description', category.description)
        
        # Check for duplicate
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != cat_id:
            flash('Tên thể loại này đã được sử dụng.', 'danger')
            return redirect(url_for('admin.edit_category', cat_id=cat_id))
        
        category.name = name
        category.description = description
        db.session.commit()
        
        flash('Thể loại đã được cập nhật.', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/edit_category.html', category=category)

@admin_bp.route('/category/<int:cat_id>/delete', methods=['POST'])
@admin_required
def delete_category(cat_id):
    """Delete category"""
    category = Category.query.get_or_404(cat_id)
    name = category.name
    
    # Remove from books
    category.books.clear()
    db.session.delete(category)
    db.session.commit()
    
    flash(f'Thể loại "{name}" đã được xóa.', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/books')
@admin_required
def books():
    """Manage books"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Book.query
    
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%'))
        )
    
    books = query.paginate(page=page, per_page=10)
    
    return render_template('admin/books.html', books=books, search=search)

@admin_bp.route('/overdue-books')
@admin_required
def overdue_books():
    """View overdue books"""
    page = request.args.get('page', 1, type=int)
    
    overdue = BorrowRecord.query.filter(
        BorrowRecord.return_date.is_(None),
        BorrowRecord.due_date < datetime.utcnow()
    ).order_by(BorrowRecord.due_date.asc()).paginate(page=page, per_page=10)
    
    return render_template('admin/overdue_books.html', overdue=overdue)

@admin_bp.route('/reservations')
@admin_required
def reservations():
    """Manage reservations"""
    page = request.args.get('page', 1, type=int)
    
    reservations = Reservation.query.paginate(page=page, per_page=10)
    
    return render_template('admin/reservations.html', reservations=reservations)

@admin_bp.route('/reports')
@admin_required
def reports():
    """Generate reports"""
    return render_template('admin/reports.html')

@admin_bp.route('/report/statistics')
@admin_required
def report_statistics():
    """Generate statistics PDF report"""
    total_books = Book.query.count()
    available_books = db.session.query(func.sum(Book.available_copies)).scalar() or 0
    borrowed_books = db.session.query(func.sum(
        Book.total_copies - Book.available_copies
    )).scalar() or 0
    total_users = User.query.filter_by(is_admin=False).count()
    overdue_books = BorrowRecord.query.filter(
        BorrowRecord.return_date.is_(None),
        BorrowRecord.due_date < datetime.utcnow()
    ).count()
    
    most_borrowed = db.session.query(
        Book.title,
        Book.author,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord).group_by(Book.id).order_by(
        func.count(BorrowRecord.id).desc()
    ).limit(10).all()
    
    active_readers = db.session.query(
        User.full_name,
        User.email,
        func.count(BorrowRecord.id).label('total_borrows'),
        func.sum((BorrowRecord.return_date.is_(None)).cast(db.Integer)).label('current_borrows')
    ).join(BorrowRecord).filter(User.is_admin == False).group_by(
        User.id
    ).order_by(func.count(BorrowRecord.id).desc()).limit(10).all()
    
    stats = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_users': total_users,
        'overdue_books': overdue_books,
        'most_borrowed_books': [
            {'title': b[0], 'author': b[1], 'borrow_count': b[2]} 
            for b in most_borrowed
        ],
        'active_readers': [
            {'name': r[0], 'email': r[1], 'total_borrows': r[2], 'current_borrows': r[3] or 0}
            for r in active_readers
        ]
    }
    
    pdf = generate_statistics_report_pdf(stats)
    
    from flask import send_file
    return send_file(
        pdf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"thong_ke_thu_vien_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
    )

@admin_bp.route('/report/user-borrow/<int:user_id>')
@admin_required
def report_user_borrow(user_id):
    """Generate user borrow history PDF"""
    user = User.query.get_or_404(user_id)
    borrow_records = user.borrow_records.all()
    
    pdf = generate_borrow_report_pdf(borrow_records, user)
    
    from flask import send_file
    return send_file(
        pdf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"lich_su_muon_{user.username}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
    )
