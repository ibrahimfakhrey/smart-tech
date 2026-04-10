import requests as http_requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models import db, RFQRequest, Product
from app.forms import RFQForm
from app.utils import generate_ref_number, send_rfq_confirmation_email, send_rfq_admin_notification
from app import limiter


def verify_recaptcha(response_token):
    """Verify reCAPTCHA response with Google. Returns True if valid or if reCAPTCHA is not configured."""
    secret = current_app.config.get('RECAPTCHA_PRIVATE_KEY', '')
    if not secret:
        return True  # Skip if not configured
    try:
        resp = http_requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': secret,
            'response': response_token
        }, timeout=5)
        return resp.json().get('success', False)
    except Exception:
        return True  # Fail open if Google is unreachable

rfq_bp = Blueprint('rfq_bp', __name__)


@rfq_bp.route('/request/<int:product_id>', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def request_quote(product_id):
    product = Product.query.get_or_404(product_id)
    form = RFQForm()

    recaptcha_error = False
    if form.validate_on_submit():
        if not verify_recaptcha(request.form.get('g-recaptcha-response', '')):
            recaptcha_error = True
            return render_template('rfq_form.html', form=form, product=product, recaptcha_error=True)

        ref = generate_ref_number()
        rfq = RFQRequest(
            ref_number=ref,
            product_id=product.id,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_name=form.company_name.data,
            notes=form.notes.data,
            privacy_accepted=form.privacy_accepted.data,
            status='new'
        )
        db.session.add(rfq)
        db.session.commit()

        # Send emails (non-blocking, fail silently)
        try:
            send_rfq_confirmation_email(rfq)
            send_rfq_admin_notification(rfq)
        except Exception:
            pass

        return render_template('rfq_success.html', ref_number=ref, product=product)

    return render_template('rfq_form.html', form=form, product=product)


@rfq_bp.route('/request-bulk', methods=['POST'])
@limiter.limit("10 per hour")
def request_bulk_quote():
    """RFQ for multiple products from wishlist."""
    form = RFQForm()

    product_ids = request.form.getlist('product_ids', type=int)
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []

    if form.validate_on_submit() and products:
        if not verify_recaptcha(request.form.get('g-recaptcha-response', '')):
            return render_template('rfq_form.html', form=form, products=products, is_bulk=True, recaptcha_error=True)

        ref = generate_ref_number()
        rfq = RFQRequest(
            ref_number=ref,
            product_id=products[0].id if len(products) == 1 else None,
            product_ids_json=[p.id for p in products],
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_name=form.company_name.data,
            notes=form.notes.data,
            privacy_accepted=form.privacy_accepted.data,
            status='new'
        )
        db.session.add(rfq)
        db.session.commit()

        try:
            send_rfq_confirmation_email(rfq)
            send_rfq_admin_notification(rfq)
        except Exception:
            pass

        return render_template('rfq_success.html', ref_number=ref, products=products)

    return render_template('rfq_form.html', form=form, products=products, is_bulk=True)
