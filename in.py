import streamlit as st
import requests

MY_API_KEY = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy"
MY_API_SECRET = "cfOnXTjw0Yes2CujCiLOyNHAlhHvGF"

URL = "https://api-v2.thaibulksms.com/sms"

st.title("ระบบแจ้งเตือน SMS")

payload = {
    "msisdn": "0808276095",
    "message": "ทดสอบระบบแจ้งเตือน",
    "sender": "SMS"   # ✅ ใช้ค่านี้ก่อน
}


headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

if st.button("ลองส่ง SMS อีกครั้ง"):
    try:
        response = requests.post(
            URL,
            data=payload,
            headers=headers,
            auth=(MY_API_KEY, MY_API_SECRET)  # ✅ จุดสำคัญ
        )

        st.write(f"Status Code: {response.status_code}")
        st.json(response.json())

        if response.status_code in [200, 201]:
            st.success("✅ ส่ง SMS สำเร็จแล้ว")
        else:
            st.error("❌ ส่งไม่สำเร็จ ดู error ด้านบน")

    except Exception as e:
        st.error(f"Error: {e}")
