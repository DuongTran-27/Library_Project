"""RESTful API routes"""
from flask import Blueprint, request, jsonify
from models import db, Book, User, BorrowRecord, Category
from routes.auth_routes import login_required
from flask_login import current_user
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/books', methods=['GET'])
def get_books():
    """Get books with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', 0, type=int)
    
    query = Book.query
    
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%'))
        )
    
    if category_id > 0:
        query = query.filter(Book.categories.any(id=category_id))
    
    books = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [{
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'isbn': b.isbn,
            'available_copies': b.available_copies,
            'total_copies': b.total_copies,
            'publisher': b.publisher,
            'published_year': b.published_year
        } for b in books.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': books.total,
            'pages': books.pages
        }
    })

@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get book details"""
    book = Book.query.get_or_404(book_id)
    
    return jsonify({
        'success': True,
        'data': {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publisher': book.publisher,
            'published_year': book.published_year,
            'description': book.description,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
            'categories': [{'id': c.id, 'name': c.name} for c in book.categories]
        }
    })

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in categories]
    })

@api_bp.route('/my-borrows', methods=['GET'])
@login_required
def get_my_borrows():
    """Get current user's borrowed books"""
    borrows = current_user.borrow_records.filter_by(return_date=None).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': b.id,
            'book_id': b.book_id,
            'book_title': b.book.title,
            'borrow_date': b.borrow_date.isoformat(),
            'due_date': b.due_date.isoformat(),
            'is_overdue': b.is_overdue(),
            'days_remaining': b.get_days_remaining(),
            'late_fee': b.calculate_late_fee()
        } for b in borrows]
    })

@api_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """Borrow book via API"""
    book = Book.query.get_or_404(book_id)
    
    if not book.is_available():
        return jsonify({
            'success': False,
            'message': 'Sách không sẵn có'
        }), 400
    
    # Check max borrow limit
    active_count = current_user.borrow_records.filter_by(return_date=None).count()
    if active_count >= 5:
        return jsonify({
            'success': False,
            'message': 'Bạn đã đạt tới giới hạn mượn sách'
        }), 400
    
    due_date = datetime.utcnow() + timedelta(days=14)
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date
    )
    
    book.available_copies -= 1
    db.session.add(borrow_record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Mượn sách thành công',
        'data': {
            'id': borrow_record.id,
            'book_id': book_id,
            'borrow_date': borrow_record.borrow_date.isoformat(),
            'due_date': borrow_record.due_date.isoformat()
        }
    }), 201

@api_bp.route('/return/<int:record_id>', methods=['POST'])
@login_required
def return_book(record_id):
    """Return book via API"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': 'Không có quyền trả sách này'
        }), 403
    
    if record.return_date is not None:
        return jsonify({
            'success': False,
            'message': 'Sách này đã được trả rồi'
        }), 400
    
    late_fee = record.calculate_late_fee()
    
    record.return_date = datetime.utcnow()
    record.late_fee = late_fee
    record.book.available_copies += 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Trả sách thành công',
        'data': {
            'id': record.id,
            'return_date': record.return_date.isoformat(),
            'late_fee': late_fee
        }
    })

@api_bp.route('/search', methods=['GET'])
def search():
    """Search books, authors, categories"""
    query = request.args.get('q', '', type=str)
    
    if not query or len(query) < 2:
        return jsonify({
            'success': False,
            'message': 'Query too short'
        }), 400
    
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%'))
    ).limit(10).all()
    
    categories = Category.query.filter(
        Category.name.ilike(f'%{query}%')
    ).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'books': [{
                'id': b.id,
                'title': b.title,
                'author': b.author,
                'type': 'book'
            } for b in books],
            'categories': [{
                'id': c.id,
                'name': c.name,
                'type': 'category'
            } for c in categories]
        }
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get library statistics"""
    total_books = Book.query.count()
    available_books = db.session.query(
        db.func.sum(Book.available_copies)
    ).scalar() or 0
    borrowed_books = db.session.query(
        db.func.sum(Book.total_copies - Book.available_copies)
    ).scalar() or 0
    
    return jsonify({
        'success': True,
        'data': {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books
        }
    })
