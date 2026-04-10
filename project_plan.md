# Sama Technology - Product Catalog & RFQ System
## Project Plan v1.0

---

## Project Overview

| Item | Details |
|------|---------|
| **Project Name** | Sama Technology - Product Catalog & Quote Request System |
| **Client** | Sama Technology (سما تكنولوجي) |
| **Tagline** | Plug Into The Future |
| **System Type** | B2B Web Application - No Payment Gateway |
| **Tech Stack** | Flask, Flask-SQLAlchemy, SQLite (dev) / PostgreSQL (prod), Jinja2, HTML/CSS/JS |
| **Language** | Arabic (RTL) - Primary |
| **Target Audience** | Companies, Government entities, IT contractors in Saudi Arabia & Gulf |
| **Primary Goal** | Convert visitors into RFQ (Request for Quote) submissions |
| **Website** | www.samatech-mea.com |
| **Email** | info@samatech-mea.com |
| **Phone** | 0556333171 / 0556333601 |

---

## Company Data (from Company Profile)

### About Sama Tech
Sama Tech is a company specialized in telecom solutions, low-current systems, and IT infrastructure. With 10+ years of experience in the Egyptian market, expanded to serve the Saudi and Gulf markets with the same professional standards and high quality.

### Vision
To be a trusted technology partner in telecom and smart infrastructure solutions in the Middle East.

### Mission
Delivering practical and effective technology solutions that help clients improve performance, increase communication efficiency, and ensure business continuity with commitment to quality, professionalism, and continuous technical support.

### Core Values
- Professionalism in execution
- Transparency with clients
- Reliance on scalable practical solutions
- Commitment to quality and technical standards
- Building long-term relationships

### Services
1. **VoIP & Call Center Solutions** - IP PBX, Call Center Solutions, IVR, unified numbers, call recording, branch linking, CRM/ERP integration
2. **Network Infrastructure** - LAN & WAN design, Fiber Optic & Structured Cabling, enterprise Wi-Fi, network management & security
3. **Low-Current Systems** - CCTV, PA Systems, access control, intercom systems
4. **Technical Support & SLA Maintenance** - Annual maintenance contracts, 24/7 support, preventive and corrective maintenance

### Partner Brands
Yealink, Yeastar, Huawei, MAXHUB, 3CX, Akuvox, Akubela, QSTECH, Grandstream

### Sectors Served
- Corporations & Enterprises
- Schools & Universities
- Hospitals & Medical Centers
- Hotels
- Call Centers

### Why Sama Tech (Social Proof)
- 10+ years of real experience
- Qualified engineering team
- Custom solutions per client needs
- Flexibility in execution and pricing
- Full commitment to quality standards

---

## Product Catalog Structure

| # | Main Category | Subcategories | Brands |
|---|--------------|---------------|--------|
| 1 | Interactive Screens (الشاشات التفاعلية) | Meeting screens, Educational screens, LED screens, Commercial displays | MAXHUB, Samsung, LG |
| 2 | Video Conferencing (أجهزة مؤتمرات الفيديو) | Small rooms (6-16), Large rooms (16+), Microsoft Teams solutions, Zoom solutions | Yealink, Poly, Logitech |
| 3 | IP Phones & VoIP (هواتف IP وVoIP) | SIP desk phones, Touch phones, Wireless DECT phones, Teams phones | Yealink, Cisco, Grandstream |
| 4 | Speakers & Microphones (السماعات والميكروفونات) | Wireless, Wired, USB, Conference speakers | Yealink, Jabra, Poly |
| 5 | Conference Cameras (كاميرات المؤتمرات) | 4K cameras, 360° cameras, USB cameras, Smart cameras | Yealink, Logitech, AVer |
| 6 | Accessories (اكسسوارات وإضافات) | Expansion modules, Mounts, Adapters, Wi-Fi dongles | Yealink, MAXHUB |

---

## User Roles

| Role | Type | Description | Permissions |
|------|------|-------------|-------------|
| Client / Visitor | Public | Company or entity representative browsing products | Browse, Wishlist, Compare, Submit RFQ |
| Admin | Internal | Sama Tech staff managing content | Full CRUD on products, manage orders, control homepage |

---

## Phase Breakdown

---

### PHASE 1: Project Setup & Database Foundation
**Duration: 3 days**
**Priority: Critical**

#### Tasks:
- [ ] Initialize Flask project structure
- [ ] Configure Flask-SQLAlchemy with SQLite (dev)
- [ ] Setup project directory layout:
```
smarttech/
├── flask_app.py              # Entry point
├── config.py                 # App configuration
├── requirements.txt
├── seed_data.py              # Seed categories, brands, sample products
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # All SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Public routes (home, about, contact)
│   │   ├── catalog.py        # Product catalog & detail routes
│   │   ├── rfq.py            # Quote request routes
│   │   └── admin.py          # Admin dashboard routes
│   ├── templates/
│   │   ├── base.html         # Base layout (RTL, Arabic)
│   │   ├── home.html
│   │   ├── catalog.html
│   │   ├── product_detail.html
│   │   ├── compare.html
│   │   ├── wishlist.html
│   │   ├── rfq_form.html
│   │   ├── rfq_success.html
│   │   ├── contact.html
│   │   ├── about.html
│   │   └── admin/
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── products.html
│   │       ├── product_form.html
│   │       ├── categories.html
│   │       ├── brands.html
│   │       ├── orders.html
│   │       ├── order_detail.html
│   │       ├── homepage_settings.html
│   │       └── shipping_settings.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css     # Main styles (RTL)
│   │   │   └── admin.css     # Admin panel styles
│   │   ├── js/
│   │   │   ├── main.js       # Search, filter, compare, wishlist
│   │   │   └── admin.js      # Admin interactions
│   │   ├── images/
│   │   │   ├── logo.png
│   │   │   ├── brands/       # Brand logos
│   │   │   └── products/     # Product images
│   │   └── uploads/          # Admin uploaded files (images, PDFs)
│   ├── forms.py              # WTForms for RFQ, Admin forms
│   └── utils.py              # Helpers (email, file upload, SEO slugs)
```

#### Database Models:
```python
# models.py

Category          # id, name_ar, name_en, slug, icon, parent_id (self-referential for subcategories), sort_order, is_active
Brand             # id, name, slug, logo_path, description_ar, website_url, is_active
Product           # id, name_ar, sku, slug, category_id, brand_id, short_description_ar, full_description_ar, specs_json, shipping_info, is_featured, is_active, views_count, created_at
ProductImage      # id, product_id, image_path, is_primary, sort_order
ProductDocument   # id, product_id, title, file_path, doc_type (datasheet/manual/brochure)
RFQRequest        # id, ref_number, product_id, full_name, email, phone, company_name, notes, status (new/reviewing/replied/closed), admin_notes, privacy_accepted, created_at, updated_at
ShippingInfo      # id, delivery_area_ar, estimated_days, coverage_regions_ar, is_active
FeaturedProduct   # id, product_id, sort_order (for homepage featured selection)
Admin             # id, username, email, password_hash
NewsletterSub     # id, email, subscribed_at
CompanyInfo       # id, key, value (key-value store for dynamic company info)
```

- [ ] Create all models with proper relationships and indexes
- [ ] Write seed script with:
  - 6 main categories + subcategories (from catalog structure above)
  - All brands: MAXHUB, Samsung, LG, Yealink, Poly, Logitech, Cisco, Grandstream, Jabra, AVer, Yeastar, Huawei, 3CX, Akuvox, Akubela, QSTECH
  - Default admin account
  - Default shipping info (Saudi Arabia delivery, Gulf delivery)
  - Company info entries (phone, email, address, social links, years of experience: 10+, etc.)
- [ ] Setup Flask-Migrate for database migrations
- [ ] Create requirements.txt:
  - Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Mail, Pillow, openpyxl, python-slugify

**Deliverable:** Working Flask app with database, migrations, and seed data running locally.

---

### PHASE 2: Public Frontend - Base Layout & Homepage
**Duration: 4 days**
**Priority: Critical**

#### Tasks:

**Base Layout (base.html):**
- [ ] Full RTL Arabic layout using dir="rtl" and lang="ar"
- [ ] Responsive design (Mobile-first approach)
- [ ] Navbar with: Logo (Sama Technology), Home, Products, About, Contact, Wishlist icon with count, Search icon
- [ ] Footer with: Company info, quick links, contact details (0556333171 / 0556333601, info@samatech-mea.com), social media links, copyright
- [ ] Sticky "Request Quote" CTA button visible on scroll (LP-07)
- [ ] Toast notification system for wishlist/compare actions (UX-03)
- [ ] Loading states/spinners (UX-04)
- [ ] Brand color scheme: Cyan/Purple/Blue gradient tones (from company profile)

**Homepage Sections (LP-01 to LP-08):**
- [ ] **LP-01 - Hero Section:** Full-width hero with headline about Sama Tech's identity and tech solutions, background image/gradient, prominent CTA button "Browse Products"
- [ ] **LP-02 - Services Section:** 4 service cards with icons:
  1. Supply & Distribution (توريد)
  2. Installation & Setup (تركيب)
  3. Warranty (ضمان)
  4. Technical Support (دعم فني)
- [ ] **LP-03 - Featured Products:** 2-3 products per category displayed as product cards (admin-controlled via FeaturedProduct model)
- [ ] **LP-04 - Category Cards:** 6 main category cards with icons, names, and links to filtered catalog
- [ ] **LP-05 - Brand Partners Strip:** Scrolling/static logo strip showing all partner brand logos (Yealink, MAXHUB, Cisco, Jabra, Logitech, Poly, Yeastar, Huawei, 3CX, Akuvox, Akubela, QSTECH, Grandstream, Samsung, LG, AVer)
- [ ] **LP-06 - Why Sama Tech (Social Proof):** Animated counters section:
  - 10+ Years of Experience (سنوات الخبرة)
  - Number of Clients (عدد العملاء)
  - Number of Products (عدد المنتجات)
  - Geographic Coverage - Saudi & Gulf (التغطية الجغرافية)
- [ ] **LP-07 - Main CTA:** "Contact Us / Request a Quote" section with form link
- [ ] **LP-08 - Newsletter:** Email subscription field (basic, stored in DB)

**About Page:**
- [ ] Company overview (from company profile - About, Vision, Mission)
- [ ] Core values section
- [ ] Sectors served (Corporations, Schools, Hospitals, Hotels, Call Centers)
- [ ] Quality commitment statement

**Contact Page:**
- [ ] Contact form (name, email, phone, message)
- [ ] Company contact info: phones, email, website
- [ ] Embedded Google Maps (if address available)

**Deliverable:** Fully styled RTL homepage with all sections, about page, and contact page.

---

### PHASE 3: Product Catalog Page
**Duration: 5 days**
**Priority: Critical**

#### Tasks:

**Product Catalog (PC-01 to PC-10):**
- [ ] **PC-01 - Product Grid:** Responsive grid displaying product cards with: image, name, SKU, category badge, brand logo, "Learn More" button
- [ ] **PC-02 - Category Filter:** Sidebar/dropdown checkbox multi-select filter for main and subcategories
- [ ] **PC-03 - Brand Filter:** Checkbox filter by brand with product count per brand
- [ ] **PC-04 - Live Search:** Real-time search input filtering by product name, SKU, and keywords (AJAX-based, debounced)
- [ ] **PC-05 - Sort Options:** Sort dropdown - Newest, Most Viewed, Name A-Z (أ-ي)
- [ ] **PC-06 - Pagination / Lazy Load:** Paginated results OR infinite scroll with "Load More" button
- [ ] **PC-07 - Wishlist Button:** Heart icon on each product card, toggle add/remove, saves to localStorage, updates wishlist counter in navbar
- [ ] **PC-08 - Compare Button:** "Compare" checkbox on cards, max 2 products, sticky compare bar appears at bottom when 1+ selected
- [ ] **PC-09 - Brand Info:** "About this brand" link on each card opens a modal with brand description and product listing
- [ ] **PC-10 - Shipping Info:** Fixed tooltip/banner: "Delivery within Saudi Arabia, estimated delivery time, Gulf shipping available"
- [ ] **UX-05 - Empty States:** Clear Arabic messages when no products match filters/search

**API Endpoints for AJAX:**
- [ ] `GET /api/products` - Returns filtered/sorted/paginated product JSON
- [ ] `GET /api/products/search?q=` - Live search endpoint

**Deliverable:** Fully functional catalog page with all filters, search, sort, wishlist, and compare features.

---

### PHASE 4: Product Detail Page
**Duration: 4 days**
**Priority: Critical**

#### Tasks:

**Product Detail (PD-01 to PD-10):**
- [ ] **PD-10 - Breadcrumb:** Navigation path: Home > Category > Product
- [ ] **PD-01 - Image Gallery:** Main image + thumbnails, click to switch, zoom on hover/click (lightbox)
- [ ] **PD-02 - Basic Info:** Product name, SKU, category, brand (with link), short description
- [ ] **PD-03 - Technical Specs:** Accordion or tab layout rendering specs from specs_json field (key-value pairs)
- [ ] **PD-04 - Product Documents:** Download links for PDF files: Data Sheet, User Manual, Brochure (from ProductDocument model)
- [ ] **PD-05 - Shipping Info:** Section showing: availability, estimated delivery time, coverage areas
- [ ] **PD-06 - RFQ CTA Button:** Prominent sticky "Request a Quote" button that stays visible on scroll - MOST IMPORTANT ELEMENT
- [ ] **PD-07 - Wishlist Button:** "Add to Wishlist" button
- [ ] **PD-08 - Compare Button:** "Compare with another product" button activating compare mode
- [ ] **PD-09 - Related Products:** "You may also like" section showing products from same category (3-4 cards)
- [ ] Track product views (increment views_count on each visit)
- [ ] SEO: Meta title, description, Schema.org Product markup (SEO-01, SEO-02, SEO-03)

**Deliverable:** Complete product detail page with gallery, specs, documents, and all interactive features.

---

### PHASE 5: RFQ (Request for Quote) System
**Duration: 4 days**
**Priority: Critical**

#### Tasks:

**RFQ Form (RFQ-01 to RFQ-08):**
- [ ] **RFQ-03 - Linked Product:** If coming from a product page, show product image and name pre-filled at top of form
- [ ] **RFQ-01 - Client Data Fields:**
  - Full Name (required)
  - Email (required)
  - Phone Number (required)
  - Company Name (required)
- [ ] **RFQ-02 - Additional Notes:** Free text field for special requirements
- [ ] **RFQ-04 - Validation:** Client-side + server-side validation with clear Arabic error messages for email format and phone format
- [ ] **RFQ-08 - Privacy:** Privacy policy link + checkbox consent before submission
- [ ] **RFQ-05 - Confirmation Message:** After submit: "Thank you" page with confirmation message and expected response time
- [ ] **RFQ-06 - Client Email Notification:** Automatic email to client confirming receipt with reference number (using Flask-Mail)
- [ ] **RFQ-07 - Admin Notification:** Email sent to Sama Tech team (info@samatech-mea.com) on new RFQ + appears in admin dashboard
- [ ] Generate unique reference number per RFQ (e.g., RFQ-2026-0001)
- [ ] SPAM protection with reCAPTCHA (RISK-03)
- [ ] Bulk RFQ from wishlist page (request quote for all wishlisted products at once - WL-02)

**Deliverable:** Complete RFQ flow with form validation, email notifications, and spam protection.

---

### PHASE 6: Compare & Wishlist Features
**Duration: 3 days**
**Priority: High**

#### Tasks:

**Product Comparison (CMP-01 to CMP-03):**
- [ ] **CMP-01 - Product Selection:** Allow selecting up to 2 products from catalog or detail pages
- [ ] **CMP-02 - Compare View:** Side-by-side comparison table showing: image, name, brand, key specs, individual RFQ button per product
- [ ] **CMP-03 - Remove/Replace:** X button to remove a product from comparison and select another
- [ ] Sticky compare bar at bottom of screen showing selected products with "Compare Now" button
- [ ] Compare state stored in localStorage

**Wishlist (WL-01 to WL-03):**
- [ ] **WL-01 - Add/Remove:** One-click toggle on product cards and detail pages with heart animation
- [ ] **WL-02 - Wishlist Page:** Dedicated page showing all saved products with option to "Request Quote for All" (bulk RFQ)
- [ ] **WL-03 - Local Storage:** All wishlist data persisted in localStorage for non-registered users
- [ ] Wishlist counter in navbar updates in real-time

**Deliverable:** Fully functional compare and wishlist features with localStorage persistence.

---

### PHASE 7: Admin Dashboard - Authentication & Products
**Duration: 5 days**
**Priority: Critical**

#### Tasks:

**Admin Auth (ADM-10):**
- [ ] Secure login page (/admin/login) with Flask-Login
- [ ] Session management with remember me option
- [ ] All /admin/* routes protected with @login_required
- [ ] Password hashing with werkzeug.security

**Product Management (ADM-01):**
- [ ] Products list page with search, filter by category/brand, pagination
- [ ] Add new product form:
  - Name (Arabic), SKU, Category (dropdown), Subcategory (dynamic), Brand (dropdown)
  - Short description, Full description (rich text or textarea)
  - Technical specs (dynamic key-value pair fields)
  - Multiple image upload with drag-and-drop, set primary image, reorder
  - Document upload (Data Sheet, Manual, Brochure - PDF)
  - Shipping info override
  - Is Featured toggle, Is Active toggle
- [ ] Edit product (pre-filled form)
- [ ] Delete product (soft delete / confirmation dialog)
- [ ] Hide/Show product (is_active toggle)
- [ ] Image validation: minimum resolution check (RISK-02)
- [ ] Bulk actions: activate, deactivate, delete selected

**Homepage Control (ADM-02):**
- [ ] Select which products appear as featured on homepage
- [ ] Drag-and-drop reorder of featured products
- [ ] Set hero section content (headline, CTA text)
- [ ] Update social proof numbers (years, clients, products, coverage)

**Deliverable:** Secure admin login and full product CRUD with image/document management.

---

### PHASE 8: Admin Dashboard - Categories, Brands & Orders
**Duration: 4 days**
**Priority: Critical**

#### Tasks:

**Category Management (ADM-03):**
- [ ] List all categories with subcategories (tree view)
- [ ] Add/Edit main category (name_ar, icon, slug)
- [ ] Add/Edit subcategory under parent
- [ ] Reorder categories (sort_order)
- [ ] Show product count per category

**Brand Management (ADM-04):**
- [ ] List all brands with logos
- [ ] Add/Edit brand (name, logo upload, description_ar, website URL)
- [ ] Show product count per brand

**Order Management (ADM-05 to ADM-08):**
- [ ] **ADM-05 - Orders List:** Table showing all RFQ requests with: ref number, client name, company, product, date, status badge
- [ ] **ADM-06 - Status Management:** Change status dropdown: New (جديد), Under Review (قيد المراجعة), Replied (تم الرد), Closed (مغلق)
- [ ] **ADM-07 - Admin Notes:** Internal notes textarea on each order (not visible to client)
- [ ] **ADM-08 - Export to Excel:** Export filtered orders as .xlsx file using openpyxl (columns: ref, name, email, phone, company, product, status, date, notes)
- [ ] Order detail page showing full client info + product info + timeline
- [ ] Filter orders by status, date range, product, search by client name/email
- [ ] Dashboard summary: total orders, new orders count, orders this month

**Shipping Info Management (ADM-09):**
- [ ] Edit delivery areas, estimated days, coverage regions displayed on product pages

**Deliverable:** Complete admin dashboard with all management features and Excel export.

---

### PHASE 9: SEO, Performance & Polish
**Duration: 3 days**
**Priority: High**

#### Tasks:

**SEO (SEO-01 to SEO-04):**
- [ ] **SEO-01 - Friendly URLs:** Pattern: `/ar/products/category-slug/product-slug/`
- [ ] **SEO-02 - Meta Tags:** Dynamic meta title and description per product, category, and page
- [ ] **SEO-03 - Schema.org Markup:** JSON-LD Product schema on product detail pages (name, sku, brand, image, description, category)
- [ ] **SEO-04 - XML Sitemap:** Auto-generated sitemap at `/sitemap.xml` listing all products, categories, and static pages
- [ ] robots.txt file
- [ ] Canonical URLs on all pages
- [ ] Open Graph tags for social sharing

**Performance:**
- [ ] Image optimization on upload (resize, compress with Pillow)
- [ ] Lazy loading for product images in catalog
- [ ] Database query optimization with proper indexes (RISK-01)
- [ ] Pagination to handle 500+ products efficiently
- [ ] Static file caching headers
- [ ] Minify CSS/JS for production

**UX Polish:**
- [ ] **UX-01 - Responsive:** Test and fix on Desktop, Tablet, Mobile
- [ ] **UX-02 - RTL:** Verify all text direction, alignment, and layout is correct RTL
- [ ] **UX-03 - Toast Notifications:** Smooth toast messages for: added to wishlist, added to compare, RFQ submitted
- [ ] **UX-04 - Loading States:** Skeleton loaders or spinners during AJAX filter/search
- [ ] **UX-05 - Empty States:** Friendly Arabic messages with illustrations for empty search/filter results
- [ ] 404 and 500 error pages (Arabic, styled)
- [ ] Favicon and app icons

**Deliverable:** SEO-optimized, performant, polished application ready for testing.

---

### PHASE 10: Testing, Security & Deployment
**Duration: 3 days**
**Priority: Critical**

#### Tasks:

**Testing:**
- [ ] Test all forms with valid/invalid data
- [ ] Test RFQ email flow (client + admin notifications)
- [ ] Test all filters, search, sort, pagination combinations
- [ ] Test wishlist and compare across browser sessions
- [ ] Test admin CRUD operations (create, edit, delete products/categories/brands)
- [ ] Test order status workflow
- [ ] Test Excel export with various data
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile responsiveness testing on real devices
- [ ] RTL layout verification on all pages

**Security:**
- [ ] CSRF protection on all forms (Flask-WTF)
- [ ] Input sanitization to prevent XSS
- [ ] SQL injection prevention (SQLAlchemy ORM handles this)
- [ ] Secure file upload validation (allowed extensions, file size limits)
- [ ] Admin route protection
- [ ] Rate limiting on RFQ form
- [ ] reCAPTCHA integration on RFQ form
- [ ] Secure session configuration (httponly, secure cookies)
- [ ] Environment variables for secrets (SECRET_KEY, MAIL_PASSWORD, etc.)

**Deployment Prep:**
- [ ] Switch to PostgreSQL for production
- [ ] Configure Flask-Mail with production SMTP (for info@samatech-mea.com)
- [ ] Setup WSGI with Gunicorn
- [ ] Nginx reverse proxy configuration
- [ ] SSL/HTTPS setup
- [ ] Environment-based config (dev/staging/prod)
- [ ] Database backup strategy
- [ ] Upload to production server

**Deliverable:** Fully tested, secure, deployed production application.

---

## Phase Summary

| Phase | Name | Duration | Priority |
|-------|------|----------|----------|
| 1 | Project Setup & Database | 3 days | Critical |
| 2 | Base Layout & Homepage | 4 days | Critical |
| 3 | Product Catalog | 5 days | Critical |
| 4 | Product Detail Page | 4 days | Critical |
| 5 | RFQ System | 4 days | Critical |
| 6 | Compare & Wishlist | 3 days | High |
| 7 | Admin - Auth & Products | 5 days | Critical |
| 8 | Admin - Categories, Brands & Orders | 4 days | Critical |
| 9 | SEO, Performance & Polish | 3 days | High |
| 10 | Testing, Security & Deployment | 3 days | Critical |
| **Total** | | **38 days** | |

---

## Risk Mitigation

| Code | Risk | Severity | Mitigation |
|------|------|----------|------------|
| RISK-01 | Catalog exceeds 500+ products, performance degrades | Medium | Database indexing + pagination + lazy loading |
| RISK-02 | Low-quality images uploaded by admin | Medium | Set minimum resolution (800x600), auto-resize on upload |
| RISK-03 | SPAM abuse on RFQ form | High | reCAPTCHA mandatory + rate limiting |
| RISK-04 | Team stops updating catalog | High | Simple admin CMS interface + staff training |

---

## Dependencies / Requirements

```
Flask==3.1.*
Flask-SQLAlchemy==3.1.*
Flask-Migrate==4.*
Flask-Login==0.6.*
Flask-WTF==1.2.*
Flask-Mail==0.10.*
Pillow==11.*
openpyxl==3.1.*
python-slugify==8.*
gunicorn==23.*
psycopg2-binary==2.9.*
email-validator==2.*
```

---

*Document prepared: April 2026*
*Production Manager Plan - All requirements traced to source documents*
