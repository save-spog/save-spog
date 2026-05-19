from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

print("=== กำลังเปิดบอทดึงข้อมูล TikTok Ads (แบบใหม่) ===")
options = Options()
# ไม่ใช้ User Data เดิมแล้ว เพื่อหลีกเลี่ยงการล็อกไฟล์
# แต่จะเปิดเบราว์เซอร์ใหม่ขึ้นมา ให้ผู้ใช้ล็อกอินชั่วคราว
options.add_experimental_option("detach", True)

try:
    driver = webdriver.Chrome(options=options)
    print("เปิด Chrome สำเร็จ! กำลังเข้าไปที่หน้า TikTok Ads...")
    driver.get("https://seller-th.tiktok.com/ads-creation/dashboard")
    
    print("\n>>> กรุณาล็อกอินด้วยบัญชี TikTok ของคุณ (หรือสแกน QR Code) <<<")
    print("และคลิกไปที่หน้าแคมเปญที่คุณต้องการดึงข้อมูล...")
    print("รอ 45 วินาทีเพื่อให้คุณดำเนินการ...")
    time.sleep(45)
    
    print("\nหมดเวลา! กำลังเริ่มทำการกวาดข้อมูลหน้าจอ (Scraping)...")
    
    # ดึงข้อมูลตัวหนังสือทั้งหมดในหน้าเว็บ
    body_text = driver.execute_script("return document.body.innerText;")
    
    # เซฟข้อมูลลงไฟล์เพื่อนำไปวิเคราะห์ต่อ
    save_path = r"c:\Users\controlss\.gemini\antigravity\scratch\scraped_data.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(body_text)
        
    print(f"ดึงข้อมูลเสร็จสมบูรณ์! เซฟไฟล์ไว้ที่: {save_path}")
    
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
finally:
    try:
        driver.quit()
    except:
        pass
