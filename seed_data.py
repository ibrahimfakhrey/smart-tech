"""
Seed script for Sama Technology Product Catalog.
Run: python seed_data.py
"""
from flask_app import app
from app.models import db, Admin, Category, Brand, ShippingInfo, CompanyInfo, Product, ProductImage

def seed():
    with app.app_context():
        db.create_all()

        # ─── Admin ───
        if not Admin.query.first():
            admin = Admin(username='admin', email='admin@samatech-mea.com')
            admin.set_password('SamaTech2026!')
            db.session.add(admin)
            print('✓ Admin created (username: admin)')

        # ─── Main Categories + Subcategories ───
        categories_data = [
            {
                'name_ar': 'الشاشات التفاعلية',
                'name_en': 'Interactive Screens',
                'slug': 'interactive-screens',
                'icon': 'bi-display',
                'sort_order': 1,
                'subs': [
                    {'name_ar': 'شاشات للاجتماعات', 'name_en': 'Meeting Screens', 'slug': 'meeting-screens'},
                    {'name_ar': 'شاشات تعليمية', 'name_en': 'Educational Screens', 'slug': 'educational-screens'},
                    {'name_ar': 'شاشات LED', 'name_en': 'LED Screens', 'slug': 'led-screens'},
                    {'name_ar': 'شاشات العرض التجارية', 'name_en': 'Commercial Displays', 'slug': 'commercial-displays'},
                ]
            },
            {
                'name_ar': 'أجهزة مؤتمرات الفيديو',
                'name_en': 'Video Conferencing',
                'slug': 'video-conferencing',
                'icon': 'bi-camera-video',
                'sort_order': 2,
                'subs': [
                    {'name_ar': 'غرف صغيرة (6-16 شخص)', 'name_en': 'Small Rooms', 'slug': 'small-rooms'},
                    {'name_ar': 'غرف كبيرة (16+)', 'name_en': 'Large Rooms', 'slug': 'large-rooms'},
                    {'name_ar': 'حلول Microsoft Teams', 'name_en': 'Microsoft Teams Solutions', 'slug': 'ms-teams-solutions'},
                    {'name_ar': 'حلول Zoom', 'name_en': 'Zoom Solutions', 'slug': 'zoom-solutions'},
                ]
            },
            {
                'name_ar': 'هواتف IP وVoIP',
                'name_en': 'IP Phones & VoIP',
                'slug': 'ip-phones-voip',
                'icon': 'bi-telephone',
                'sort_order': 3,
                'subs': [
                    {'name_ar': 'هواتف SIP مكتبية', 'name_en': 'SIP Desk Phones', 'slug': 'sip-desk-phones'},
                    {'name_ar': 'هواتف لمس', 'name_en': 'Touch Phones', 'slug': 'touch-phones'},
                    {'name_ar': 'هواتف لاسلكية DECT', 'name_en': 'DECT Wireless Phones', 'slug': 'dect-wireless-phones'},
                    {'name_ar': 'هواتف Teams', 'name_en': 'Teams Phones', 'slug': 'teams-phones'},
                ]
            },
            {
                'name_ar': 'السماعات والميكروفونات',
                'name_en': 'Speakers & Microphones',
                'slug': 'speakers-microphones',
                'icon': 'bi-headset',
                'sort_order': 4,
                'subs': [
                    {'name_ar': 'سماعات لاسلكية', 'name_en': 'Wireless Headsets', 'slug': 'wireless-headsets'},
                    {'name_ar': 'سماعات سلكية', 'name_en': 'Wired Headsets', 'slug': 'wired-headsets'},
                    {'name_ar': 'سماعات USB', 'name_en': 'USB Headsets', 'slug': 'usb-headsets'},
                    {'name_ar': 'سماعات مؤتمرات', 'name_en': 'Conference Speakers', 'slug': 'conference-speakers'},
                ]
            },
            {
                'name_ar': 'كاميرات المؤتمرات',
                'name_en': 'Conference Cameras',
                'slug': 'conference-cameras',
                'icon': 'bi-webcam',
                'sort_order': 5,
                'subs': [
                    {'name_ar': 'كاميرات 4K', 'name_en': '4K Cameras', 'slug': '4k-cameras'},
                    {'name_ar': 'كاميرات 360°', 'name_en': '360 Cameras', 'slug': '360-cameras'},
                    {'name_ar': 'كاميرات USB', 'name_en': 'USB Cameras', 'slug': 'usb-cameras'},
                    {'name_ar': 'كاميرات ذكية', 'name_en': 'Smart Cameras', 'slug': 'smart-cameras'},
                ]
            },
            {
                'name_ar': 'اكسسوارات وإضافات',
                'name_en': 'Accessories',
                'slug': 'accessories',
                'icon': 'bi-plug',
                'sort_order': 6,
                'subs': [
                    {'name_ar': 'وحدات توسعة', 'name_en': 'Expansion Modules', 'slug': 'expansion-modules'},
                    {'name_ar': 'حوامل', 'name_en': 'Mounts & Stands', 'slug': 'mounts-stands'},
                    {'name_ar': 'محولات', 'name_en': 'Adapters', 'slug': 'adapters'},
                    {'name_ar': 'دونجل واي-فاي', 'name_en': 'Wi-Fi Dongles', 'slug': 'wifi-dongles'},
                ]
            },
        ]

        if not Category.query.first():
            for cat_data in categories_data:
                subs = cat_data.pop('subs')
                cat = Category(**cat_data)
                db.session.add(cat)
                db.session.flush()

                for sub_data in subs:
                    sub = Category(
                        name_ar=sub_data['name_ar'],
                        name_en=sub_data['name_en'],
                        slug=sub_data['slug'],
                        parent_id=cat.id,
                        sort_order=0
                    )
                    db.session.add(sub)
            print('✓ Categories seeded (6 main + subcategories)')

        # ─── Brands ───
        brands_data = [
            {'name': 'Yealink', 'slug': 'yealink', 'description_ar': 'شركة رائدة عالمياً في حلول الاتصالات الموحدة وأجهزة مؤتمرات الفيديو'},
            {'name': 'MAXHUB', 'slug': 'maxhub', 'description_ar': 'رائدة في الشاشات التفاعلية وحلول غرف الاجتماعات الذكية'},
            {'name': 'Poly', 'slug': 'poly', 'description_ar': 'متخصصة في سماعات الرأس وأنظمة مؤتمرات الصوت والفيديو'},
            {'name': 'Logitech', 'slug': 'logitech', 'description_ar': 'حلول كاميرات وأجهزة مؤتمرات الفيديو عالية الجودة'},
            {'name': 'Jabra', 'slug': 'jabra', 'description_ar': 'سماعات وميكروفونات احترافية للمكاتب ومراكز الاتصال'},
            {'name': 'Cisco', 'slug': 'cisco', 'description_ar': 'حلول شبكات واتصالات متكاملة للمؤسسات'},
            {'name': 'Grandstream', 'slug': 'grandstream', 'description_ar': 'هواتف IP وحلول اتصالات بأسعار تنافسية'},
            {'name': 'Samsung', 'slug': 'samsung', 'description_ar': 'شاشات عرض تجارية وشاشات LED احترافية'},
            {'name': 'LG', 'slug': 'lg', 'description_ar': 'شاشات عرض وحلول Digital Signage'},
            {'name': 'AVer', 'slug': 'aver', 'description_ar': 'كاميرات مؤتمرات وحلول تعليمية تفاعلية'},
            {'name': 'Yeastar', 'slug': 'yeastar', 'description_ar': 'أنظمة PBX سحابية وحلول اتصالات موحدة'},
            {'name': 'Huawei', 'slug': 'huawei', 'description_ar': 'حلول شبكات وبنية تحتية تقنية متكاملة'},
            {'name': '3CX', 'slug': '3cx', 'description_ar': 'نظام اتصالات موحد برمجي للمؤسسات'},
            {'name': 'Akuvox', 'slug': 'akuvox', 'description_ar': 'أنظمة اتصال داخلي وأجهزة إنتركم ذكية'},
            {'name': 'Akubela', 'slug': 'akubela', 'description_ar': 'حلول المنازل الذكية وأنظمة التحكم'},
            {'name': 'QSTECH', 'slug': 'qstech', 'description_ar': 'شاشات LED احترافية وحلول العرض المرئي'},
        ]

        if not Brand.query.first():
            for brand_data in brands_data:
                db.session.add(Brand(**brand_data))
            print('✓ Brands seeded (16 brands)')

        # ─── Shipping Info ───
        if not ShippingInfo.query.first():
            db.session.add(ShippingInfo(
                delivery_area_ar='داخل المملكة العربية السعودية',
                estimated_days='3-7 أيام عمل',
                coverage_regions_ar='جميع مناطق المملكة العربية السعودية - الرياض، جدة، الدمام، مكة، المدينة وجميع المدن'
            ))
            db.session.add(ShippingInfo(
                delivery_area_ar='دول الخليج العربي',
                estimated_days='7-14 يوم عمل',
                coverage_regions_ar='الإمارات، الكويت، البحرين، عمان، قطر'
            ))
            print('✓ Shipping info seeded')

        # ─── Company Info ───
        company_data = {
            'company_name_ar': 'سما تكنولوجي',
            'company_name_en': 'Sama Technology',
            'tagline': 'Plug Into The Future',
            'phone_1': '0556333171',
            'phone_2': '0556333601',
            'email': 'info@samatech-mea.com',
            'website': 'www.samatech-mea.com',
            'years_experience': '10+',
            'clients_count': '500+',
            'products_count': '200+',
            'coverage': 'السعودية والخليج',
            'about_ar': 'سما تك هي شركة متخصصة في حلول الاتصالات وأنظمة التيار الخفيف والبنية التحتية التقنية. تمتلك خبرة عملية تمتد لأكثر من 10 سنوات في السوق المصري، توسعت بأعمالها لتخدم السوق السعودي بنفس المعايير المهنية والجودة العالية. تقدم حلولاً متكاملة تعتمد على الفهم العميق لاحتياجات العملاء، مع التركيز على الاعتمادية، الاستقرار، وقابلية التوسع.',
            'vision_ar': 'أن نكون شريكاً تقنياً موثوقاً في حلول الاتصالات والبنية التحتية الذكية في الشرق الأوسط، من خلال تقديم أنظمة مستقرة قابلة للتطوير، ومبنية على أفضل الممارسات العالمية.',
            'mission_ar': 'تقديم حلول تقنية عملية وفعّالة تساعد عملاءنا على تحسين الأداء، رفع كفاءة الاتصال، وضمان استمرارية الأعمال مع الالتزام بالجودة، الاحترافية، والدعم الفني المستمر.',
            'services_1': 'حلول VoIP ومراكز الاتصال',
            'services_1_desc': 'أنظمة IP PBX، مراكز اتصال، أنظمة IVR والرقم الموحد، تسجيل المكالمات، ربط الفروع، تكامل مع CRM وERP',
            'services_2': 'البنية التحتية للشبكات',
            'services_2_desc': 'تصميم وتنفيذ شبكات LAN & WAN، Fiber Optic & Structured Cabling، حلول Wi-Fi للمؤسسات، إدارة وتأمين الشبكات',
            'services_3': 'أنظمة التيار الخفيف',
            'services_3_desc': 'أنظمة كاميرات المراقبة CCTV، أنظمة الصوتيات والنداء العام، أنظمة السنترالات وأنظمة التحكم والدخول',
            'services_4': 'الدعم الفني وعقود الصيانة',
            'services_4_desc': 'عقود صيانة سنوية ودعم فني 24/7، استجابة سريعة للأعطال وصيانة وقائية وتحسينية',
            'values_ar': 'الاحترافية في التنفيذ|الشفافية مع العملاء|الاعتماد على حلول عملية قابلة للتطوير|الالتزام بالجودة والمعايير الفنية|بناء علاقات طويلة الأمد',
            'sectors_ar': 'الشركات والمؤسسات|المدارس والجامعات|المستشفيات والمراكز الطبية|الفنادق|مراكز الاتصال',
            'hero_headline': 'شريكك التقني الموثوق لحلول الاتصالات والبنية التحتية الذكية',
            'hero_cta': 'تصفح المنتجات',
        }

        if not CompanyInfo.query.first():
            for key, value in company_data.items():
                db.session.add(CompanyInfo(key=key, value=value))
            print('✓ Company info seeded')

        # ─── Sample Products ───
        if not Product.query.first():
            # Get category and brand references
            cats = {c.slug: c for c in Category.query.all()}
            brands = {b.slug: b for b in Brand.query.all()}

            sample_products = [
                # Interactive Screens
                {
                    'name_ar': 'MAXHUB V6 Classic 65" شاشة تفاعلية',
                    'sku': 'MH-V6C-65',
                    'slug': 'maxhub-v6-classic-65',
                    'category': 'meeting-screens',
                    'brand': 'maxhub',
                    'short_description_ar': 'شاشة تفاعلية 65 بوصة بدقة 4K مثالية لغرف الاجتماعات',
                    'specs_json': {'الحجم': '65 بوصة', 'الدقة': '4K UHD', 'اللمس': '20 نقطة لمس', 'النظام': 'Android 11', 'المنافذ': 'HDMI, USB-C, USB 3.0'},
                    'is_featured': True
                },
                {
                    'name_ar': 'MAXHUB V6 ViewPro 75" شاشة تفاعلية',
                    'sku': 'MH-V6VP-75',
                    'slug': 'maxhub-v6-viewpro-75',
                    'category': 'meeting-screens',
                    'brand': 'maxhub',
                    'short_description_ar': 'شاشة تفاعلية احترافية 75 بوصة لغرف الاجتماعات الكبيرة',
                    'specs_json': {'الحجم': '75 بوصة', 'الدقة': '4K UHD', 'اللمس': '40 نقطة لمس', 'الكاميرا': 'مدمجة 48MP'},
                    'is_featured': True
                },
                # Video Conferencing
                {
                    'name_ar': 'Yealink MeetingBar A30 نظام مؤتمرات فيديو',
                    'sku': 'YL-A30',
                    'slug': 'yealink-meetingbar-a30',
                    'category': 'small-rooms',
                    'brand': 'yealink',
                    'short_description_ar': 'نظام مؤتمرات فيديو متكامل للغرف الصغيرة والمتوسطة - يدعم Teams و Zoom',
                    'specs_json': {'الكاميرا': '4K مع AI Tracking', 'الصوت': '8 ميكروفونات MEMS', 'التوافق': 'Microsoft Teams, Zoom', 'الاتصال': 'Wi-Fi 6, Bluetooth 5.0'},
                    'is_featured': True
                },
                {
                    'name_ar': 'Poly Studio X50 نظام مؤتمرات',
                    'sku': 'PL-X50',
                    'slug': 'poly-studio-x50',
                    'category': 'small-rooms',
                    'brand': 'poly',
                    'short_description_ar': 'جهاز مؤتمرات فيديو متكامل مع كاميرا 4K وصوت محيطي',
                    'specs_json': {'الكاميرا': '4K، زاوية 120°', 'الصوت': 'ستيريو مع إلغاء الضوضاء', 'التوافق': 'Teams, Zoom, RingCentral'},
                    'is_featured': True
                },
                # IP Phones
                {
                    'name_ar': 'Yealink T54W هاتف IP مكتبي',
                    'sku': 'YL-T54W',
                    'slug': 'yealink-t54w',
                    'category': 'sip-desk-phones',
                    'brand': 'yealink',
                    'short_description_ar': 'هاتف IP احترافي بشاشة ملونة 4.3 بوصة ودعم Wi-Fi و Bluetooth',
                    'specs_json': {'الشاشة': '4.3 بوصة ملونة', 'الخطوط': '16 حساب SIP', 'الاتصال': 'Wi-Fi, Bluetooth, USB', 'PoE': 'نعم'},
                    'is_featured': True
                },
                {
                    'name_ar': 'Grandstream GRP2615 هاتف IP',
                    'sku': 'GS-GRP2615',
                    'slug': 'grandstream-grp2615',
                    'category': 'sip-desk-phones',
                    'brand': 'grandstream',
                    'short_description_ar': 'هاتف IP متقدم بشاشة لمس 4.3 بوصة و 10 خطوط',
                    'specs_json': {'الشاشة': '4.3 بوصة لمس', 'الخطوط': '10 حسابات SIP', 'Wi-Fi': 'مدمج', 'Bluetooth': 'مدمج'},
                },
                # Speakers & Microphones
                {
                    'name_ar': 'Jabra Speak2 75 سماعة مؤتمرات',
                    'sku': 'JB-SPK275',
                    'slug': 'jabra-speak2-75',
                    'category': 'conference-speakers',
                    'brand': 'jabra',
                    'short_description_ar': 'سماعة مؤتمرات لاسلكية بتقنية إلغاء الضوضاء لغرف الاجتماعات',
                    'specs_json': {'النوع': 'سماعة مؤتمرات', 'الاتصال': 'Bluetooth, USB-A', 'البطارية': '24 ساعة', 'المشاركين': 'حتى 8 أشخاص'},
                    'is_featured': True
                },
                {
                    'name_ar': 'Poly Sync 60 سماعة مؤتمرات',
                    'sku': 'PL-SYNC60',
                    'slug': 'poly-sync-60',
                    'category': 'conference-speakers',
                    'brand': 'poly',
                    'short_description_ar': 'سماعة مؤتمرات USB و Bluetooth للمكاتب وغرف الاجتماعات',
                    'specs_json': {'الاتصال': 'USB-A, USB-C, Bluetooth', 'الميكروفونات': '6 ميكروفونات', 'إلغاء الصدى': 'نعم'},
                },
                # Conference Cameras
                {
                    'name_ar': 'Yealink UVC34 كاميرا مؤتمرات 4K',
                    'sku': 'YL-UVC34',
                    'slug': 'yealink-uvc34',
                    'category': '4k-cameras',
                    'brand': 'yealink',
                    'short_description_ar': 'كاميرا مؤتمرات 4K مع ميكروفونات ومكبر صوت مدمج - الكل في واحد',
                    'specs_json': {'الدقة': '4K', 'زاوية الرؤية': '120°', 'AI': 'تتبع المتحدث', 'الميكروفونات': 'مدمجة'},
                    'is_featured': True
                },
                {
                    'name_ar': 'Logitech Rally Bar كاميرا مؤتمرات',
                    'sku': 'LG-RALLYBAR',
                    'slug': 'logitech-rally-bar',
                    'category': '4k-cameras',
                    'brand': 'logitech',
                    'short_description_ar': 'نظام مؤتمرات فيديو متكامل للغرف المتوسطة والكبيرة',
                    'specs_json': {'الدقة': '4K', 'الصوت': 'AI Noise Suppression', 'التوافق': 'Teams, Zoom, Google Meet'},
                    'is_featured': True
                },
                # Accessories
                {
                    'name_ar': 'Yealink EXP50 وحدة توسعة',
                    'sku': 'YL-EXP50',
                    'slug': 'yealink-exp50',
                    'category': 'expansion-modules',
                    'brand': 'yealink',
                    'short_description_ar': 'وحدة توسعة بشاشة ملونة لهواتف Yealink - تضيف 60 مفتاح برمجي',
                    'specs_json': {'الشاشة': '4.3 بوصة ملونة', 'المفاتيح': '20 مفتاح × 3 صفحات', 'التوافق': 'T54W, T57W, T58A'},
                },
                {
                    'name_ar': 'MAXHUB حامل شاشة متحرك ST33',
                    'sku': 'MH-ST33',
                    'slug': 'maxhub-stand-st33',
                    'category': 'mounts-stands',
                    'brand': 'maxhub',
                    'short_description_ar': 'حامل متحرك لشاشات MAXHUB التفاعلية من 55 إلى 86 بوصة',
                    'specs_json': {'التوافق': '55" - 86"', 'الحمولة': 'حتى 100 كجم', 'العجلات': '4 عجلات مع قفل', 'التعديل': 'ارتفاع قابل للتعديل'},
                },
            ]

            for p_data in sample_products:
                cat_slug = p_data.pop('category')
                brand_slug = p_data.pop('brand')

                category = cats.get(cat_slug)
                brand = brands.get(brand_slug)

                if category and brand:
                    product = Product(
                        name_ar=p_data['name_ar'],
                        sku=p_data['sku'],
                        slug=p_data['slug'],
                        category_id=category.id,
                        brand_id=brand.id,
                        short_description_ar=p_data['short_description_ar'],
                        specs_json=p_data.get('specs_json'),
                        is_featured=p_data.get('is_featured', False),
                        is_active=True
                    )
                    db.session.add(product)

            print('✓ Sample products seeded (12 products)')

        db.session.commit()
        print('\n✅ Database seeded successfully!')
        print('   Admin login: username=admin, password=SamaTech2026!')
        print('   Run the app: python flask_app.py')


if __name__ == '__main__':
    seed()
