import streamlit as st
import requests

# 1. ใส่รหัสของคุณตรงนี้ (ตรวจสอบว่าไม่มีตัวอักษร " หรือ ' ปนในรหัส)
MY_API_KEY = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy".strip()
MY_API_SECRET = "cfOnXTjw0Yes2CujCiLOyNHAlhHvGF".strip()
URL = "https://api.thaibulksms.com/v2/sms"

# 2. ข้อมูลผู้รับ
payload = {
    "msisdn": "0808276095", # ใส่เบอร์จริง
    "message": "ทดสอบระบบนวัตกรรม",
    "sender": "SMS"
}

# 3. การส่งแบบระบุ Header ชัดเจน (วิธีนี้ช่วยแก้ปัญหา 401 ได้ดีที่สุด)
try:
    # การส่งแบบ x-www-form-urlencoded พร้อมส่งรหัสผ่าน data
    data_to_send = {
        "api_key": MY_API_KEY,
        "api_secret": MY_API_SECRET,
        "msisdn": payload["msisdn"],
        "message": payload["message"],
        "sender": payload["sender"]
    }
    
    # ลองส่งแบบกำหนด headers ให้ระบบรู้ว่าเป็น Form data
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(URL, data=data_to_send, headers=headers)

    st.write(f"รหัสสถานะ (Status Code): {response.status_code}")
    
    try:
        result = response.json()
        st.json(result)
    except:
        st.write("Response Text:", response.text)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดที่ตัวโค้ด: {e}")
