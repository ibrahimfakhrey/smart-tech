"""
Comprehensive Playwright E2E Test Suite for Sama Technology Web App.
Generates HTML report with screenshots for every test.

Run:
    python3 test_app.py
"""
import os
import re
import time
import json
import html as html_lib
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

BASE = 'http://127.0.0.1:5000'
ADMIN_USER = 'admin'
ADMIN_PASS = 'SamaTech2026!'
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'test_reports', 'screenshots')
REPORT_DIR = os.path.join(os.path.dirname(__file__), 'test_reports')
RESULTS = []
TEST_NUM = 0


def setup_dirs():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)


def run_test(name, fn, page, timeout=15):
    global TEST_NUM
    TEST_NUM += 1
    num = f'{TEST_NUM:02d}'
    screenshot_name = f'{num}_{name.replace(" ", "_").replace("/", "_")}.png'
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
    start = time.time()
    try:
        fn(page)
        # Take screenshot on success
        page.screenshot(path=screenshot_path, full_page=False)
        duration = round(time.time() - start, 2)
        RESULTS.append({'num': num, 'name': name, 'passed': True, 'error': '', 'screenshot': screenshot_name, 'duration': duration})
        print(f'  ✅ {num}. {name} ({duration}s)')
    except Exception as e:
        # Take screenshot on failure too
        try:
            page.screenshot(path=screenshot_path, full_page=False)
        except:
            pass
        duration = round(time.time() - start, 2)
        error_msg = str(e)[:200]
        RESULTS.append({'num': num, 'name': name, 'passed': False, 'error': error_msg, 'screenshot': screenshot_name, 'duration': duration})
        print(f'  ❌ {num}. {name} ({duration}s) — {error_msg[:80]}')


def generate_report():
    passed = sum(1 for r in RESULTS if r['passed'])
    failed = sum(1 for r in RESULTS if not r['passed'])
    total = len(RESULTS)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    rows = ''
    for r in RESULTS:
        status_class = 'pass' if r['passed'] else 'fail'
        status_icon = '✅' if r['passed'] else '❌'
        error_html = f'<div class="error">{html_lib.escape(r["error"])}</div>' if r['error'] else ''
        rows += f'''
        <div class="test-card {status_class}">
            <div class="test-header">
                <span class="status">{status_icon}</span>
                <span class="test-name">{r['num']}. {html_lib.escape(r['name'])}</span>
                <span class="duration">{r['duration']}s</span>
            </div>
            {error_html}
            <div class="screenshot-container">
                <img src="screenshots/{r['screenshot']}" alt="{html_lib.escape(r['name'])}" loading="lazy" onclick="this.classList.toggle('expanded')">
            </div>
        </div>
        '''

    report_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير اختبار سما تكنولوجي</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Tajawal, sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }}
        .header {{ text-align: center; padding: 40px 20px; margin-bottom: 30px; background: linear-gradient(135deg, #0891b2, #7c3aed); border-radius: 16px; }}
        .header h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        .header .date {{ opacity: 0.8; font-size: 0.9rem; }}
        .stats {{ display: flex; gap: 16px; justify-content: center; margin: 20px 0 30px; flex-wrap: wrap; }}
        .stat {{ background: #1e293b; padding: 20px 30px; border-radius: 12px; text-align: center; min-width: 150px; }}
        .stat .number {{ font-size: 2.5rem; font-weight: 900; }}
        .stat .label {{ font-size: 0.85rem; opacity: 0.7; margin-top: 4px; }}
        .stat.total .number {{ color: #38bdf8; }}
        .stat.passed .number {{ color: #4ade80; }}
        .stat.failed .number {{ color: #f87171; }}
        .progress-bar {{ width: 100%; height: 8px; background: #334155; border-radius: 4px; margin-bottom: 30px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4ade80, #22d3ee); border-radius: 4px; transition: width 0.5s; }}
        .filter-bar {{ display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }}
        .filter-btn {{ padding: 8px 20px; border-radius: 20px; border: 1px solid #334155; background: transparent; color: #e2e8f0; cursor: pointer; font-size: 0.9rem; }}
        .filter-btn:hover, .filter-btn.active {{ background: #7c3aed; border-color: #7c3aed; }}
        .test-card {{ background: #1e293b; border-radius: 12px; margin-bottom: 12px; overflow: hidden; border-right: 4px solid; }}
        .test-card.pass {{ border-right-color: #4ade80; }}
        .test-card.fail {{ border-right-color: #f87171; }}
        .test-header {{ display: flex; align-items: center; gap: 12px; padding: 16px 20px; }}
        .test-name {{ flex: 1; font-weight: 500; }}
        .duration {{ font-size: 0.8rem; opacity: 0.6; }}
        .error {{ padding: 0 20px 12px; color: #f87171; font-size: 0.85rem; font-family: monospace; word-break: break-all; }}
        .screenshot-container {{ padding: 0 20px 16px; }}
        .screenshot-container img {{ width: 100%; border-radius: 8px; cursor: pointer; transition: all 0.3s; border: 1px solid #334155; max-height: 200px; object-fit: cover; object-position: top; }}
        .screenshot-container img:hover {{ border-color: #7c3aed; }}
        .screenshot-container img.expanded {{ max-height: none; object-fit: contain; }}
        .section-title {{ font-size: 1.3rem; font-weight: 700; padding: 20px 0 12px; color: #38bdf8; border-bottom: 1px solid #334155; margin-bottom: 16px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 تقرير اختبار سما تكنولوجي</h1>
        <div class="date">Sama Technology — E2E Test Report — {now}</div>
    </div>

    <div class="stats">
        <div class="stat total"><div class="number">{total}</div><div class="label">إجمالي الاختبارات</div></div>
        <div class="stat passed"><div class="number">{passed}</div><div class="label">ناجح</div></div>
        <div class="stat failed"><div class="number">{failed}</div><div class="label">فاشل</div></div>
    </div>

    <div class="progress-bar"><div class="progress-fill" style="width:{round(passed/total*100) if total else 0}%"></div></div>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterTests('all')">الكل ({total})</button>
        <button class="filter-btn" onclick="filterTests('pass')">ناجح ({passed})</button>
        <button class="filter-btn" onclick="filterTests('fail')">فاشل ({failed})</button>
    </div>

    <div id="testResults">
        {rows}
    </div>

    <script>
    function filterTests(type) {{
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');
        document.querySelectorAll('.test-card').forEach(c => {{
            if (type === 'all') c.style.display = '';
            else if (type === 'pass') c.style.display = c.classList.contains('pass') ? '' : 'none';
            else c.style.display = c.classList.contains('fail') ? '' : 'none';
        }});
    }}
    </script>
</body>
</html>'''

    report_path = os.path.join(REPORT_DIR, 'report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    return report_path


# ═══════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════

def admin_login(page):
    """Login to admin. Skips if already authenticated."""
    page.goto(BASE + '/admin/', wait_until='networkidle', timeout=10000)
    # If we're not redirected to login, we're already authenticated
    if '/login' not in page.url:
        return
    page.fill('input[name="username"]', ADMIN_USER)
    page.fill('input[name="password"]', ADMIN_PASS)
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle', timeout=10000)


def safe_goto(page, url):
    """Navigate with timeout safety."""
    page.goto(url, wait_until='domcontentloaded', timeout=10000)
    page.wait_for_timeout(300)


# ═══════════════════════════════════════════════════
#  1. PUBLIC PAGES
# ═══════════════════════════════════════════════════

def test_homepage_loads(page):
    resp = page.goto(BASE + '/', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_homepage_navbar(page):
    safe_goto(page, BASE + '/')
    assert page.locator('#mainNav').is_visible()

def test_homepage_navbar_scroll(page):
    safe_goto(page, BASE + '/')
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_timeout(300)
    nav = page.locator('#mainNav')
    cls_before = nav.get_attribute('class') or ''
    page.evaluate('window.scrollTo(0, 200)')
    page.wait_for_timeout(500)
    cls_after = nav.get_attribute('class') or ''
    assert 'scrolled' in cls_after

def test_homepage_newsletter(page):
    safe_goto(page, BASE + '/')
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_timeout(500)
    email_input = page.locator('input[name="email"]').last
    if email_input.is_visible():
        email_input.fill(f'pwtest_{int(time.time())}@example.com')
        btn = email_input.locator('xpath=ancestor::form//button[contains(@type,"submit")]')
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(1500)

def test_about_page(page):
    resp = page.goto(BASE + '/about', wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    assert 'سما' in page.content()

def test_contact_page(page):
    resp = page.goto(BASE + '/contact', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_privacy_page(page):
    resp = page.goto(BASE + '/privacy', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_robots_txt(page):
    safe_goto(page, BASE + '/robots.txt')
    assert 'Disallow: /admin/' in page.content()

def test_sitemap_xml(page):
    safe_goto(page, BASE + '/sitemap.xml')
    assert '<urlset' in page.content()

def test_404_page(page):
    resp = page.goto(BASE + '/nonexistent-page-xyz', wait_until='networkidle', timeout=10000)
    assert resp.status == 404

def test_security_headers(page):
    resp = page.goto(BASE + '/', wait_until='networkidle', timeout=10000)
    assert resp.headers.get('x-content-type-options') == 'nosniff'
    assert resp.headers.get('x-frame-options') == 'SAMEORIGIN'


# ═══════════════════════════════════════════════════
#  2. CATALOG
# ═══════════════════════════════════════════════════

def test_catalog_loads(page):
    safe_goto(page, BASE + '/ar/products/')
    assert page.locator('.product-card').count() > 0

def test_catalog_search(page):
    safe_goto(page, BASE + '/ar/products/?q=Yealink')
    assert page.locator('.product-card').count() >= 1

def test_catalog_sort_name(page):
    resp = page.goto(BASE + '/ar/products/?sort=name', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_catalog_sort_views(page):
    resp = page.goto(BASE + '/ar/products/?sort=views', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_catalog_filter_brand(page):
    resp = page.goto(BASE + '/ar/products/?brand=yealink', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_category_page(page):
    resp = page.goto(BASE + '/ar/products/interactive-screens/', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_product_detail(page):
    safe_goto(page, BASE + '/ar/products/')
    link = page.locator('.product-card a[href*="/ar/products/"]').first
    href = link.get_attribute('href')
    resp = page.goto(BASE + href, wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    assert page.locator('h1').count() >= 1

def test_product_rfq_button(page):
    safe_goto(page, BASE + '/ar/products/')
    link = page.locator('.product-card a[href*="/ar/products/"]').first
    page.goto(BASE + link.get_attribute('href'), wait_until='networkidle', timeout=10000)
    rfq = page.locator('a[href*="/rfq/request/"]')
    assert rfq.count() >= 1


# ═══════════════════════════════════════════════════
#  3. SEARCH OVERLAY
# ═══════════════════════════════════════════════════

def test_search_open_close(page):
    safe_goto(page, BASE + '/')
    toggle = page.locator('#searchToggle')
    if toggle.count() > 0:
        toggle.click()
        page.wait_for_timeout(400)
        overlay = page.locator('#searchOverlay')
        assert 'active' in (overlay.get_attribute('class') or '')
        page.keyboard.press('Escape')
        page.wait_for_timeout(400)

def test_search_live_results(page):
    safe_goto(page, BASE + '/')
    toggle = page.locator('#searchToggle')
    if toggle.count() > 0:
        toggle.click()
        page.wait_for_timeout(400)
        page.locator('#globalSearchInput').fill('Yealink')
        page.wait_for_timeout(1500)
        results_html = page.locator('#searchResults').inner_html()
        assert len(results_html) > 10, 'Live search returned no results'

def test_search_api(page):
    safe_goto(page, BASE + '/ar/products/api/search?q=MAXHUB')
    text = page.inner_text('body')
    data = json.loads(text)
    assert isinstance(data, list) and len(data) >= 1


# ═══════════════════════════════════════════════════
#  4. WISHLIST
# ═══════════════════════════════════════════════════

def test_wishlist_add(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.clear()')
    page.wait_for_timeout(200)
    btn = page.locator('.wishlist-btn').first
    pid = btn.get_attribute('data-product-id')
    btn.click()
    page.wait_for_timeout(500)
    stored = page.evaluate('JSON.parse(localStorage.getItem("samatech_wishlist") || "[]")')
    assert any(str(i['id']) == str(pid) for i in stored)

def test_wishlist_badge(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.setItem("samatech_wishlist", JSON.stringify([{id:1,name:"Test"}]))')
    page.reload(wait_until='networkidle', timeout=10000)
    page.wait_for_timeout(300)
    badge = page.locator('#wishlistCount')
    assert badge.inner_text() == '1'

def test_wishlist_page(page):
    safe_goto(page, BASE + '/ar/products/')
    # Set a real product in wishlist
    btn = page.locator('.wishlist-btn').first
    pid = btn.get_attribute('data-product-id')
    pname = btn.get_attribute('data-product-name') or 'Test'
    page.evaluate(f'localStorage.setItem("samatech_wishlist", JSON.stringify([{{id:{pid},name:"{pname}"}}]))')
    resp = page.goto(BASE + '/ar/products/wishlist', wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    page.wait_for_timeout(1500)


# ═══════════════════════════════════════════════════
#  5. COMPARE
# ═══════════════════════════════════════════════════

def test_compare_add(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.clear()')
    page.wait_for_timeout(200)
    btn = page.locator('.compare-btn').first
    btn.click()
    page.wait_for_timeout(500)
    stored = page.evaluate('JSON.parse(localStorage.getItem("samatech_compare") || "[]")')
    assert len(stored) == 1

def test_compare_bar_visible(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.setItem("samatech_compare", JSON.stringify([{id:1,name:"A"}]))')
    page.reload(wait_until='networkidle', timeout=10000)
    page.wait_for_timeout(500)
    bar = page.locator('#compareBar')
    assert 'active' in (bar.get_attribute('class') or '')

def test_compare_max_two(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.setItem("samatech_compare", JSON.stringify([{id:1,name:"A"},{id:2,name:"B"}]))')
    page.reload(wait_until='networkidle', timeout=10000)
    page.wait_for_timeout(300)
    # Try adding a third
    btns = page.locator('.compare-btn')
    if btns.count() >= 3:
        btns.nth(2).click()
        page.wait_for_timeout(500)
        stored = page.evaluate('JSON.parse(localStorage.getItem("samatech_compare") || "[]")')
        assert len(stored) <= 2

def test_compare_navigate(page):
    safe_goto(page, BASE + '/ar/products/')
    # Get two real product IDs
    btns = page.locator('.compare-btn')
    items = []
    for i in range(min(2, btns.count())):
        pid = btns.nth(i).get_attribute('data-product-id')
        pname = btns.nth(i).get_attribute('data-product-name') or f'P{i}'
        items.append(f'{{id:{pid},name:"{pname}"}}')
    js_arr = '[' + ','.join(items) + ']'
    page.evaluate(f'localStorage.setItem("samatech_compare", JSON.stringify({js_arr}))')
    page.reload(wait_until='networkidle', timeout=10000)
    page.wait_for_timeout(500)
    compare_btn = page.locator('#compareNowBtn')
    if compare_btn.is_visible():
        compare_btn.click()
        page.wait_for_timeout(1000)
        assert '/compare' in page.url

def test_compare_page(page):
    resp = page.goto(BASE + '/ar/products/compare?ids=1,2', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_compare_clear(page):
    safe_goto(page, BASE + '/ar/products/')
    page.evaluate('localStorage.setItem("samatech_compare", JSON.stringify([{id:1,name:"A"}]))')
    page.reload(wait_until='networkidle', timeout=10000)
    page.wait_for_timeout(500)
    clear_btn = page.locator('#clearCompareBtn')
    if clear_btn.is_visible():
        clear_btn.click()
        page.wait_for_timeout(500)
        stored = page.evaluate('JSON.parse(localStorage.getItem("samatech_compare") || "[]")')
        assert len(stored) == 0


# ═══════════════════════════════════════════════════
#  6. RFQ
# ═══════════════════════════════════════════════════

def test_rfq_form_loads(page):
    resp = page.goto(BASE + '/rfq/request/1', wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    assert page.locator('form').count() >= 1

def test_rfq_submit(page):
    safe_goto(page, BASE + '/rfq/request/1')
    page.fill('input[name="full_name"]', 'مختبر بلايرايت')
    page.fill('input[name="email"]', 'pw@test.sa')
    page.fill('input[name="phone"]', '0551234567')
    page.fill('input[name="company_name"]', 'شركة اختبار')
    notes = page.locator('textarea[name="notes"]')
    if notes.count() > 0:
        notes.fill('اختبار Playwright')
    privacy = page.locator('input[name="privacy_accepted"]')
    if privacy.count() > 0:
        privacy.check()
    submit_btn = page.locator('form button[type="submit"]').last
    submit_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    submit_btn.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    content = page.content()
    assert 'RFQ-' in content or 'تم' in content or 'شكر' in content

def test_rfq_from_product(page):
    safe_goto(page, BASE + '/ar/products/')
    link = page.locator('.product-card a[href*="/ar/products/"]').first
    page.goto(BASE + link.get_attribute('href'), wait_until='networkidle', timeout=10000)
    rfq = page.locator('a[href*="/rfq/request/"]').first
    if rfq.count() > 0:
        rfq.click()
        page.wait_for_load_state('networkidle', timeout=10000)
        assert '/rfq/request/' in page.url


# ═══════════════════════════════════════════════════
#  7. STICKY CTA
# ═══════════════════════════════════════════════════

def test_sticky_cta(page):
    safe_goto(page, BASE + '/')
    cta = page.locator('#stickyCta')
    if cta.count() > 0:
        page.evaluate('window.scrollTo(0, 600)')
        page.wait_for_timeout(600)
        assert 'visible' in (cta.get_attribute('class') or '')


# ═══════════════════════════════════════════════════
#  8. API ENDPOINTS
# ═══════════════════════════════════════════════════

def test_api_products_by_ids(page):
    safe_goto(page, BASE + '/ar/products/api/products-by-ids?ids=1,2')
    data = json.loads(page.inner_text('body'))
    assert isinstance(data, list)


# ═══════════════════════════════════════════════════
#  9. MOBILE RESPONSIVE
# ═══════════════════════════════════════════════════

def test_mobile_homepage(page):
    page.set_viewport_size({'width': 375, 'height': 812})
    resp = page.goto(BASE + '/', wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    toggler = page.locator('.navbar-toggler')
    if toggler.count() > 0:
        assert toggler.is_visible()
    page.set_viewport_size({'width': 1280, 'height': 720})

def test_mobile_catalog(page):
    page.set_viewport_size({'width': 375, 'height': 812})
    resp = page.goto(BASE + '/ar/products/', wait_until='networkidle', timeout=10000)
    assert resp.status == 200
    page.set_viewport_size({'width': 1280, 'height': 720})


# ═══════════════════════════════════════════════════
#  10. ADMIN - AUTH
# ═══════════════════════════════════════════════════

def test_admin_login_page(page):
    resp = page.goto(BASE + '/admin/login', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_wrong_password(page):
    safe_goto(page, BASE + '/admin/login')
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'wrong')
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle', timeout=10000)
    assert '/admin/login' in page.url or 'غير صحيحة' in page.content()

def test_admin_redirect_unauth(page):
    safe_goto(page, BASE + '/admin/')
    assert 'login' in page.url

def test_admin_login_success(page):
    admin_login(page)
    assert '/admin' in page.url and 'login' not in page.url

def test_admin_dashboard(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/', wait_until='networkidle', timeout=10000)
    assert resp.status == 200


# ═══════════════════════════════════════════════════
#  11. ADMIN - PRODUCTS
# ═══════════════════════════════════════════════════

def test_admin_products_list(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/products', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_products_search(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/products?q=Yealink', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_product_add(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/products/add')
    page.fill('input[name="name_ar"]', 'منتج اختبار بلايرايت')
    page.fill('input[name="sku"]', f'PW-{int(time.time())}')
    cat = page.locator('select[name="category_id"]')
    if cat.count() > 0:
        cat.select_option(index=1)
    brand = page.locator('select[name="brand_id"]')
    if brand.count() > 0:
        brand.select_option(index=1)
    desc = page.locator('textarea[name="short_description_ar"]')
    if desc.count() > 0:
        desc.fill('وصف اختبار')
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle', timeout=10000)

def test_admin_product_edit(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/products/edit/1', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_product_toggle(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/products')
    toggle = page.locator('form[action*="toggle"] button').first
    if toggle.count() > 0:
        toggle.click()
        page.wait_for_load_state('networkidle', timeout=10000)


# ═══════════════════════════════════════════════════
#  12. ADMIN - CATEGORIES
# ═══════════════════════════════════════════════════

def test_admin_categories(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/categories', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_category_add(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/categories')
    name_input = page.locator('input[name="name_ar"]').first
    if name_input.count() > 0 and name_input.is_visible():
        name_input.fill('تصنيف اختبار بلايرايت')
        en = page.locator('input[name="name_en"]').first
        if en.count() > 0 and en.is_visible():
            en.fill('Playwright Test Cat')
        page.locator('form:has(input[name="name_ar"]) button[type="submit"]').first.click()
        page.wait_for_load_state('networkidle', timeout=10000)


# ═══════════════════════════════════════════════════
#  13. ADMIN - BRANDS
# ═══════════════════════════════════════════════════

def test_admin_brands(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/brands', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_brand_add(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/brands')
    name_input = page.locator('input[name="name"]').first
    if name_input.count() > 0 and name_input.is_visible():
        name_input.fill(f'PW-Brand-{int(time.time())}')
        page.locator('form:has(input[name="name"]) button[type="submit"]').first.click()
        page.wait_for_load_state('networkidle', timeout=10000)


# ═══════════════════════════════════════════════════
#  14. ADMIN - ORDERS
# ═══════════════════════════════════════════════════

def test_admin_orders_list(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/orders', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_orders_filter(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/orders?status=new', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_orders_search(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/orders?q=أحمد', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_order_detail(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/orders/1', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_order_status_update(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/orders/1')
    sel = page.locator('select[name="status"]')
    if sel.count() > 0:
        sel.select_option('reviewing')
        page.locator('form:has(select[name="status"]) button').first.click()
        page.wait_for_load_state('networkidle', timeout=10000)

def test_admin_order_notes(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/orders/1')
    notes = page.locator('textarea[name="admin_notes"]')
    if notes.count() > 0:
        notes.fill('ملاحظة اختبار Playwright')
        page.locator('form:has(textarea[name="admin_notes"]) button').first.click()
        page.wait_for_load_state('networkidle', timeout=10000)

def test_admin_orders_export(page):
    admin_login(page)
    safe_goto(page, BASE + '/admin/orders')
    # Use JS to trigger download via a hidden link
    with page.expect_download(timeout=10000) as dl:
        page.evaluate(f'window.location.href = "{BASE}/admin/orders/export"')
    download = dl.value
    assert download.suggested_filename.endswith('.xlsx')


# ═══════════════════════════════════════════════════
#  15. ADMIN - SETTINGS
# ═══════════════════════════════════════════════════

def test_admin_homepage_settings(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/homepage', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_shipping_settings(page):
    admin_login(page)
    resp = page.goto(BASE + '/admin/shipping', wait_until='networkidle', timeout=10000)
    assert resp.status == 200

def test_admin_logout(page):
    admin_login(page)
    page.goto(BASE + '/admin/logout', wait_until='networkidle', timeout=10000)
    assert 'login' in page.url


# ═══════════════════════════════════════════════════
#  RUNNER
# ═══════════════════════════════════════════════════

def main():
    setup_dirs()

    print('=' * 60)
    print('  سما تكنولوجي - Playwright E2E Test Suite')
    print('  Screenshots + HTML Report')
    print('=' * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={'width': 1280, 'height': 720}, locale='ar-SA')
        page = context.new_page()
        page.set_default_timeout(10000)

        # ── PUBLIC ──
        print('\n📄 Public Pages')
        run_test('Homepage loads', test_homepage_loads, page)
        run_test('Navbar visible', test_homepage_navbar, page)
        run_test('Navbar scroll effect', test_homepage_navbar_scroll, page)
        run_test('Newsletter subscribe', test_homepage_newsletter, page)
        run_test('About page', test_about_page, page)
        run_test('Contact page', test_contact_page, page)
        run_test('Privacy page', test_privacy_page, page)
        run_test('robots.txt', test_robots_txt, page)
        run_test('sitemap.xml', test_sitemap_xml, page)
        run_test('404 error page', test_404_page, page)
        run_test('Security headers', test_security_headers, page)

        # ── CATALOG ──
        print('\n🛒 Catalog & Products')
        run_test('Catalog loads', test_catalog_loads, page)
        run_test('Catalog search', test_catalog_search, page)
        run_test('Sort by name', test_catalog_sort_name, page)
        run_test('Sort by views', test_catalog_sort_views, page)
        run_test('Filter by brand', test_catalog_filter_brand, page)
        run_test('Category page', test_category_page, page)
        run_test('Product detail', test_product_detail, page)
        run_test('Product RFQ button', test_product_rfq_button, page)

        # ── SEARCH ──
        print('\n🔍 Search')
        run_test('Search open/close', test_search_open_close, page)
        run_test('Live search results', test_search_live_results, page)
        run_test('Search API', test_search_api, page)

        # ── WISHLIST ──
        print('\n♥ Wishlist')
        page.evaluate('localStorage.clear()')
        run_test('Add to wishlist', test_wishlist_add, page)
        run_test('Wishlist badge', test_wishlist_badge, page)
        run_test('Wishlist page', test_wishlist_page, page)

        # ── COMPARE ──
        print('\n⚖ Compare')
        page.evaluate('localStorage.clear()')
        run_test('Add to compare', test_compare_add, page)
        run_test('Compare bar visible', test_compare_bar_visible, page)
        run_test('Max 2 compare', test_compare_max_two, page)
        run_test('Compare navigate', test_compare_navigate, page)
        page.evaluate('localStorage.clear()')
        run_test('Compare page', test_compare_page, page)
        run_test('Clear compare', test_compare_clear, page)

        # ── RFQ ──
        print('\n📋 RFQ')
        run_test('RFQ form loads', test_rfq_form_loads, page)
        run_test('RFQ submit', test_rfq_submit, page)
        run_test('RFQ from product', test_rfq_from_product, page)

        # ── MISC ──
        print('\n📌 UI Elements')
        run_test('Sticky CTA', test_sticky_cta, page)
        run_test('Products by IDs API', test_api_products_by_ids, page)

        # ── MOBILE ──
        print('\n📱 Mobile')
        run_test('Mobile homepage', test_mobile_homepage, page)
        run_test('Mobile catalog', test_mobile_catalog, page)

        context.close()

        # ── ADMIN ── (fresh context)
        admin_ctx = browser.new_context(viewport={'width': 1280, 'height': 720}, locale='ar-SA')
        page = admin_ctx.new_page()
        page.set_default_timeout(10000)

        print('\n🔐 Admin Auth')
        run_test('Admin login page', test_admin_login_page, page)
        run_test('Admin wrong password', test_admin_wrong_password, page)
        run_test('Admin redirect unauth', test_admin_redirect_unauth, page)
        run_test('Admin login success', test_admin_login_success, page)
        run_test('Admin dashboard', test_admin_dashboard, page)

        print('\n📦 Admin Products')
        run_test('Products list', test_admin_products_list, page)
        run_test('Products search', test_admin_products_search, page)
        run_test('Product add', test_admin_product_add, page)
        run_test('Product edit', test_admin_product_edit, page)
        run_test('Product toggle', test_admin_product_toggle, page)

        print('\n📂 Admin Categories')
        run_test('Categories list', test_admin_categories, page)
        run_test('Category add', test_admin_category_add, page)

        print('\n🏷 Admin Brands')
        run_test('Brands list', test_admin_brands, page)
        run_test('Brand add', test_admin_brand_add, page)

        print('\n📑 Admin Orders')
        run_test('Orders list', test_admin_orders_list, page)
        run_test('Orders filter', test_admin_orders_filter, page)
        run_test('Orders search', test_admin_orders_search, page)
        run_test('Order detail', test_admin_order_detail, page)
        run_test('Order status update', test_admin_order_status_update, page)
        run_test('Order add notes', test_admin_order_notes, page)
        run_test('Orders export Excel', test_admin_orders_export, page)

        print('\n⚙ Admin Settings')
        run_test('Homepage settings', test_admin_homepage_settings, page)
        run_test('Shipping settings', test_admin_shipping_settings, page)
        run_test('Admin logout', test_admin_logout, page)

        admin_ctx.close()
        browser.close()

    # Generate report
    report_path = generate_report()

    passed = sum(1 for r in RESULTS if r['passed'])
    failed = sum(1 for r in RESULTS if not r['passed'])
    total = len(RESULTS)

    print('\n' + '=' * 60)
    print(f'  RESULTS: {passed}/{total} passed, {failed} failed')
    print('=' * 60)

    if failed:
        print('\n❌ Failed:')
        for r in RESULTS:
            if not r['passed']:
                print(f'   • {r["name"]}: {r["error"][:80]}')

    print(f'\n📊 Report: {report_path}')
    print(f'📸 Screenshots: {SCREENSHOT_DIR}/')

    # Open report in browser
    import webbrowser
    webbrowser.open('file://' + os.path.abspath(report_path))


if __name__ == '__main__':
    main()
