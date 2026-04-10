import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sama-tech-dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "instance", "samatech.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    ALLOWED_DOC_EXTENSIONS = {'pdf'}
    MIN_IMAGE_WIDTH = 800
    MIN_IMAGE_HEIGHT = 600

    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@samatech-mea.com')

    # Company info
    COMPANY_NAME_AR = 'سما تكنولوجي'
    COMPANY_NAME_EN = 'Sama Technology'
    COMPANY_TAGLINE = 'Plug Into The Future'
    COMPANY_EMAIL = 'info@samatech-mea.com'
    COMPANY_PHONE_1 = '0556333171'
    COMPANY_PHONE_2 = '0556333601'
    COMPANY_WEBSITE = 'www.samatech-mea.com'

    # Pagination
    PRODUCTS_PER_PAGE = 12

    # reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
