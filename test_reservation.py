#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test reservation functionality"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime, timedelta
from app import create_app, db
from models import User, Book, BorrowRecord, Reservation
from config import Config

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    print("="*60)
    print("TESTING RESERVATION FUNCTIONALITY")
    print("="*60)
    
    # Get test data
    admin = User.query.filter_by(username='admin').first()
    book = Book.query.first()
    
    # Create test users
    print("\n1. Creating test users...")
    user1 = User.query.filter_by(username='user1').first()
    if not user1:
        user1 = User(
            username='user1',
            email='user1@test.local',
            full_name='User One',
            is_admin=False
        )
        user1.set_password('pass123')
        db.session.add(user1)
    
    user2 = User.query.filter_by(username='user2').first()
    if not user2:
        user2 = User(
            username='user2',
            email='user2@test.local',
            full_name='User Two',
            is_admin=False
        )
        user2.set_password('pass123')
        db.session.add(user2)
    
    user3 = User.query.filter_by(username='user3').first()
    if not user3:
        user3 = User(
            username='user3',
            email='user3@test.local',
            full_name='User Three',
            is_admin=False
        )
        user3.set_password('pass123')
        db.session.add(user3)
    
    db.session.commit()
    print("[OK] Created test users: user1, user2, user3")
    
    # Create a borrow record
    print("\n2. Creating borrow record...")
    book = Book.query.first()
    print(f"   Book: {book.title}")
    print(f"   Available copies: {book.available_copies}")
    
    # Create borrow for user1
    borrow1 = BorrowRecord.query.filter_by(user_id=user1.id, book_id=book.id, return_date=None).first()
    if not borrow1:
        borrow1 = BorrowRecord(
            user_id=user1.id,
            book_id=book.id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )
        book.available_copies -= 1
        db.session.add(borrow1)
        db.session.commit()
        print(f"[OK] User1 borrowed book (ID: {borrow1.id})")
        print(f"   Available copies now: {book.available_copies}")
    
    # Create reservations
    print("\n3. Creating reservations...")
    
    # User2 reserves
    res2 = Reservation.query.filter_by(user_id=user2.id, book_id=book.id, status='waiting').first()
    if not res2:
        res2 = Reservation(user_id=user2.id, book_id=book.id, status='waiting')
        db.session.add(res2)
        print(f"[OK] User2 reserved book (status: waiting)")
    
    # User3 reserves
    res3 = Reservation.query.filter_by(user_id=user3.id, book_id=book.id, status='waiting').first()
    if not res3:
        res3 = Reservation(user_id=user3.id, book_id=book.id, status='waiting')
        db.session.add(res3)
        print(f"[OK] User3 reserved book (status: waiting)")
    
    db.session.commit()
    
    # Show reservation queue
    print("\n4. Current reservation queue:")
    reservations = Reservation.query.filter_by(book_id=book.id, status='waiting').order_by(Reservation.reserved_at.asc()).all()
    for i, res in enumerate(reservations, 1):
        print(f"   Position {i}: {res.user.full_name} ({res.reserved_at.strftime('%H:%M:%S')})")
    
    # Simulate return book
    print("\n5. Simulating book return by User1...")
    print(f"   Before return:")
    print(f"   - Borrow record return_date: {borrow1.return_date}")
    print(f"   - Available copies: {book.available_copies}")
    
    # This is what happens when user returns book
    borrow1.return_date = datetime.utcnow()
    borrow1.late_fee = 0  # No late fee
    
    # Check for waiting reservations
    first_reservation = Reservation.query.filter_by(
        book_id=book.id,
        status='waiting'
    ).order_by(Reservation.reserved_at.asc()).first()
    
    if first_reservation:
        # Cancel existing notified if any
        existing_notified = Reservation.query.filter_by(
            book_id=book.id,
            status='notified'
        ).first()
        
        if existing_notified:
            existing_notified.status = 'cancelled'
            print(f"   [OK] Cancelled existing notified: {existing_notified.user.full_name}")
        
        # Set first in queue as notified
        first_reservation.status = 'notified'
        print(f"   [OK] Notified: {first_reservation.user.full_name}")
    else:
        book.available_copies += 1
        print(f"   [OK] No reservations, increased available copies")
    
    db.session.commit()
    
    print(f"\n   After return:")
    print(f"   - Borrow record return_date: {borrow1.return_date}")
    print(f"   - Available copies: {book.available_copies}")
    
    # Show updated queue
    print("\n6. Updated reservation status:")
    all_res = Reservation.query.filter_by(book_id=book.id).order_by(Reservation.reserved_at.asc()).all()
    for res in all_res:
        print(f"   {res.user.full_name}: {res.status}")
    
    print("\n" + "="*60)
    print("[SUCCESS] TEST COMPLETE - No PendingRollbackError!")
    print("="*60)
