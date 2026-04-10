import os
from flask import Flask, request, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from app.models import db, Admin

login_manager = LoginManager()
login_manager.login_view = 'admin_bp.login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول لهذه الصفحة'
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per hour"], storage_uri="memory://")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config.get('UPLOAD_FOLDER', ''), exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.catalog import catalog_bp
    from app.routes.rfq import rfq_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(catalog_bp, url_prefix='/ar/products')
    app.register_blueprint(rfq_bp, url_prefix='/rfq')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # Security & cache headers
    @app.after_request
    def add_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        if 'static' in request.path:
            response.headers['Cache-Control'] = 'public, max-age=604800'
        return response

    # Template context - make company info available globally
    @app.context_processor
    def inject_company_info():
        from app.models import CompanyInfo, Category, Brand
        info = {}
        try:
            for item in CompanyInfo.query.all():
                info[item.key] = item.value
        except Exception:
            pass

        categories = []
        brands = []
        try:
            categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
            brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()
        except Exception:
            pass

        return {
            'company_info': info,
            'nav_categories': categories,
            'nav_brands': brands,
            'config': app.config
        }

    return app
