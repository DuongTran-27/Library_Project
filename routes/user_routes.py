"""User profile and account management routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db, User
from routes.auth_routes import login_required

user_bp = Blueprint('user', __name__, url_prefix='/profile')

@user_bp.route('/')
@login_required
def profile():
    """View user profile"""
    active_borrows = current_user.get_active_borrows()
    overdue_count = current_user.get_overdue_count()
    
    return render_template('user/profile.html', 
                         active_borrows=active_borrows,
                         overdue_count=overdue_count)

@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if not full_name:
            flash('Tên đầy đủ là bắt buộc.', 'danger')
            return redirect(url_for('user.edit_profile'))
        
        current_user.full_name = full_name
        current_user.phone = phone
        current_user.address = address
        db.session.commit()
        
        flash('Hồ sơ của bạn đã được cập nhật thành công.', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/edit_profile.html')

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Mật khẩu hiện tại không đúng.', 'danger')
            return redirect(url_for('user.change_password'))
        
        if len(new_password) < 6:
            flash('Mật khẩu mới phải có ít nhất 6 ký tự.', 'danger')
            return redirect(url_for('user.change_password'))
        
        if new_password != confirm_password:
            flash('Mật khẩu xác nhận không khớp.', 'danger')
            return redirect(url_for('user.change_password'))
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Mật khẩu của bạn đã được thay đổi thành công.', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/change_password.html')

@user_bp.route('/reservations')
@login_required
def reservations():
    """View user reservations"""
    page = request.args.get('page', 1, type=int)
    
    reservations = current_user.reservations.paginate(page=page, per_page=10)
    
    return render_template('user/reservations.html', reservations=reservations)
