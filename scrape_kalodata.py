import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import json

def scrape_kalodata():
    print("===================================================")
    print("🚀 เริ่มระบบบอทขูดข้อมูลจาก Kalodata.com")
    print("===================================================")

    # โครงสร้างโฟลเดอร์สำหรับส่งข้อมูลเข้าแดชบอร์ด
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_dir = os.path.join(current_dir, "tiktok_dashboard_ui")
    json_path = os.path.join(dashboard_dir, "data.json")

    options = Options()
    # เชื่อมต่อไปยัง Chrome ที่รันโหมดรีโมทดีบัก (Bypass Cloudflare & Anti-Bot 100%)
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        driver = webdriver.Chrome(options=options)
        print("🔗 เชื่อมต่อกับ Google Chrome พอร์ต 9222 สำเร็จ!")
        print(f"หน้าเว็บปัจจุบัน: '{driver.title}'")
        
        # ตรวจสอบเบื้องต้นว่าเข้าเว็บถูกหรือไม่
        if "kalodata" not in driver.current_url.lower():
            print("⚠️ คำเตือน: เบราว์เซอร์ปัจจุบันไม่ได้เปิดหน้าเว็บ Kalodata.com อยู่")
            print(f"URL ปัจจุบันคือ: {driver.current_url}")
            print("บอทกำลังเกาะหน้าจอรอสแกนตารางข้อมูล...")

        print("\n[เริ่มทำการสแกนข้อมูล] กำลังวิเคราะห์หน้าจอและขูดข้อมูล...")
        
        # เขียนสคริปต์ JS ขั้นเทพในการดึงตารางข้อมูลสินค้า/ครีเอเตอร์ของ Kalodata
        js_script = """
        let results = [];
        
        // 1. ลองหาโครงสร้างตารางหลักของ Ant Design (Kalodata นิยมใช้) หรือตารางทั่วไป
        let rows = document.querySelectorAll('.ant-table-row, table tr, [class*="table-row"], [role="row"]');
        
        if (rows.length > 0) {
            rows.forEach((row, idx) => {
                // ข้ามหัวข้อตาราง (Header)
                if (row.querySelector('th') || row.classList.contains('ant-table-row-indent') || idx === 0 && row.tagName === 'TR') {
                    return;
                }
                
                let cells = row.querySelectorAll('td, [role="gridcell"], [class*="table-cell"], div');
                let validCells = Array.from(cells).filter(c => c.innerText.trim().length > 0);
                
                if (validCells.length >= 3) {
                    // ดึงรูปภาพสินค้า
                    let imgEl = row.querySelector('img');
                    let imgUrl = imgEl ? imgEl.src : "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600&q=80";
                    
                    // วิเคราะห์ข้อความในแต่ละคอลัมน์เพื่อจัดประเภท
                    let rowText = row.innerText.split('\\n').map(t => t.trim()).filter(t => t.length > 0);
                    
                    if (rowText.length >= 3) {
                        let rank = idx + 1;
                        let title = "สินค้าไม่มีชื่อ";
                        let price = "-";
                        let sales = "-";
                        let revenue = "-";
                        let shopName = "Kalodata Shop";
                        
                        // ถ้าระบบ split ข้อความได้ละเอียด
                        // ตัวอย่างข้อความในแถว: ["1", "ชื่อสินค้า...", "฿350", "12.5K", "฿4.37M", "ชื่อร้าน"]
                        
                        // พยายามแกะข้อความตามลำดับ
                        let indexShift = 0;
                        if (!isNaN(rowText[0])) {
                            rank = parseInt(rowText[0]);
                            indexShift = 1;
                        }
                        
                        title = rowText[indexShift] || "สินค้าไม่มีชื่อ";
                        
                        // ค้นหาข้อความที่เป็นค่าเงิน หรือยอดขาย
                        for (let k = indexShift + 1; k < rowText.length; k++) {
                            let text = rowText[k];
                            // ตรวจหาสัญลักษณ์ค่าเงิน หรือยอดรายได้
                            if (text.includes('฿') || text.includes('$') || text.includes('M') || text.includes('K') || text.includes('万')) {
                                if (revenue === "-") {
                                    revenue = text;
                                } else if (sales === "-") {
                                    sales = text;
                                } else if (price === "-") {
                                    price = text;
                                }
                            } else if (text.length > 2 && text.length < 25 && shopName === "Kalodata Shop") {
                                shopName = text;
                            }
                        }
                        
                        results.push({
                            rank: rank,
                            title: title,
                            price: price !== "-" ? price : (rowText[indexShift+1] || "-"),
                            sales: sales !== "-" ? sales : (rowText[indexShift+2] || "-"),
                            revenue: revenue !== "-" ? revenue : (rowText[indexShift+3] || "-"),
                            shopName: shopName,
                            imgUrl: imgUrl
                        });
                    }
                }
            });
        }
        
        // 2. ถ้าหากหาตารางแบบแรกไม่เจอ ลองดึงข้อมูลจากโครงสร้างบล็อกสินค้าเดี่ยว (Grid cards)
        if (results.length === 0) {
            let cards = document.querySelectorAll('[class*="product-card"], [class*="item-card"], .ant-card, [class*="product_item"]');
            cards.forEach((card, idx) => {
                let titleEl = card.querySelector('[class*="title"], [class*="name"], h3, h4');
                let imgEl = card.querySelector('img');
                if (titleEl) {
                    let textList = card.innerText.split('\\n').map(t => t.trim()).filter(t => t.length > 0);
                    results.push({
                        rank: idx + 1,
                        title: titleEl.innerText.trim(),
                        price: textList.find(t => t.includes('฿') || t.includes('$')) || "-",
                        sales: textList.find(t => t.toLowerCase().includes('sold') || t.includes('ขายแล้ว')) || "-",
                        revenue: textList.find(t => t.includes('M') || t.includes('K')) || "-",
                        shopName: "Kalodata",
                        imgUrl: imgEl ? imgEl.src : "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600&q=80"
                    });
                }
            });
        }
        
        return results;
        """
        
        data = driver.execute_script(js_script)
        
        # จัดการกรองข้อมูลที่ซ้ำซ้อนหรือว่างเปล่า
        data = [d for d in data if d['title'] != 'สินค้าไม่มีชื่อ']
        
        if not data or len(data) == 0:
            print("⚠️ ดึงข้อมูลไม่สำเร็จหรือหน้าจอไม่มีข้อมูลตารางสินค้าที่เป็นระเบียบ!")
            print("กำลังบันทึกหน้าเว็บแบบดิบไว้เพื่อช่วยตรวจสอบโครงสร้างภายหลัง (save เป็น debug_kalodata.html)")
            with open(os.path.join(current_dir, "debug_kalodata.html"), "w", encoding="utf-8") as f:
                f.write(driver.page_source)
                
            return {
                "status": "error",
                "message": "ไม่พบตารางข้อมูลสินค้าในหน้านี้ กรุณาเปิดหน้าจัดอันดับ (Rankings) ของ Kalodata แล้วลองอีกครั้งครับ!"
            }
            
        print(f"✅ ดึงข้อมูลสำเร็จ! พบรายการสินค้าของ Kalodata ทั้งหมด {len(data)} รายการ")
        
        # อัปเดตไฟล์ข้อมูลหลักของ Dashboard
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"💾 บันทึกข้อมูลลงสู่ Dashboard เรียบร้อยแล้ว! (data.json)")
        return {"status": "success", "data": data}
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในขณะรันบอท: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    scrape_kalodata()
