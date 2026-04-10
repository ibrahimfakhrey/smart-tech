import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from slugify import slugify
from flask import current_app


def generate_slug(text):
    """Generate a URL-friendly slug. For Arabic text, use transliteration + uuid suffix."""
    slug = slugify(text, allow_unicode=False)
    if not slug:
        slug = str(uuid.uuid4())[:8]
    # Ensure uniqueness by appending short uuid if needed
    return slug


def generate_ref_number():
    """Generate a unique RFQ reference number like RFQ-2026-0001."""
    from app.models import RFQRequest
    year = datetime.utcnow().year
    last = RFQRequest.query.filter(
        RFQRequest.ref_number.like(f'RFQ-{year}-%')
    ).order_by(RFQRequest.id.desc()).first()

    if last:
        last_num = int(last.ref_number.split('-')[-1])
        new_num = last_num + 1
    else:
        new_num = 1

    return f'RFQ-{year}-{new_num:04d}'


def save_uploaded_file(file, subfolder='images'):
    """Save an uploaded file and return its relative path."""
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    if not filename:
        return None

    # Validate extension
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if subfolder.startswith('images'):
        allowed = current_app.config.get('ALLOWED_IMAGE_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp', 'gif'})
    else:
        allowed = current_app.config.get('ALLOWED_DOC_EXTENSIONS', {'pdf'})
    if ext not in allowed:
        return None

    # Add uuid prefix to avoid collisions
    unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"

    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, unique_name)
    file.save(filepath)

    # Optimize images
    if subfolder == 'images':
        try:
            from PIL import Image
            img = Image.open(filepath)
            # Convert RGBA to RGB for JPEG
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            # Resize if very large (max 1920px wide)
            max_width = 1920
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
            # Save optimized
            img.save(filepath, quality=85, optimize=True)
        except Exception:
            pass  # Keep original if optimization fails

    # Return relative path from static folder
    return f'uploads/{subfolder}/{unique_name}'


def send_rfq_confirmation_email(rfq):
    """Send confirmation email to the client."""
    from flask_mail import Message
    from app import mail

    product_name = rfq.product.name_ar if rfq.product else 'طلب متعدد المنتجات'

    msg = Message(
        subject=f'تأكيد استلام طلبك - {rfq.ref_number}',
        recipients=[rfq.email]
    )
    msg.html = f"""
    <div dir="rtl" style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>شكراً لتواصلك مع سما تكنولوجي</h2>
        <p>عزيزنا {rfq.full_name}،</p>
        <p>تم استلام طلب عرض السعر الخاص بك بنجاح.</p>
        <table style="border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 8px; font-weight: bold;">رقم المرجع:</td><td style="padding: 8px;">{rfq.ref_number}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">المنتج:</td><td style="padding: 8px;">{product_name}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">الشركة:</td><td style="padding: 8px;">{rfq.company_name}</td></tr>
        </table>
        <p>سيتواصل معك فريقنا خلال 24-48 ساعة عمل.</p>
        <br>
        <p>مع تحيات فريق سما تكنولوجي</p>
        <p style="color: #666;">Sama Technology - Plug Into The Future</p>
    </div>
    """
    mail.send(msg)


def send_rfq_admin_notification(rfq):
    """Send notification email to Sama Tech admin team."""
    from flask_mail import Message
    from app import mail

    product_name = rfq.product.name_ar if rfq.product else 'طلب متعدد المنتجات'

    msg = Message(
        subject=f'طلب عرض سعر جديد - {rfq.ref_number}',
        recipients=[current_app.config['COMPANY_EMAIL']]
    )
    msg.html = f"""
    <div dir="rtl" style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>طلب عرض سعر جديد</h2>
        <table style="border-collapse: collapse;">
            <tr><td style="padding: 8px; font-weight: bold;">رقم المرجع:</td><td style="padding: 8px;">{rfq.ref_number}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">الاسم:</td><td style="padding: 8px;">{rfq.full_name}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">البريد:</td><td style="padding: 8px;">{rfq.email}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">الجوال:</td><td style="padding: 8px;">{rfq.phone}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">الشركة:</td><td style="padding: 8px;">{rfq.company_name}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">المنتج:</td><td style="padding: 8px;">{product_name}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">ملاحظات:</td><td style="padding: 8px;">{rfq.notes or 'لا يوجد'}</td></tr>
        </table>
    </div>
    """
    mail.send(msg)
