from gtts import gTTS
import os
import time

text = "สวัสดีครับลูกพี่ ผมแฮ่มเองครับ! นี่คือตัวอย่างเสียงพากย์อัตโนมัติ สบายใจได้ครับ แฮ่มพร้อมลุยงานให้แล้ว!"
print("กำลังเสกเสียง...")

try:
    # แปลงข้อความเป็นเสียง (ภาษาไทย)
    tts = gTTS(text=text, lang='th')
    filename = "ham_voice.mp3"
    tts.save(filename)
    
    print("กำลังเล่นเสียง...")
    # สั่งให้ Windows เปิดไฟล์เสียงขึ้นมาเล่นทันที
    os.startfile(filename)
    print("เสร็จเรียบร้อย! ลองฟังดูครับ")
    
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
