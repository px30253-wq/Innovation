import requests

# 1. ข้อมูลจากหน้าเว็บ ThaiBulkSMS
api_key = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy"
api_secret = "Aue7hCtJYxAR6NltykYSzztEfllE2d"

# 2. ข้อมูลที่จะส่ง
target_phone = "0808276095" # ใส่เบอร์คุณเองเพื่อทดสอบ
message = "ทดสอบระบบนวัตกรรม: ส่ง SMS ผ่าน API สำเร็จแล้ว!"

# 3. ยิงข้อมูลไปที่ URL ของเขา
url = "https://api.thaibulksms.com/v2/sms"
response = requests.post(
    url, 
    auth=(api_key, api_secret), 
    data={
        "msisdn": target_phone,
        "message": message,
        "sender": "SMS" # INNOVATION INTERNSHIP
    }
)

print(response.json()) # ดูผลลัพธ์ว่าส่งสำเร็จไหม
