#!/usr/bin/env python
"""Initialize fresh database"""
import os
import sys
from app import create_app, db
from models import User, Book, Category, BorrowRecord, Reservation

# Create app
app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("✓ Database initialized successfully!")
    
    # Create admin user
    print("\nCreating admin user...")
    admin = User(
        username='admin',
        email='admin@library.local',
        full_name='Administrator',
        is_admin=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print("✓ Admin user created: admin/admin123")
    
    # Create sample categories
    print("\nCreating sample categories...")
    categories = [
        Category(name='Kỹ thuật', description='Sách về kỹ thuật và công nghệ'),
        Category(name='Tiểu thuyết', description='Các tiểu thuyết văn học'),
        Category(name='Lịch sử', description='Sách về lịch sử'),
        Category(name='Khoa học', description='Sách về khoa học'),
        Category(name='Tự truyện', description='Sách tự truyện'),
    ]
    
    for cat in categories:
        existing = Category.query.filter_by(name=cat.name).first()
        if not existing:
            db.session.add(cat)
    
    db.session.commit()
    print(f"✓ Created {len(categories)} categories")
    
    # Create sample books
    print("\nCreating sample books...")
    tech_cat = Category.query.filter_by(name='Kỹ thuật').first()
    novel_cat = Category.query.filter_by(name='Tiểu thuyết').first()
    history_cat = Category.query.filter_by(name='Lịch sử').first()
    
    books = [
        Book(
            title='Python Programming',
            author='Mark Lutz',
            isbn='978-1449355739',
            publisher='O\'Reilly',
            published_year=2013,
            description='Comprehensive Python book',
            total_copies=3,
            available_copies=3
        ),
        Book(
            title='Rừng Na Uy',
            author='Haruki Murakami',
            isbn='978-4103206109',
            publisher='Shinchosa',
            published_year=1987,
            description='Modern classic novel',
            total_copies=2,
            available_copies=2
        ),
        Book(
            title='Lịch Sử Việt Nam',
            author='Trần Văn Giáp',
            isbn='978-8481410778',
            publisher='NXB Khoa Học Xã Hội',
            published_year=1998,
            description='Vietnamese history',
            total_copies=2,
            available_copies=2
        ),
    ]
    
    for book in books:
        existing = Book.query.filter_by(isbn=book.isbn).first()
        if not existing:
            if 'Python' in book.title and tech_cat:
                book.categories.append(tech_cat)
            elif 'Rừng' in book.title and novel_cat:
                book.categories.append(novel_cat)
            elif 'Lịch' in book.title and history_cat:
                book.categories.append(history_cat)
            
            db.session.add(book)
    
    db.session.commit()
    print(f"✓ Created {len(books)} sample books")
    
    print("\n" + "="*50)
    print("✓ Database initialization complete!")
    print("="*50)
    print("\nYou can now start the application:")
    print("  venv/bin/python run.py")
    print("\nLogin with:")
    print("  Username: admin")
    print("  Password: admin123")
