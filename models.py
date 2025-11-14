from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association table for many-to-many relationship between books and categories
book_category = db.Table('book_category',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# Association table for book reservations
class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_active_borrows(self):
        """Get active borrow records"""
        return self.borrow_records.filter_by(return_date=None).all()
    
    def get_overdue_count(self):
        """Get count of overdue books"""
        return self.borrow_records.filter(
            BorrowRecord.return_date.is_(None),
            BorrowRecord.due_date < datetime.utcnow()
        ).count()
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    """Book model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(120))
    published_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    cover_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', secondary=book_category, backref='books', lazy='dynamic')
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    def is_available(self):
        """Check if book is available for borrowing"""
        return self.available_copies > 0
    
    def get_wait_list_count(self):
        """Get number of users waiting for this book"""
        return self.reservations.filter_by(status='waiting').count()
    
    def __repr__(self):
        return f'<Book {self.title}>'


class Category(db.Model):
    """Book category model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class BorrowRecord(db.Model):
    """Record of book borrowing"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    due_date = db.Column(db.DateTime, nullable=False, index=True)
    return_date = db.Column(db.DateTime)
    late_fee = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_overdue(self):
        """Check if book is overdue"""
        if self.return_date is None:
            return datetime.utcnow() > self.due_date
        return False
    
    def calculate_late_fee(self, fee_per_day=5000):
        """Calculate late fee in VND"""
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * fee_per_day
        elif self.return_date is None and datetime.utcnow() > self.due_date:
            days_late = (datetime.utcnow() - self.due_date).days
            return days_late * fee_per_day
        return 0
    
    def get_days_remaining(self):
        """Get days until due date"""
        if self.return_date is None:
            return (self.due_date - datetime.utcnow()).days
        return 0
    
    def __repr__(self):
        return f'<BorrowRecord user={self.user_id} book={self.book_id}>'


class Reservation(db.Model):
    """Book reservation model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='waiting')  # waiting, notified, cancelled, fulfilled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Create a composite index for better query performance
    __table_args__ = (
        db.Index('ix_user_book_status', 'user_id', 'book_id', 'status'),
    )
    
    def __repr__(self):
        return f'<Reservation user={self.user_id} book={self.book_id}>'
