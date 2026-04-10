"""
Seed test-specific data: extra test users, RFQ orders, newsletter subs.
Run AFTER seed_data.py: python seed_test_data.py
"""
from flask_app import app
from app.models import db, Admin, RFQRequest, Product, NewsletterSub


def seed_test():
    with app.app_context():
        # ─── Extra Admin for testing ───
        if not Admin.query.filter_by(username='testadmin').first():
            admin = Admin(username='testadmin', email='test@samatech-mea.com')
            admin.set_password('Test1234!')
            db.session.add(admin)
            print('✓ Test admin created (username: testadmin, password: Test1234!)')

        # ─── Sample RFQ Orders for testing ───
        products = Product.query.limit(4).all()
        if not RFQRequest.query.first() and products:
            test_orders = [
                {
                    'ref_number': 'RFQ-2026-0001',
                    'product_id': products[0].id,
                    'full_name': 'أحمد محمد الشمري',
                    'email': 'ahmed@testcorp.sa',
                    'phone': '0501234567',
                    'company_name': 'شركة التقنية المتقدمة',
                    'notes': 'نحتاج 10 وحدات مع التركيب',
                    'status': 'new',
                    'privacy_accepted': True
                },
                {
                    'ref_number': 'RFQ-2026-0002',
                    'product_id': products[1].id if len(products) > 1 else products[0].id,
                    'full_name': 'سارة عبدالله القحطاني',
                    'email': 'sara@govtech.gov.sa',
                    'phone': '0559876543',
                    'company_name': 'وزارة التعليم',
                    'notes': 'طلب لتجهيز 5 قاعات اجتماعات',
                    'status': 'reviewing',
                    'privacy_accepted': True
                },
                {
                    'ref_number': 'RFQ-2026-0003',
                    'product_id': products[2].id if len(products) > 2 else products[0].id,
                    'full_name': 'خالد إبراهيم العتيبي',
                    'email': 'khalid@smartoffice.sa',
                    'phone': '0543216789',
                    'company_name': 'مكاتب ذكية للحلول التقنية',
                    'notes': '',
                    'status': 'replied',
                    'privacy_accepted': True
                },
                {
                    'ref_number': 'RFQ-2026-0004',
                    'product_id': None,
                    'product_ids_json': [p.id for p in products[:3]],
                    'full_name': 'فهد سعد الدوسري',
                    'email': 'fahad@buildco.sa',
                    'phone': '0567891234',
                    'company_name': 'شركة البناء والتشييد',
                    'notes': 'طلب مجمع - نحتاج عرض سعر لكامل المنتجات',
                    'status': 'closed',
                    'privacy_accepted': True
                },
            ]

            for order_data in test_orders:
                db.session.add(RFQRequest(**order_data))
            print('✓ 4 test RFQ orders created')

        # ─── Newsletter subscribers ───
        test_emails = ['test1@example.com', 'test2@example.com', 'newsletter@testcorp.sa']
        for email in test_emails:
            if not NewsletterSub.query.filter_by(email=email).first():
                db.session.add(NewsletterSub(email=email))
        print('✓ Newsletter test subscribers added')

        db.session.commit()
        print('\n✅ Test data seeded successfully!')
        print('   Test Admin: testadmin / Test1234!')
        print('   Main Admin: admin / SamaTech2026!')


if __name__ == '__main__':
    seed_test()
