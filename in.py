import streamlit as st
import requests

# 1. ใส่รหัสของคุณตรงนี้
MY_API_KEY = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy".strip()
MY_API_SECRET = "cfOnXTjw0Yes2CujCiLOyNHAlhHvGF".strip()
URL = "https://api.thaibulksms.com/v2/sms"

st.title("ระบบแจ้งเตือน SMS")

# 2. ข้อมูลที่จะส่ง
payload = {
    "msisdn": "0808276095",  # ใส่เบอร์โทรจริงของคุณเพื่อทดสอบ
    "message": "ทดสอบครั้งสุดท้ายก่อนเปลี่ยนไปใช้เมล",
    "sender": "SMS"
}

# 3. ส่งรหัสผ่าน Header (วิธีมาตรฐาน)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "api-key": MY_API_KEY,
    "api-secret": MY_API_SECRET
}

if st.button("ลองส่ง SMS อีกครั้ง"):
    try:
        # ส่งแบบกำหนด headers แยกต่างหาก
        response = requests.post(URL, data=payload, headers=headers)
        
        st.write(f"Status Code: {response.status_code}")
        result = response.json()
        st.json(result)
        
        if response.status_code in [200, 201]:
            st.success("สำเร็จแล้ว! ข้อความกำลังไปที่มือถือ")
        else:
            st.error("ยังไม่สำเร็จ... ลองดูเหตุผลในกรอบสีดำด้านบน")
            
    except Exception as e:
        st.error(f"Error: {e}")
