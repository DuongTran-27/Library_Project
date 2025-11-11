#!/usr/bin/env python
"""Create admin account"""

from app import create_app, db
from models import User

app = create_app()
ctx = app.app_context()
ctx.push()

# Check if admin already exists
existing = User.query.filter_by(username='admin').first()
if existing:
    print("✓ Admin account already exists!")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: admin@library.local")
else:
    # Create admin user
    admin = User(
        username='admin',
        email='admin@library.local',
        full_name='Administrator',
        is_admin=True,
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    print('✓ Admin account created successfully!')
    print('  Username: admin')
    print('  Password: admin123')
    print('  Email: admin@library.local')
