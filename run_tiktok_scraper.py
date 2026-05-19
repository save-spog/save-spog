from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import os

print("===================================================")
print("🚀 เริ่มระบบบอทดึงข้อมูล TikTok สู่หน้า Dashboard")
print("===================================================")

options = Options()
options.add_experimental_option("detach", True)

# กำหนด Path ไฟล์ JSON ที่ Dashboard กำลังรออ่านข้อมูล
dashboard_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok_dashboard_ui")
json_path = os.path.join(dashboard_dir, "data.json")

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://seller-th.tiktok.com/ads-creation/dashboard")
    
    print("\n[ขั้นตอนที่ 1] กรุณาล็อกอินเข้าสู่ระบบ TikTok Seller")
    print("[ขั้นตอนที่ 2] เปิดไปยังหน้าที่แสดงตารางรายการสินค้า หรือ แคมเปญโฆษณา")
    print(">> บอทจะรอ 60 วินาที เพื่อให้คุณจัดการหน้าเว็บให้พร้อม <<")
    
    # นับถอยหลังให้เห็น
    for i in range(60, 0, -1):
        print(f"รอเวลาอีก {i} วินาที...", end="\r")
        time.sleep(1)
        
    print("\n\n[เริ่มการสแกน] กำลังวิเคราะห์และกวาดข้อมูลจากหน้าจอ...")
    
    # -------------------------------------------------------------
    # ส่วนกวาดข้อมูล (Scraping Logic)
    # เนื่องจากเราไม่รู้โครงสร้างเว็บเป๊ะๆ เราจะใช้ JS กวาด <TABLE> หรือ <DIV>
    # -------------------------------------------------------------
    js_script = """
    let results = [];
    
    // พยายามหาตารางข้อมูล (Table) ก่อน
    let rows = document.querySelectorAll('table tr');
    if (rows.length > 1) {
        for(let i=1; i<rows.length; i++) {
            let cells = rows[i].querySelectorAll('td, th');
            if (cells.length >= 3) {
                // พยายามดึงข้อความจากแต่ละคอลัมน์
                let title = cells[0].innerText.replace(/\n/g, ' ').trim();
                let col2 = cells[1].innerText.replace(/\n/g, ' ').trim();
                let col3 = cells[2].innerText.replace(/\n/g, ' ').trim();
                let col4 = cells.length > 3 ? cells[3].innerText.replace(/\n/g, ' ').trim() : '-';
                
                // ข้ามแถวที่ว่างเปล่า
                if(title.length > 0) {
                    results.push({
                        rank: results.length + 1,
                        title: title,
                        price: col2, // อาจจะเป็นราคาหรือยอดคลิก ขึ้นอยู่กับหน้าเว็บ
                        sales: col3, // อาจจะเป็นยอดขายหรือการแสดงผล
                        revenue: col4, // อาจจะเป็นต้นทุน/รายได้
                        shopName: "TikTok Data",
                        imgUrl: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=600&q=80"
                    });
                }
            }
        }
    }
    
    return results;
    """
    
    data = driver.execute_script(js_script)
    
    # หากไม่พบตารางเลย (โครงสร้างเว็บอาจใช้ div แทน table)
    if not data or len(data) == 0:
        print("\n⚠️ ไม่พบข้อมูลในรูปแบบตาราง! บอทจะบันทึกโครงสร้างเว็บไว้เพื่อวิเคราะห์ต่อ...")
        # Save raw HTML for debugging
        with open("tiktok_raw_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # แจ้งเตือนขึ้นหน้า Dashboard
        data = [{
            "rank": 1,
            "title": "ไม่พบรูปแบบตารางในหน้านี้ (บันทึก HTML ไว้ที่ tiktok_raw_page.html แล้ว)",
            "price": "กรุณา",
            "sales": "เปลี่ยนหน้า",
            "revenue": "เพื่อดึงใหม่",
            "shopName": "System Alert",
            "imgUrl": "https://images.unsplash.com/photo-1594322436404-5a0526db4d13?w=600&q=80" // Error Icon style
        }]
    else:
        print(f"\n✅ ดึงข้อมูลสำเร็จ! พบรายการข้อมูลทั้งหมด {len(data)} รายการ")
    
    # อัปเดตไฟล์ data.json เพื่อให้ Dashboard รีเฟรชตัวเองทันที!
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"บันทึกข้อมูลลง Dashboard เรียบร้อยแล้ว! (เปิดดูหน้าเว็บได้เลย)")

except Exception as e:
    print(f"\n❌ เกิดข้อผิดพลาด: {e}")
finally:
    print("\nบอททำงานเสร็จสิ้น (สามารถรันไฟล์นี้ใหม่ได้ทุกเมื่อที่ต้องการอัปเดตข้อมูล)")
