from flask import Blueprint, render_template, request, jsonify, abort
from app.models import db, Product, Category, Brand, ShippingInfo

catalog_bp = Blueprint('catalog_bp', __name__)


@catalog_bp.route('/')
def product_list():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Base query
    query = Product.query.filter_by(is_active=True)

    # Category filter
    category_slugs = request.args.getlist('category')
    if category_slugs:
        cat_ids = []
        for slug in category_slugs:
            cat = Category.query.filter_by(slug=slug).first()
            if cat:
                cat_ids.append(cat.id)
                for sub in cat.subcategories:
                    cat_ids.append(sub.id)
        if cat_ids:
            query = query.filter(Product.category_id.in_(cat_ids))

    # Brand filter
    brand_slugs = request.args.getlist('brand')
    if brand_slugs:
        brand_ids = [b.id for b in Brand.query.filter(Brand.slug.in_(brand_slugs)).all()]
        if brand_ids:
            query = query.filter(Product.brand_id.in_(brand_ids))

    # Search
    search_q = request.args.get('q', '').strip()
    if search_q:
        query = query.filter(
            db.or_(
                Product.name_ar.ilike(f'%{search_q}%'),
                Product.sku.ilike(f'%{search_q}%'),
                Product.short_description_ar.ilike(f'%{search_q}%')
            )
        )

    # Sort
    sort = request.args.get('sort', 'newest')
    if sort == 'views':
        query = query.order_by(Product.views_count.desc())
    elif sort == 'name':
        query = query.order_by(Product.name_ar.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()
    shipping = ShippingInfo.query.filter_by(is_active=True).first()

    return render_template('catalog.html',
                           products=products,
                           categories=categories,
                           brands=brands,
                           shipping_info=shipping,
                           current_search=search_q,
                           current_sort=sort,
                           current_categories=category_slugs,
                           current_brands=brand_slugs)


@catalog_bp.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])

    products = Product.query.filter(
        Product.is_active == True,
        db.or_(
            Product.name_ar.ilike(f'%{q}%'),
            Product.sku.ilike(f'%{q}%')
        )
    ).limit(10).all()

    results = []
    for p in products:
        img = p.primary_image
        results.append({
            'id': p.id,
            'name': p.name_ar,
            'sku': p.sku,
            'slug': p.slug,
            'category': p.category.name_ar if p.category else '',
            'brand': p.brand.name if p.brand else '',
            'image': img.image_path if img else None
        })
    return jsonify(results)


@catalog_bp.route('/compare')
def compare_products():
    ids = request.args.get('ids', '')
    product_ids = [int(x) for x in ids.split(',') if x.strip().isdigit()][:2]
    products = Product.query.filter(Product.id.in_(product_ids), Product.is_active == True).all() if product_ids else []
    return render_template('compare.html', products=products)


@catalog_bp.route('/wishlist')
def wishlist_page():
    return render_template('wishlist.html')


@catalog_bp.route('/api/products-by-ids')
def api_products_by_ids():
    ids = request.args.get('ids', '')
    product_ids = [int(x) for x in ids.split(',') if x.strip().isdigit()]
    products = Product.query.filter(Product.id.in_(product_ids), Product.is_active == True).all() if product_ids else []
    results = []
    for p in products:
        img = p.primary_image
        cat = p.category
        results.append({
            'id': p.id,
            'name': p.name_ar,
            'sku': p.sku,
            'slug': p.slug,
            'brand': p.brand.name if p.brand else '',
            'category': cat.name_ar if cat else '',
            'category_slug': (cat.parent.slug if cat and cat.parent else cat.slug) if cat else '',
            'image': img.image_path if img else None,
            'specs': p.specs_json or {}
        })
    return jsonify(results)


@catalog_bp.route('/<string:category_slug>/')
def category_products(category_slug):
    category = Category.query.filter_by(slug=category_slug, is_active=True).first_or_404()

    page = request.args.get('page', 1, type=int)
    cat_ids = [category.id] + [s.id for s in category.subcategories]
    products = Product.query.filter(
        Product.is_active == True,
        Product.category_id.in_(cat_ids)
    ).order_by(Product.created_at.desc()).paginate(page=page, per_page=12, error_out=False)

    categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()

    return render_template('catalog.html',
                           products=products,
                           categories=categories,
                           brands=brands,
                           current_category=category,
                           current_search='',
                           current_sort='newest',
                           current_categories=[category_slug],
                           current_brands=[])


@catalog_bp.route('/<string:category_slug>/<string:product_slug>/')
def product_detail(category_slug, product_slug):
    product = Product.query.filter_by(slug=product_slug, is_active=True).first_or_404()

    # Increment view count
    product.views_count = (product.views_count or 0) + 1
    db.session.commit()

    # Related products from same category
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()

    shipping = ShippingInfo.query.filter_by(is_active=True).first()

    return render_template('product_detail.html',
                           product=product,
                           related_products=related,
                           shipping_info=shipping)
