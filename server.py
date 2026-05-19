from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import json

app = Flask(__name__, static_folder='tiktok_dashboard_ui')
CORS(app)

dashboard_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok_dashboard_ui")
json_path = os.path.join(dashboard_dir, "data.json")

@app.route('/')
def serve_index():
    return send_from_directory('tiktok_dashboard_ui', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('tiktok_dashboard_ui', path)

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    print("Scrape triggered...")
    try:
        options = Options()
        # เชื่อมต่อไปยังเบราว์เซอร์ Chrome ที่ผู้ใช้เปิดไว้แล้ว (Bypass การตรวจจับบอท 100%)
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
        driver = webdriver.Chrome(options=options)
        
        # ไม่ต้องให้บอทเปิดเว็บเองแล้ว เพราะเราจะให้บอทดูดข้อมูลจาก "หน้าจอที่เปิดอยู่ปัจจุบัน" เลย!
        # ดังนั้นจะไม่มีการโดนบล็อกการล็อกอินอีกต่อไป
        print("กำลังกวาดข้อมูลตารางจากหน้าที่เปิดอยู่...")
        
        js_script = """
        let results = [];
        let rows = document.querySelectorAll('table tr');
        if (rows.length > 1) {
            for(let i=1; i<rows.length; i++) {
                let cells = rows[i].querySelectorAll('td, th');
                if (cells.length >= 3) {
                    let title = cells[0].innerText.replace(/\n/g, ' ').trim();
                    if(title.length > 0) {
                        results.push({
                            rank: results.length + 1,
                            title: title,
                            price: cells[1].innerText.replace(/\n/g, ' ').trim(),
                            sales: cells[2].innerText.replace(/\n/g, ' ').trim(),
                            revenue: cells.length > 3 ? cells[3].innerText.replace(/\n/g, ' ').trim() : '-',
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
        
        if not data or len(data) == 0:
            print("คำเตือน: ไม่พบตาราง อาจจะไม่ได้อยู่หน้าจอที่ถูกต้อง")
            data = [{
                "rank": 1,
                "title": "ไม่พบตารางข้อมูล หรือไม่ได้ล็อกอิน (บันทึก HTML ไว้แล้ว)",
                "price": "-", "sales": "-", "revenue": "-", "shopName": "System",
                "imgUrl": "https://images.unsplash.com/photo-1594322436404-5a0526db4d13?w=600&q=80"
            }]
            with open("tiktok_raw_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        driver.quit()
        print("กวาดข้อมูลสำเร็จ ส่งกลับไปยังหน้าเว็บ!")
        return jsonify({"status": "success", "data": data})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/scrape-kalodata', methods=['POST'])
def trigger_scrape_kalodata():
    print("Kalodata scrape triggered...")
    try:
        from scrape_kalodata import scrape_kalodata
        result = scrape_kalodata()
        if result["status"] == "success":
            return jsonify(result)
        else:
            return jsonify(result), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("==================================================")
    print("Start TikTok Dashboard API Server")
    print("Open your browser at: http://localhost:5000")
    print("==================================================")
    app.run(port=5000, host="0.0.0.0")
