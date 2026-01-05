import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("ระบบแจ้งเตือนนวัตกรรมผ่าน Email")

# 1. ตั้งค่าการส่ง (แก้ไขตรงนี้)
SENDER_EMAIL = "sd9268102@gmail.com"

APP_PASSWORD = "pczdwxidblvxitnq"    # รหัส 16 หลักที่ได้จาก Google
RECEIVER_EMAIL = "px30253@gmail.com" # เมลของพนักงานที่จะส่งไปหา

# 2. ฟอร์มกรอกข้อความ
subject = st.text_input("หัวข้ออีเมล", "แจ้งเตือนงานนวัตกรรม")
message_body = st.text_area("รายละเอียด", "มีงานใหม่รอการตรวจสอบ...")

if st.button("ส่งอีเมลเดี๋ยวนี้"):
    try:
        # เตรียมเนื้อหาเมล
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, 'plain'))

        # เชื่อมต่อกับ Server ของ Google
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # เข้ารหัสความปลอดภัย
        server.login(SENDER_EMAIL, APP_PASSWORD) # ล็อกอิน
        
        # สั่งส่ง
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()

        st.success(f"✅ ส่งอีเมลไปที่ {RECEIVER_EMAIL} สำเร็จแล้ว!")

    except Exception as e:
        st.error(f"❌ ส่งไม่สำเร็จเนื่องจาก: {e}")
        st.info("คำแนะนำ: ตรวจสอบว่าใช้ App Password 16 หลักที่ถูกต้อง และเปิด 2-Step Auth หรือยัง")
