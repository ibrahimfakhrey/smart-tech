/* ═══════════════════════════════════════════
   SAMA TECHNOLOGY - Main JavaScript
   ═══════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initSearch();
    initStickyCta();
    initWishlistUI();
    initCompareUI();
});

/* ─── Navbar Scroll Effect ─── */
function initNavbar() {
    const nav = document.getElementById('mainNav');
    if (!nav) return;

    function onScroll() {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

/* ─── Search Overlay ─── */
function initSearch() {
    const toggle = document.getElementById('searchToggle');
    const overlay = document.getElementById('searchOverlay');
    const closeBtn = document.getElementById('searchClose');
    const input = document.getElementById('globalSearchInput');
    const results = document.getElementById('searchResults');

    if (!toggle || !overlay) return;

    toggle.addEventListener('click', function() {
        overlay.classList.add('active');
        setTimeout(() => input.focus(), 200);
    });

    closeBtn.addEventListener('click', function() {
        overlay.classList.remove('active');
        results.innerHTML = '';
        input.value = '';
    });

    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            overlay.classList.remove('active');
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') overlay.classList.remove('active');
    });

    // Live search
    let searchTimer;
    input.addEventListener('input', function() {
        clearTimeout(searchTimer);
        const q = this.value.trim();
        if (q.length < 2) { results.innerHTML = ''; return; }

        searchTimer = setTimeout(function() {
            fetch('/ar/products/api/search?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        results.innerHTML = '<p style="color:rgba(255,255,255,0.5);text-align:center;padding:20px;">لا توجد نتائج</p>';
                        return;
                    }
                    results.innerHTML = data.map(function(p) {
                        const img = p.image
                            ? '/static/' + p.image
                            : 'https://placehold.co/50x50/e2e8f0/94a3b8?text=' + p.brand;
                        return '<a href="/ar/products/' + p.slug + '/" class="search-result-item">' +
                            '<img src="' + img + '" alt="">' +
                            '<div><strong>' + p.name + '</strong><br><small style="color:rgba(255,255,255,0.5);">' + p.brand + ' | ' + p.sku + '</small></div>' +
                            '</a>';
                    }).join('');
                })
                .catch(function() {
                    results.innerHTML = '';
                });
        }, 300);
    });
}

/* ─── Sticky CTA ─── */
function initStickyCta() {
    const cta = document.getElementById('stickyCta');
    if (!cta) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 400) {
            cta.classList.add('visible');
        } else {
            cta.classList.remove('visible');
        }
    }, { passive: true });
}

/* ─── Toast Notification (UX-03) ─── */
function showToast(message, type) {
    type = type || 'success';
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#0891b2'
    };

    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.setAttribute('role', 'alert');
    toast.innerHTML =
        '<div class="toast-body d-flex align-items-center gap-2" style="background:' + colors[type] + ';color:#fff;border-radius:12px;padding:12px 20px;">' +
        '<i class="bi ' + (type === 'success' ? 'bi-check-circle-fill' : type === 'error' ? 'bi-x-circle-fill' : 'bi-info-circle-fill') + '"></i>' +
        message +
        '</div>';

    container.appendChild(toast);
    setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
}

/* ─── Wishlist (localStorage) ─── */
function getWishlist() {
    try {
        return JSON.parse(localStorage.getItem('samatech_wishlist') || '[]');
    } catch(e) { return []; }
}

function saveWishlist(list) {
    localStorage.setItem('samatech_wishlist', JSON.stringify(list));
    updateWishlistCount();
}

function updateWishlistCount() {
    var count = getWishlist().length;
    var badge = document.getElementById('wishlistCount');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
    // Update all heart icons
    var wishlist = getWishlist();
    document.querySelectorAll('.wishlist-btn').forEach(function(btn) {
        var pid = String(btn.getAttribute('data-product-id'));
        var inList = wishlist.some(function(item) { return String(item.id) === pid; });
        if (inList) {
            btn.classList.add('active');
            btn.querySelector('i').className = 'bi bi-heart-fill';
        } else {
            btn.classList.remove('active');
            btn.querySelector('i').className = 'bi bi-heart';
        }
    });
}

function toggleWishlist(btn) {
    var id = btn.getAttribute('data-product-id');
    var name = btn.getAttribute('data-product-name');
    var wishlist = getWishlist();
    var index = wishlist.findIndex(function(item) { return String(item.id) === String(id); });

    if (index > -1) {
        wishlist.splice(index, 1);
        saveWishlist(wishlist);
        showToast('تم إزالة المنتج من المفضلة', 'info');
        // Reload if on wishlist page so removed item disappears
        if (window.location.pathname.includes('/wishlist')) {
            setTimeout(function() { window.location.reload(); }, 500);
        }
        return;
    } else {
        wishlist.push({ id: id, name: name });
        showToast('تم إضافة المنتج للمفضلة', 'success');
    }

    saveWishlist(wishlist);
}

function initWishlistUI() {
    updateWishlistCount();
}

function openWishlistPage(e) {
    e.preventDefault();
    window.location.href = '/ar/products/wishlist';
}

/* ─── Compare (localStorage, max 2) ─── */
function getCompareList() {
    try {
        return JSON.parse(localStorage.getItem('samatech_compare') || '[]');
    } catch(e) { return []; }
}

function saveCompareList(list) {
    localStorage.setItem('samatech_compare', JSON.stringify(list));
    updateCompareBar();
}

function toggleCompare(btn) {
    var id = btn.getAttribute('data-product-id');
    var name = btn.getAttribute('data-product-name');
    var list = getCompareList();
    var index = list.findIndex(function(item) { return String(item.id) === String(id); });

    if (index > -1) {
        list.splice(index, 1);
        showToast('تم إزالة المنتج من المقارنة', 'info');
    } else {
        if (list.length >= 2) {
            showToast('يمكنك مقارنة منتجين فقط', 'error');
            return;
        }
        list.push({ id: id, name: name });
        showToast('تم إضافة المنتج للمقارنة', 'success');
    }

    saveCompareList(list);
}

function updateCompareBar() {
    var list = getCompareList();
    var bar = document.getElementById('compareBar');
    var items = document.getElementById('compareItems');
    var compareBtn = document.getElementById('compareNowBtn');

    if (!bar) return;

    if (list.length === 0) {
        bar.classList.remove('active');
        bar.style.removeProperty('display');
        document.body.classList.remove('compare-active');
        return;
    }

    bar.classList.add('active');
    document.body.classList.add('compare-active');
    items.innerHTML = list.map(function(item) {
        return '<div class="compare-item">' +
            '<span>' + item.name.substring(0, 30) + '</span>' +
            '<button class="btn btn-sm text-white" onclick="removeCompareItem(\'' + item.id + '\')">&times;</button>' +
            '</div>';
    }).join('');

    if (compareBtn) {
        compareBtn.href = '/ar/products/compare?ids=' + list.map(function(i) { return i.id; }).join(',');
        if (list.length === 2) {
            compareBtn.classList.remove('disabled');
            compareBtn.classList.add('btn-primary');
        } else {
            compareBtn.classList.add('disabled');
            compareBtn.classList.remove('btn-primary');
            compareBtn.classList.add('btn-outline-light');
        }
    }

    // Update compare buttons
    document.querySelectorAll('.compare-btn').forEach(function(btn) {
        var pid = String(btn.getAttribute('data-product-id'));
        var inList = list.some(function(item) { return String(item.id) === pid; });
        if (inList) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function removeCompareItem(id) {
    var list = getCompareList().filter(function(item) { return String(item.id) !== String(id); });
    saveCompareList(list);
}

function initCompareUI() {
    updateCompareBar();

    var clearBtn = document.getElementById('clearCompareBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            saveCompareList([]);
            showToast('تم مسح المقارنة', 'info');
        });
    }
}
