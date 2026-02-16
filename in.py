import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# --- ส่วนซ่อนเมนูเพื่อความปลอดภัย ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

LINE_ACCESS_TOKEN = "ztDjzTNBkelWGloIlOw+WTGcSRlopY5QQljoxrSD13rHOQ7rD8iMAzodBppKH3tkUX7wKAx2cBveWCi/xWG8NODcXPfmLUPWAGZqUDOYy19dTLUqYPX+xaFMPeNf5s32ezrfcHK9XpLd5swV0t6jBAdB04t89/1O/w1cDnyilFU="
USER_ID = "Cd344d34fa9507060a68cf386aa3b6b4b" 

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
st.info("อัปโหลดไฟล์เพื่อกรองรายการ DELIVERY_FAILED ของวันนี้")

uploaded_file = st.file_uploader("เลือกไฟล์ Inventory Report (.csv หรือ .xlsx)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        today = datetime.now().date()

col_status = df.columns[4]
col_date = df.columns[6]

df[col_date] = pd.to_datetime(df[col_date], errors='coerce').dt.date

mask = (df[col_status] == 'DELIVERY_FAILED') & (df[col_date] == today)
filtered_df = df[mask].copy()

        if not filtered_df.empty:
            display_cols = [1, 4, 5, 13, 15]
            final_df = filtered_df.iloc[:, display_cols]
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Delivery Date','Pickup Customer Name', 'TourID']

            st.success(f"✅ พบรายการพัสดุ {len(final_df)} รายการ สำหรับวันที่ {today_str}")
            st.dataframe(final_df, use_container_width=True)

            st.divider()
            st.subheader("🚀 ส่งการแจ้งเตือน")
            
            if st.button("ส่งข้อมูลเข้า LINE ทั้งหมด"):
                success_count = 0
                total_items = len(final_df)
                progress_bar = st.progress(0.0)
                
                for i, (idx, row) in enumerate(final_df.iterrows()):
                    msg = (f"⚠️ รายงานพัสดุ ที่ต้องนำส่งอีกครั้ง วันนี้!\n"
                           f"📦 ID: {row['Parcel ID']}\n"
                           f"📍 Customer: {row['Pickup Customer Name']}\n"
                           f"🚚 Status: {row['Failure Reason']}\n"
                           f"👤 Courier ID: {row['TourID']}")
                    
                    response = send_line_push(msg)
                    if response.status_code == 200:
                        success_count += 1
                    
                    current_step = i + 1
                    percent_complete = current_step / total_items
                    progress_bar.progress(float(percent_complete))
                
                st.balloons()
                st.success(f"ส่งสำเร็จแล้ว {success_count} รายการ!")
        else:
            st.warning(f"❌ ไม่พบรายการสำหรับวันที่ {today_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.write("รอการอัปโหลดไฟล์...")
