import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json


LINE_ACCESS_TOKEN = "ztDjzTNBkelWGloIlOw+WTGcSRlopY5QQljoxrSD13rHOQ7rD8iMAzodBppKH3tkUX7wKAx2cBveWCi/xWG8NODcXPfmLUPWAGZqUDOYy19dTLUqYPX+xaFMPeNf5s32ezrfcHK9XpLd5swV0t6jBAdB04t89/1O/w1cDnyilFU="
USER_ID = "U398d18e426987b0e189f434ebd941610" 

def send_line_push(message_text):
    """ฟังก์ชันสำหรับส่งข้อความผ่าน LINE Messaging API"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    return res


st.set_page_config(page_title="INNOVATION LINE ALERT", layout="wide")
st.title("📱 ระบบกรองข้อมูลและแจ้งเตือนผ่าน LINE")
st.info("อัปโหลดไฟล์เพื่อกรองรายการ DELIVERY_FAILED ของวันพรุ่งนี้")


uploaded_file = st.file_uploader("เลือกไฟล์ Inventory Report (.csv หรือ .xlsx)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # อ่านไฟล์ข้อมูล
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        # เตรียมวันที่วันพรุ่งนี้ (ตามรูปแบบในไฟล์ของคุณ)
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%d-%b-%Y') 

        # กรองข้อมูล (Parcel Status อยู่คอลัมน์ที่ 4, Next Delivery Date อยู่คอลัมน์ที่ 6)
        col_status = df.columns[3]
        col_date = df.columns[5]
        
        mask = (df[col_status] == 'DELIVERY_FAILED') & (df[col_date].astype(str).str.strip() == tomorrow_str)
        filtered_df = df[mask].copy()

        if not filtered_df.empty:
            # เลือกคอลัมน์ที่จำเป็น (B, E, F, P)
            display_cols = [1, 4, 5, 13, 15]
            final_df = filtered_df.iloc[:, display_cols]
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Next Delivery Date','Pickup Customer Name', 'TourID']

            st.success(f"✅ พบรายการพัสดุเสียทั้งหมด {len(final_df)} รายการ สำหรับวันที่ {tomorrow_str}")
            st.dataframe(final_df, width='stretch')

            # ==========================================
            # 4. ส่วนการส่ง LINE
            # ==========================================
            st.divider()
            st.subheader("🚀 ส่งการแจ้งเตือน")
            
            if st.button("ส่งข้อมูลเข้า LINE ทั้งหมด"):
                success_count = 0
                total_items = len(final_df)
                progress_bar = st.progress(0.0)
                
                # ใช้ enumerate เพื่อให้ได้เลขลำดับ 0, 1, 2... ที่แน่นอน
                for i, (idx, row) in enumerate(final_df.iterrows()):
                    # --- ส่วนส่ง LINE (เหมือนเดิม) ---
                    msg = (f"⚠️ รายงานพัสดุที่ต้องนำส่งอีกครั้ง!\n"
                           f"📦 ID: {row['Parcel ID']}\n"
                           f"👤 งาน: {row['Pickup Customer Name']}\n"
                           f"📍 สายส่ง: {row['TourID']}")
                    
                    response = send_line_push(msg)
                    if response.status_code == 200:
                        success_count += 1
                    
                    # --- คำนวณ Progress แบบปลอดภัย (0.0 ถึง 1.0) ---
                    current_step = i + 1
                    percent_complete = current_step / total_items
                    
                    # บังคับให้ไม่เกิน 1.0 เผื่อกันพลาด
                    progress_bar.progress(min(float(percent_complete), 1.0))
                
                st.balloons()
                st.success(f"ส่งเข้า LINE สำเร็จแล้ว {success_count} รายการ!")
                
        else:
            st.warning(f"❌ ไม่พบรายการ DELIVERY_FAILED สำหรับวันที่ {tomorrow_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
else:
    st.write("รอการอัปโหลดไฟล์...")
