from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, PasswordField, BooleanField,
                     SelectField, IntegerField, HiddenField)
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(message='يرجى إدخال اسم المستخدم')])
    password = PasswordField('كلمة المرور', validators=[DataRequired(message='يرجى إدخال كلمة المرور')])
    remember = BooleanField('تذكرني')


class RFQForm(FlaskForm):
    full_name = StringField('الاسم الكامل', validators=[
        DataRequired(message='يرجى إدخال الاسم الكامل'),
        Length(min=3, max=150, message='الاسم يجب أن يكون بين 3 و 150 حرف')
    ])
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired(message='يرجى إدخال البريد الإلكتروني'),
        Email(message='يرجى إدخال بريد إلكتروني صحيح')
    ])
    phone = StringField('رقم الجوال', validators=[
        DataRequired(message='يرجى إدخال رقم الجوال'),
        Length(min=10, max=20, message='رقم الجوال غير صحيح')
    ])
    company_name = StringField('اسم الشركة', validators=[
        DataRequired(message='يرجى إدخال اسم الشركة'),
        Length(min=2, max=200)
    ])
    notes = TextAreaField('ملاحظات إضافية', validators=[Optional(), Length(max=2000)])
    privacy_accepted = BooleanField('أوافق على سياسة الخصوصية', validators=[
        DataRequired(message='يرجى الموافقة على سياسة الخصوصية')
    ])


class ProductForm(FlaskForm):
    name_ar = StringField('اسم المنتج', validators=[DataRequired(message='يرجى إدخال اسم المنتج')])
    sku = StringField('رمز المنتج (SKU)', validators=[DataRequired(message='يرجى إدخال رمز المنتج')])
    category_id = SelectField('التصنيف', coerce=int, validators=[DataRequired()])
    brand_id = SelectField('العلامة التجارية', coerce=int, validators=[DataRequired()])
    short_description_ar = TextAreaField('وصف مختصر', validators=[Optional()])
    full_description_ar = TextAreaField('وصف تفصيلي', validators=[Optional()])
    specs_json = TextAreaField('المواصفات التقنية (JSON)', validators=[Optional()])
    shipping_info = TextAreaField('معلومات الشحن', validators=[Optional()])
    is_featured = BooleanField('منتج مميز')
    is_active = BooleanField('مفعل', default=True)


class CategoryForm(FlaskForm):
    name_ar = StringField('اسم التصنيف بالعربية', validators=[DataRequired()])
    name_en = StringField('اسم التصنيف بالإنجليزية', validators=[Optional()])
    icon = StringField('أيقونة', validators=[Optional()])
    parent_id = SelectField('التصنيف الأب', coerce=int, validators=[Optional()])


class BrandForm(FlaskForm):
    name = StringField('اسم العلامة التجارية', validators=[DataRequired()])
    description_ar = TextAreaField('الوصف', validators=[Optional()])
    website_url = StringField('رابط الموقع', validators=[Optional()])


class ShippingForm(FlaskForm):
    delivery_area_ar = StringField('منطقة التوصيل', validators=[DataRequired()])
    estimated_days = StringField('المدة التقديرية', validators=[Optional()])
    coverage_regions_ar = TextAreaField('مناطق التغطية', validators=[Optional()])
