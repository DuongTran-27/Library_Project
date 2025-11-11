"""Run Flask application"""
import os
from app import create_app, db
from models import User, Book, Category, BorrowRecord, Reservation
# from flask_migrate import Migrate  # Optional: uncomment if installed

app = create_app(os.getenv('FLASK_ENV', 'development'))
# migrate = Migrate(app, db)  # Optional: uncomment if flask_migrate installed

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Book': Book,
        'Category': Category,
        'BorrowRecord': BorrowRecord,
        'Reservation': Reservation
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized.")

@app.cli.command()
def create_admin():
    """Create admin user"""
    from werkzeug.security import generate_password_hash
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    if User.query.filter_by(username=username).first():
        print("User already exists!")
        return
    
    admin = User(
        username=username,
        email=email,
        full_name="Administrator",
        is_admin=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user '{username}' created successfully!")

@app.cli.command()
def create_sample_data():
    """Create sample data"""
    # Create categories
    categories = [
        Category(name="Tiểu thuyết", description="Những cuốn tiểu thuyết hấp dẫn"),
        Category(name="Lịch sử", description="Sách về lịch sử"),
        Category(name="Khoa học", description="Sách khoa học"),
        Category(name="Tự giáo dục", description="Sách tự giáo dục"),
        Category(name="Tâm lý", description="Sách về tâm lý"),
    ]
    
    for cat in categories:
        if not Category.query.filter_by(name=cat.name).first():
            db.session.add(cat)
    
    db.session.commit()
    
    # Create sample books
    books = [
        Book(
            title="Chiếc lá cuối cùng",
            author="O. Henry",
            isbn="978-0-12345-678-9",
            publisher="NXB Văn học",
            published_year=1905,
            description="Một câu chuyện cảm động về tình yêu và sự hy sinh",
            total_copies=5,
            available_copies=5
        ),
        Book(
            title="Nhà giả kim",
            author="Paulo Coelho",
            isbn="978-1-98765-432-1",
            publisher="NXB Thế giới",
            published_year=1988,
            description="Câu chuyện về một cậu bé tìm kiếm kho báu và phát hiện bản thân",
            total_copies=8,
            available_copies=8
        ),
        Book(
            title="Bắc Mỹ độc lập",
            author="Jacques Godechot",
            isbn="978-2-54321-876-5",
            publisher="NXB Giáo dục",
            published_year=1963,
            description="Nghiên cứu chi tiết về Cách mạng Mỹ",
            total_copies=3,
            available_copies=3
        ),
    ]
    
    for book in books:
        if not Book.query.filter_by(isbn=book.isbn).first():
            db.session.add(book)
    
    db.session.commit()
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
