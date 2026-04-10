from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(150), nullable=False)
    name_en = db.Column(db.String(150))
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parent = db.relationship('Category', remote_side=[id], backref=db.backref('subcategories', lazy='dynamic', order_by='Category.sort_order'))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    @property
    def product_count(self):
        count = self.products.filter_by(is_active=True).count()
        for sub in self.subcategories:
            count += sub.products.filter_by(is_active=True).count()
        return count


class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo_path = db.Column(db.String(255))
    description_ar = db.Column(db.Text)
    website_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='brand', lazy='dynamic')

    @property
    def product_count(self):
        return self.products.filter_by(is_active=True).count()


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False, index=True)
    short_description_ar = db.Column(db.Text)
    full_description_ar = db.Column(db.Text)
    specs_json = db.Column(db.JSON)
    shipping_info = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('ProductImage', backref='product', lazy='dynamic', order_by='ProductImage.sort_order', cascade='all, delete-orphan')
    documents = db.relationship('ProductDocument', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    rfq_requests = db.relationship('RFQRequest', backref='product', lazy='dynamic')

    @property
    def primary_image(self):
        img = self.images.filter_by(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img


class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    image_path = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)


class ProductDocument(db.Model):
    __tablename__ = 'product_documents'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    doc_type = db.Column(db.String(20), nullable=False)  # datasheet, manual, brochure


class RFQRequest(db.Model):
    __tablename__ = 'rfq_requests'
    id = db.Column(db.Integer, primary_key=True)
    ref_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='new', index=True)  # new, reviewing, replied, closed
    admin_notes = db.Column(db.Text)
    privacy_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product_ids_json = db.Column(db.JSON)

    @property
    def status_ar(self):
        return {
            'new': 'جديد',
            'reviewing': 'قيد المراجعة',
            'replied': 'تم الرد',
            'closed': 'مغلق'
        }.get(self.status, self.status)


class ShippingInfo(db.Model):
    __tablename__ = 'shipping_info'
    id = db.Column(db.Integer, primary_key=True)
    delivery_area_ar = db.Column(db.String(200), nullable=False)
    estimated_days = db.Column(db.String(50))
    coverage_regions_ar = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)


class FeaturedProduct(db.Model):
    __tablename__ = 'featured_products'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref='featured_entry')


class NewsletterSub(db.Model):
    __tablename__ = 'newsletter_subs'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)


class CompanyInfo(db.Model):
    __tablename__ = 'company_info'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
