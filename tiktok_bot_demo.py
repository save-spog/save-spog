from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

print("=== เริ่มต้นโปรแกรมจำลองบอท (เพื่อการศึกษา) ===")
print("กำลังจำลองการเปิด Chrome เบราว์เซอร์...")

# 1. เปิดเบราว์เซอร์ Chrome ขึ้นมา
# (Selenium เวอร์ชั่นใหม่ๆ จะจัดการโหลด ChromeDriver ให้เองโดยอัตโนมัติ)
driver = webdriver.Chrome()

try:
    # 2. สั่งให้บอทวิ่งไปที่หน้าเว็บ
    print("กำลังนำทางไปที่หน้าเว็บ TikTok...")
    driver.get("https://www.tiktok.com/")
    time.sleep(5) # รอเว็บโหลด
    
    print(">>> เข้าสู่หน้าเว็บสำเร็จ! <<<")
    print("สังเกต: เบราว์เซอร์นี้จะถูกควบคุมโดยซอฟต์แวร์อัตโนมัติ (จะมีแถบแจ้งเตือนด้านบน)")
    
    # เพื่อการศึกษา: เราจะให้มันพิมพ์ค้นหาคำว่า "TikTok LIVE" ในช่องค้นหา
    print("กำลังจำลองการพิมพ์ข้อความค้นหา...")
    # *หมายเหตุ: โค้ดส่วนนี้อาจจะไม่ทำงานถ้าโครงสร้างเว็บของ TikTok เปลี่ยนแปลง หรือติดระบบกันบอท 
    # แต่เราเขียนไว้เพื่อให้เห็นโครงสร้างการทำงาน
    try:
        # พยายามหาช่องค้นหา (อาจจะใช้ไม่ได้จริงเนื่องจากการป้องกันของระบบ)
        # แต่เพื่อแสดงเป็นตัวอย่างการทำงาน
        search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
        search_box.send_keys("การทำไลฟ์สด")
        search_box.send_keys(Keys.RETURN)
        print("พิมพ์ข้อความค้นหาเสร็จสิ้น...")
    except Exception as e:
        print("ไม่สามารถพิมพ์ข้อความได้ (อาจติดระบบป้องกันบอท หรือโครงสร้างเว็บเปลี่ยน)")

    print("\nเปิดเบราว์เซอร์ค้างไว้เพื่อดูผลการทำงาน...")
    print("โปรแกรมจะทำการปิดตัวเองอัตโนมัติใน 10 วินาที...")
    time.sleep(10)

finally:
    # 3. ปิดเบราว์เซอร์
    driver.quit()
    print("=== ทำงานเสร็จสมบูรณ์ ปิดเบราว์เซอร์เรียบร้อย ===")
