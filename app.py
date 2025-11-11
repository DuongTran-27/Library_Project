"""Flask application factory"""
# Compatibility shim for Windows without C++ compiler
import markupsafe_compat

from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import config
from services.email_service import mail
import os

login_manager = LoginManager()

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.book_routes import book_bp
    from routes.borrow_routes import borrow_bp
    from routes.user_routes import user_bp
    from routes.admin_routes import admin_bp
    from routes.api_routes import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(borrow_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Default route - redirect to books
    @app.route('/')
    def index():
        """Default route redirects to books"""
        from flask import redirect, url_for
        return redirect(url_for('book.index'))
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
