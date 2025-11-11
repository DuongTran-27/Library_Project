#!/usr/bin/env python
"""Create sample data for testing"""

from app import create_app, db
from models import User, Book, Category
from datetime import datetime

app = create_app()
ctx = app.app_context()
ctx.push()

# Create categories
categories_data = [
    {'name': 'Văn học', 'description': 'Sách văn học tiểu thuyết'},
    {'name': 'Công nghệ', 'description': 'Sách về công nghệ, lập trình'},
    {'name': 'Kinh tế', 'description': 'Sách về kinh tế, quản lý'},
    {'name': 'Lịch sử', 'description': 'Sách về lịch sử, tiểu sử'},
    {'name': 'Tự phát triển', 'description': 'Sách về phát triển bản thân'},
]

categories = []
for cat_data in categories_data:
    existing = Category.query.filter_by(name=cat_data['name']).first()
    if not existing:
        cat = Category(name=cat_data['name'], description=cat_data['description'])
        categories.append(cat)
        db.session.add(cat)

db.session.commit()
print(f"✓ Categories ready ({len(categories)} new ones added)")

# Create sample books
books_data = [
    {
        'title': 'Nhà Giả Kim',
        'author': 'Paulo Coelho',
        'isbn': '978-8501920789',
        'year': 2006,
        'quantity': 5,
        'category': 'Văn học'
    },
    {
        'title': 'Lập trình Python',
        'author': 'Mark Summerfield',
        'isbn': '978-0132269360',
        'year': 2009,
        'quantity': 3,
        'category': 'Công nghệ'
    },
    {
        'title': 'Giàu có và tự do tài chính',
        'author': 'Robert Kiyosaki',
        'isbn': '978-0944991344',
        'year': 1997,
        'quantity': 4,
        'category': 'Kinh tế'
    },
]

for book_data in books_data:
    category = Category.query.filter_by(name=book_data['category']).first()
    book = Book(
        title=book_data['title'],
        author=book_data['author'],
        isbn=book_data['isbn'],
        published_year=book_data['year'],
        total_copies=book_data['quantity'],
        available_copies=book_data['quantity']
    )
    book.categories.append(category)
    db.session.add(book)

db.session.commit()
print(f"✓ Created {len(books_data)} sample books")

print("\n✓ Sample data created successfully!")
print("  - 5 categories")
print("  - 3 sample books")
print("  - Ready for testing!")
