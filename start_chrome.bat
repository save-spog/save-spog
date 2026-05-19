@echo off
echo ========================================================
echo กําลังเปิด Google Chrome โหมดพิเศษสําหรับบอท (Bypass Anti-Bot)
echo ========================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\BotProfile"
echo Chrome เปิดแล้ว! คุณสามารถเข้าใช้งานและล็อกอิน TikTok ได้ตามปกติ
exit
