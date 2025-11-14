#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete test users"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import create_app, db
from models import User

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    print("="*60)
    print("DELETING TEST USERS")
    print("="*60)
    
    test_users = ['user1', 'user2', 'user3']
    deleted_count = 0
    
    for username in test_users:
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"[OK] Deleting user: {username}")
            db.session.delete(user)
            deleted_count += 1
        else:
            print(f"[SKIP] User not found: {username}")
    
    db.session.commit()
    
    print("\n" + "="*60)
    print(f"[SUCCESS] Deleted {deleted_count} test users")
    print("="*60)
    
    # Show remaining users
    print("\nRemaining users:")
    all_users = User.query.all()
    for user in all_users:
        role = "ADMIN" if user.is_admin else "USER"
        print(f"  - {user.username} ({user.email}) [{role}]")
    
    print("\n[INFO] You can now register new accounts to test the system!")
