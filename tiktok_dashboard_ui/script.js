// Function to render product cards
function renderProducts(products) {
    const container = document.getElementById('products-container');
    container.innerHTML = ''; // Clear existing
    
    if (products.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">ไม่พบข้อมูลสินค้า</div>';
        return;
    }

    products.forEach((product, index) => {
        const rank = product.rank || (index + 1);
        const card = document.createElement('div');
        
        // Add dynamic rank styling class
        let rankClass = '';
        if (rank === 1) rankClass = ' rank-1';
        else if (rank === 2) rankClass = ' rank-2';
        else if (rank === 3) rankClass = ' rank-3';
        
        card.className = 'product-card' + rankClass;
        
        const defaultImg = "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600&q=80";
        
        // Format first letter of shop name for avatar
        const shopInitials = product.shopName ? product.shopName.charAt(0).toUpperCase() : 'S';
        
        card.innerHTML = `
            <div class="product-rank">TOP ${rank}</div>
            <div class="product-img-wrapper">
                <img src="${product.imgUrl || defaultImg}" alt="Product Image" class="product-img" onerror="this.src='${defaultImg}'">
            </div>
            <div class="product-details">
                <h3 class="product-title" title="${product.title || ''}">${product.title || 'ไม่มีชื่อสินค้า'}</h3>
                
                <div class="product-metrics">
                    <span class="price">${product.price || '-'}</span>
                    <span class="sales">${product.sales || '-'}</span>
                </div>
                
                <div class="product-estimate">
                    <span class="estimate-label">รายได้ประมาณ (GMV)</span>
                    <span class="estimate-val">${product.revenue || '-'}</span>
                </div>
                
                <div class="shop-info">
                    <div class="shop-avatar">${shopInitials}</div>
                    <span>${product.shopName || 'Shop'}</span>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Fetch data from data.json
async function loadData() {
    try {
        // Add cache busting parameter to prevent browser caching
        const response = await fetch('data.json?t=' + new Date().getTime());
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        renderProducts(data);
    } catch (error) {
        console.error("Error loading data:", error);
    }
}

// Setup sidebar interactions
function setupSidebar() {
    const navItems = document.querySelectorAll('.nav-item');
    const pageTitle = document.querySelector('.page-header h1');
    const sectionTitle = document.querySelector('.section-header h2');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent page reload
            
            // Remove active class from all
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            item.classList.add('active');
            
            // Update title just to show it works
            const menuText = item.innerText.trim();
            pageTitle.innerHTML = `🔥 ${menuText}`;
            sectionTitle.innerText = `Top 50 ${menuText} ขายดี`;
        });
    });
}

function setupScrapeButton() {
    const btn = document.getElementById('scrape-btn');
    if(btn) {
        btn.addEventListener('click', async () => {
            // Update button UI to loading state
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังดูดข้อมูลจากเบราว์เซอร์...';
            btn.disabled = true;
            btn.style.opacity = '0.7';
            
            try {
                // Call the Flask Backend
                const response = await fetch('/api/scrape', { method: 'POST' });
                const result = await response.json();
                
                if(result.status === 'success') {
                    renderProducts(result.data);
                } else {
                    alert('บอทเกิดข้อผิดพลาด: ' + result.message);
                }
            } catch (err) {
                alert('ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์หลังบ้านได้ กรุณาไปกดรันไฟล์ server.py ก่อนครับ!');
            } finally {
                // Reset button UI
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.style.opacity = '1';
            }
        });
    }
}

function setupKalodataScrapeButton() {
    const btn = document.getElementById('scrape-kalodata-btn');
    if(btn) {
        btn.addEventListener('click', async () => {
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังเกาะขูดข้อมูล Kalodata...';
            btn.disabled = true;
            btn.style.opacity = '0.7';
            
            try {
                const response = await fetch('/api/scrape-kalodata', { method: 'POST' });
                const result = await response.json();
                
                if(result.status === 'success') {
                    renderProducts(result.data);
                    alert('อาแฮ่มขูดข้อมูลจาก Kalodata สำเร็จแล้วครับลูกพี่! 🎉');
                } else {
                    alert('บอทเกิดข้อผิดพลาด: ' + result.message);
                }
            } catch (err) {
                alert('ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์หลังบ้านได้ กรุณาไปกดรันไฟล์ server.py ก่อนครับ!');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.style.opacity = '1';
            }
        });
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    setupSidebar();
    setupScrapeButton();
    setupKalodataScrapeButton();
    // Auto refresh data every 5 seconds to show real-time updates!
    setInterval(loadData, 5000);
});
