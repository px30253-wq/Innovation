import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

# ==========================================
# 1. ตั้งค่า LINE Messaging API (ใส่รหัสของคุณตรงนี้)
# ==========================================
LINE_ACCESS_TOKEN = "ztDjzTNBkelWGloIlOw+WTGcSRlopY5QQljoxrSD13rHOQ7rD8iMAzodBppKH3tkUX7wKAx2cBveWCi/xWG8NODcXPfmLUPWAGZqUDOYy19dTLUqYPX+xaFMPeNf5s32ezrfcHK9XpLd5swV0t6jBAdB04t89/1O/w1cDnyilFU="
USER_ID = "0981183684" 

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

# ==========================================
# 2. ตั้งค่าหน้าเว็บ Streamlit
# ==========================================
st.set_page_config(page_title="INNOVATION LINE ALERT", layout="wide")
st.title("📱 ระบบกรองข้อมูลและแจ้งเตือนผ่าน LINE")
st.info("อัปโหลดไฟล์เพื่อกรองรายการ DELIVERY_FAILED ของวันพรุ่งนี้ และส่งเข้า LINE")

# ==========================================
# 3. ส่วนการอัปโหลดและประมวลผลไฟล์
# ==========================================
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
            display_cols = [1, 4, 5, 15]
            final_df = filtered_df.iloc[:, display_cols]
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Next Delivery Date', 'TourID']

            st.success(f"✅ พบรายการพัสดุเสียทั้งหมด {len(final_df)} รายการ สำหรับวันที่ {tomorrow_str}")
            st.dataframe(final_df, use_container_width=True)

            # ==========================================
            # 4. ส่วนการส่ง LINE
            # ==========================================
            st.divider()
            st.subheader("🚀 ส่งการแจ้งเตือน")
            
            if st.button("ส่งข้อมูลเข้า LINE ทั้งหมด"):
                success_count = 0
                progress_bar = st.progress(0)
                
                for index, row in final_df.iterrows():
                    # สร้างข้อความที่จะส่ง
                    msg = (f"⚠️ รายงานพัสดุเสีย!\n"
                           f"📦 ID: {row['Parcel ID']}\n"
                           f"❌ สาเหตุ: {row['Failure Reason']}\n"
                           f"🚚 ส่งใหม่: {row['Next Delivery Date']}\n"
                           f"📍 สายส่ง: {row['TourID']}")
                    
                    # เรียกฟังก์ชันส่ง LINE
                    response = send_line_push(msg)
                    
                    if response.status_code == 200:
                        success_count += 1
                    
                    # อัปเดต Progress Bar
                    progress_bar.progress((index + 1) / len(final_df))
                
                st.balloons()
                st.success(f"ส่งเข้า LINE สำเร็จแล้ว {success_count} รายการ!")
                
        else:
            st.warning(f"❌ ไม่พบรายการ DELIVERY_FAILED สำหรับวันที่ {tomorrow_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
else:
    st.write("รอการอัปโหลดไฟล์...")
