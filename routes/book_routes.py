"""Book management routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db, Book, Category, BorrowRecord, Reservation
from routes.auth_routes import login_required, admin_required
from datetime import datetime, timedelta

book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.route('/')
def index():
    """Book list with search and filter"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category', 0, type=int)
    
    query = Book.query
    
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%')) |
            (Book.isbn.ilike(f'%{search}%'))
        )
    
    if category_id > 0:
        query = query.filter(Book.categories.any(id=category_id))
    
    books = query.paginate(page=page, per_page=10)
    categories = Category.query.all()
    
    return render_template('book/index.html', books=books, categories=categories, 
                         search=search, category_id=category_id)

@book_bp.route('/detail/<int:book_id>')
def detail(book_id):
    """Book detail page"""
    book = Book.query.get_or_404(book_id)
    user_reservation = None
    
    if current_user.is_authenticated:
        user_reservation = Reservation.query.filter_by(
            user_id=current_user.id, 
            book_id=book_id,
            status='waiting'
        ).first()
    
    return render_template('book/detail.html', book=book, user_reservation=user_reservation)

@book_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new book (Admin only)"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        published_year = request.form.get('published_year', type=int)
        description = request.form.get('description')
        total_copies = request.form.get('total_copies', 1, type=int)
        category_ids = request.form.getlist('categories')
        
        if not all([title, author]):
            flash('Tên sách và tác giả là bắt buộc.', 'danger')
            return redirect(url_for('book.create'))
        
        if isbn and Book.query.filter_by(isbn=isbn).first():
            flash('ISBN này đã tồn tại.', 'danger')
            return redirect(url_for('book.create'))
        
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publisher=publisher,
            published_year=published_year,
            description=description,
            total_copies=total_copies,
            available_copies=total_copies
        )
        
        for cat_id in category_ids:
            category = Category.query.get(cat_id)
            if category:
                book.categories.append(category)
        
        db.session.add(book)
        db.session.commit()
        
        flash(f'Sách "{title}" đã được thêm thành công.', 'success')
        return redirect(url_for('book.detail', book_id=book.id))
    
    categories = Category.query.all()
    return render_template('book/create.html', categories=categories)

@book_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit(book_id):
    """Edit book (Admin only)"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form.get('title', book.title)
        book.author = request.form.get('author', book.author)
        book.publisher = request.form.get('publisher', book.publisher)
        book.published_year = request.form.get('published_year', book.published_year, type=int)
        book.description = request.form.get('description', book.description)
        book.total_copies = request.form.get('total_copies', book.total_copies, type=int)
        
        # Update categories
        category_ids = request.form.getlist('categories')
        book.categories.clear()
        for cat_id in category_ids:
            category = Category.query.get(cat_id)
            if category:
                book.categories.append(category)
        
        db.session.commit()
        flash('Sách đã được cập nhật thành công.', 'success')
        return redirect(url_for('book.detail', book_id=book.id))
    
    categories = Category.query.all()
    return render_template('book/edit.html', book=book, categories=categories)

@book_bp.route('/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete(book_id):
    """Delete book (Admin only)"""
    book = Book.query.get_or_404(book_id)
    title = book.title
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Sách "{title}" đã được xóa.', 'success')
    return redirect(url_for('book.index'))

@book_bp.route('/reserve/<int:book_id>', methods=['POST'])
@login_required
def reserve(book_id):
    """Reserve book"""
    book = Book.query.get_or_404(book_id)
    
    if book.available_copies > 0:
        flash('Sách này vẫn còn sẵn, bạn có thể mượn trực tiếp.', 'info')
        return redirect(url_for('book.detail', book_id=book_id))
    
    existing = Reservation.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        status='waiting'
    ).first()
    
    if existing:
        flash('Bạn đã đặt trước sách này rồi.', 'warning')
        return redirect(url_for('book.detail', book_id=book_id))
    
    reservation = Reservation(user_id=current_user.id, book_id=book_id, status='waiting')
    db.session.add(reservation)
    db.session.commit()
    
    flash('Đặt trước sách thành công!', 'success')
    return redirect(url_for('book.detail', book_id=book_id))

@book_bp.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    """Cancel reservation"""
    reservation = Reservation.query.get_or_404(reservation_id)
    
    if reservation.user_id != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền hủy đặt trước này.', 'danger')
        return redirect(url_for('book.index'))
    
    book_id = reservation.book_id
    db.session.delete(reservation)
    db.session.commit()
    
    flash('Hủy đặt trước thành công.', 'success')
    return redirect(url_for('book.detail', book_id=book_id))
