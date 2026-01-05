import requests

# 1. ข้อมูลจากหน้าเว็บ ThaiBulkSMS
api_key = "ใส่ API Key ของคุณที่นี่"
api_secret = "ใส่ API Secret ของคุณที่นี่"

# 2. ข้อมูลที่จะส่ง
target_phone = "08XXXXXXXX" # ใส่เบอร์คุณเองเพื่อทดสอบ
message = "ทดสอบระบบนวัตกรรม: ส่ง SMS ผ่าน API สำเร็จแล้ว!"

# 3. ยิงข้อมูลไปที่ URL ของเขา
url = "https://api.thaibulksms.com/v2/sms"
response = requests.post(
    url, 
    auth=(api_key, api_secret), 
    data={
        "msisdn": target_phone,
        "message": message,
        "sender": "SMS" # หรือชื่อ Sender Name ที่คุณได้รับอนุมัติ
    }
)

print(response.json()) # ดูผลลัพธ์ว่าส่งสำเร็จไหม
