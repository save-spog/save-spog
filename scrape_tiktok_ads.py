from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

print("=== กำลังเปิดบอทดึงข้อมูล TikTok Ads ===")
options = Options()
# กำหนด Path ไปที่โฟลเดอร์ User Data ของ Chrome เพื่อให้จำค่าการล็อกอิน
user_data_path = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data")
options.add_argument(f"user-data-dir={user_data_path}")

try:
    driver = webdriver.Chrome(options=options)
    print("เปิด Chrome สำเร็จ! กำลังเข้าไปที่หน้า TikTok Ads...")
    # เข้าไปที่หน้าจัดการแคมเปญโฆษณา
    driver.get("https://seller-th.tiktok.com/ads-creation/dashboard")
    
    print("กำลังรอให้หน้าเว็บโหลด 15 วินาที...")
    print(">>> หากคุณพี่ต้องการดูแคมเปญไหนเป็นพิเศษ สามารถคลิกเข้าไปในแคมเปญนั้นได้เลยภายใน 15 วินาทีนี้ครับ <<<")
    time.sleep(15)
    
    print("หมดเวลา! กำลังเริ่มทำการกวาดข้อมูลหน้าจอ (Scraping)...")
    
    # ดึงข้อมูลตัวหนังสือทั้งหมดในหน้าเว็บ
    body_text = driver.execute_script("return document.body.innerText;")
    
    # เซฟข้อมูลลงไฟล์เพื่อนำไปวิเคราะห์ต่อ
    save_path = r"c:\Users\controlss\.gemini\antigravity\scratch\scraped_data.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(body_text)
        
    print(f"ดึงข้อมูลเสร็จสมบูรณ์! เซฟไฟล์ไว้ที่: {save_path}")
    
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
    print("คำแนะนำ: โปรดแน่ใจว่าได้ปิดหน้าต่าง Google Chrome ครบทุกหน้าต่างแล้วจริงๆ ก่อนรันบอทครับ")
finally:
    try:
        driver.quit()
    except:
        pass
