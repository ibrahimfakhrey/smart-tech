from flask import Blueprint, render_template, request, jsonify, Response, url_for
from app.models import db, Category, Brand, Product, FeaturedProduct, CompanyInfo, NewsletterSub, ShippingInfo
from app import csrf

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def home():
    # Featured products grouped by category
    featured = (
        db.session.query(Product)
        .join(FeaturedProduct, FeaturedProduct.product_id == Product.id)
        .filter(Product.is_active == True)
        .order_by(FeaturedProduct.sort_order)
        .all()
    )

    categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()
    shipping = ShippingInfo.query.filter_by(is_active=True).all()

    return render_template('home.html',
                           featured_products=featured,
                           categories=categories,
                           brands=brands,
                           shipping_info=shipping)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')


@main_bp.route('/newsletter', methods=['POST'])
@csrf.exempt
def newsletter_subscribe():
    email = request.form.get('email', '').strip()
    if not email:
        return jsonify({'success': False, 'message': 'يرجى إدخال البريد الإلكتروني'}), 400

    existing = NewsletterSub.query.filter_by(email=email).first()
    if existing:
        return jsonify({'success': True, 'message': 'أنت مشترك بالفعل في النشرة البريدية'})

    sub = NewsletterSub(email=email)
    db.session.add(sub)
    db.session.commit()
    return jsonify({'success': True, 'message': 'تم الاشتراك بنجاح في النشرة البريدية'})


@main_bp.route('/robots.txt')
def robots_txt():
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /rfq/

Sitemap: https://www.samatech-mea.com/sitemap.xml
"""
    return Response(content, mimetype='text/plain')


@main_bp.route('/sitemap.xml')
def sitemap():
    pages = []
    base = 'https://www.samatech-mea.com'

    # Static pages
    for rule in ['main_bp.home', 'main_bp.about', 'main_bp.contact', 'main_bp.privacy', 'catalog_bp.product_list']:
        pages.append({'loc': base + url_for(rule), 'priority': '1.0' if rule == 'main_bp.home' else '0.8'})

    # Categories
    categories = Category.query.filter_by(is_active=True).all()
    for cat in categories:
        pages.append({
            'loc': base + url_for('catalog_bp.category_products', category_slug=cat.slug),
            'priority': '0.7'
        })

    # Products
    products = Product.query.filter_by(is_active=True).all()
    for p in products:
        cat_slug = (p.category.parent.slug if p.category and p.category.parent else p.category.slug) if p.category else 'products'
        pages.append({
            'loc': base + url_for('catalog_bp.product_detail', category_slug=cat_slug, product_slug=p.slug),
            'lastmod': p.updated_at.strftime('%Y-%m-%d') if p.updated_at else '',
            'priority': '0.9'
        })

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        if page.get('lastmod'):
            xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    xml += '</urlset>'

    return Response(xml, mimetype='application/xml')
