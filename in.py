import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

# --- 1. ดึงค่าจาก Secrets (ต้องชื่อตรงกับในหน้าเว็บ Streamlit) ---
try:
    LINE_TOKEN = st.secrets["ztDjzTNBkelWGloIlOw+WTGcSRlopY5QQljoxrSD13rHOQ7rD8iMAzodBppKH3tkUX7wKAx2cBveWCi/xWG8NODcXPfmLUPWAGZqUDOYy19dTLUqYPX+xaFMPeNf5s32ezrfcHK9XpLd5swV0t6jBAdB04t89/1O/w1cDnyilFU="]
    USER_ID = st.secrets["Cd344d34fa9507060a68cf386aa3b6b4b"]
except KeyError:
    st.error("❌ ไม่พบข้อมูลใน Secrets! กรุณาตรวจสอบการตั้งค่าใน Streamlit Cloud")
    st.stop()

# --- 2. ซ่อนเมนู View Source เพื่อความปลอดภัย ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def send_line_push(message_text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message_text}]
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    return res

st.set_page_config(page_title="INNOVATION LINE ALERT", layout="wide")
st.title("📦 ระบบกรองข้อมูลและแจ้งเตือนผ่าน LINE")

uploaded_file = st.file_uploader("เลือกไฟล์ Inventory Report (.csv หรือ .xlsx)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%d-%b-%Y') 

        # กรองข้อมูล DELIVERY_FAILED ของวันพรุ่งนี้
        col_status = df.columns[3]
        col_date = df.columns[5]
        mask = (df[col_status] == 'DELIVERY_FAILED') & (df[col_date].astype(str).str.strip() == tomorrow_str)
        filtered_df = df[mask].copy()

        if not filtered_df.empty:
            display_cols = [1, 4, 5, 13, 15]
            final_df = filtered_df.iloc[:, display_cols]
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Next Delivery Date','Pickup Customer Name', 'TourID']

            st.success(f"✅ พบรายการทั้งหมด {len(final_df)} รายการ สำหรับวันที่ {tomorrow_str}")
            st.dataframe(final_df, use_container_width=True)

            if st.button("🚀 ส่งข้อมูลเข้า LINE ทั้งหมด"):
                success_count = 0
                progress_bar = st.progress(0.0)
                
                for i, (idx, row) in enumerate(final_df.iterrows()):
                    msg = (f"⚠️ แจ้งเตือนพัสดุ!\n"
                           f"📦 ID: {row['Parcel ID']}\n"
                           f"📍 ชื่อลูกค้า: {row['Pickup Customer Name']}\n"
                           f"👤 Courier ID: {row['TourID']}")
                    
                    response = send_line_push(msg)
                    if response.status_code == 200:
                        success_count += 1
                    
                    progress_bar.progress((i + 1) / len(final_df))
                
                st.balloons()
                st.success(f"ส่งเข้า LINE สำเร็จแล้ว {success_count} รายการ!")
        else:
            st.warning(f"❌ ไม่พบรายการสำหรับวันที่ {tomorrow_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.write("รอการอัปโหลดไฟล์...")
