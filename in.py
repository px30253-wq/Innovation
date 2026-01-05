import streamlit as st
import requests

# --- 1. ส่วนหัวของโปรแกรม ---
st.title("ระบบส่ง SMS แจ้งเตือนพนักงาน (Innovation)")
st.write("สถานะ: กำลังเตรียมการส่ง")

# --- 2. ตั้งค่า API (ตรวจสอบเครื่องหมายคำพูด " " ให้ดี) ---
# ใส่ API Key และ Secret ที่ก๊อปมาจากหน้าเว็บ ThaiBulkSMS
MY_API_KEY = "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy" 
MY_API_SECRET = "Aue7hCtJYxAR6NltykYSzztEfllE2d"
URL = "https://api.thaibulksms.com/v2/sms"

# --- 3. ข้อมูลที่จะส่ง (ตัวอย่างการกรองข้อมูล) ---
# ในอนาคตคุณสามารถเปลี่ยนเบอร์และข้อความตามไฟล์ Excel ได้
payload = {
    "api_key": "abLVnvN6jlZq4hCLP1HuaNRUCFbNwy",      
    "api_secret": "Aue7hCtJYxAR6NltykYSzztEfllE2d", 
    "msisdn": "0808276095",      # ใส่เบอร์โทรพนักงาน (ตัวเลขล้วน)
    "message": "ทดสอบ: งานพัสดุหมายเลข #123 ต้องส่งใหม่วันพรุ่งนี้", # ภาษาไทยได้
    "sender": "INNOVATION INTERNSHIP"              # ถ้ายังไม่ได้ขอชื่อตัวเอง ให้ใช้ SMS ไปก่อน
}

# --- 4. ส่วนส่งข้อมูลและตรวจสอบ Error (โครงสร้างที่ถูกต้อง) ---
try:
    # ส่งข้อมูลไปยัง API
    response = requests.post(URL, data=payload)
    
    # แสดงสถานะการตอบกลับ
    st.subheader("ผลการทำงาน")
    st.write(f"รหัสสถานะ (Status Code): {response.status_code}")
    
    # พยายามอ่านค่าเป็น JSON
    try:
        result = response.json()
        st.json(result) # โชว์รายละเอียดถ้าส่งสำเร็จ
        
        if response.status_code == 201 or response.status_code == 200:
            st.success("ส่งข้อความสำเร็จแล้ว!")
        else:
            st.warning("API ตอบกลับมาแต่ส่งไม่สำเร็จ ตรวจสอบยอดเงินหรือความถูกต้องของเบอร์โทร")
            
    except:
        # ถ้า API ไม่ส่ง JSON กลับมา ให้โชว์เป็นข้อความธรรมดาแทน
        st.error("API ไม่ได้ส่งข้อมูลรูปแบบ JSON กลับมา")
        st.write("ข้อความจากระบบ:", response.text)

except Exception as e:
    # ถ้าคำสั่ง requests.post พังตั้งแต่แรก (เช่น เน็ตหลุด หรือ Syntax ผิด)
    st.error(f"ระบบขัดข้อง: {e}")

# --- 5. ปุ่มสำหรับรันซ้ำ ---
if st.button("กดเพื่อลองส่งอีกครั้ง"):
    st.rerun()
