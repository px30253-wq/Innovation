import streamlit as st
import requests

# 1. ระบุค่า API ของคุณ (ตรวจสอบให้มั่นใจว่าไม่มีเว้นวรรค และเป็นภาษาอังกฤษล้วน)
MY_API_KEY = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy"
MY_API_SECRET = "Aue7hCtJYxAR6NltykYSzztEfllE2d"

url = "https://api.thaibulksms.com/v2/sms"

# 2. เอา API Key/Secret มาใส่ไว้ใน payload แทน
payload = {
    "api_key": abLVnvN6jlZq4hCLP1HuaNRUCFbNwy,      
    "api_secret": Aue7hCtJYxAR6NltykYSzztEfllE2d, 
    "msisdn": "0808276095",      # เบอร์พนักงาน/เบอร์ทดสอบ
    "message": "ทดสอบส่งข้อความภาษาไทย", 
    "sender": "SMS" 
}

# 3. ตอนส่ง requests.post ไม่ต้องใส่ auth=(...) แล้ว
try:
    # ส่งแค่ url กับ data เท่านั้น
    response = requests.post(url, data=payload)
    
    # ตรวจสอบผลลัพธ์
    result = response.json()
    st.write(result)
    
except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
