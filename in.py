import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

# --- ตั้งค่า LINE Messaging API (แก้ไขตรงนี้) ---
LINE_ACCESS_TOKEN = "ztDjzTNBkelWGloIlOw+WTGcSRlopY5QQljoxrSD13rHOQ7rD8iMAzodBppKH3tkUX7wKAx2cBveWCi/xWG8NODcXPfmLUPWAGZqUDOYy19dTLUqYPX+xaFMPeNf5s32ezrfcHK9XpLd5swV0t6jBAdB04t89/1O/w1cDnyilFU="
# ถ้าส่งหาตัวเองเพื่อทดสอบ ให้เอา User ID จากหน้า Console มาใส่ก่อน
USER_ID = "0981183684" 

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response

# --- ส่วนของระบบเดิมของคุณ (ตัดมาเฉพาะส่วนแสดงผล) ---
# ... (โค้ดส่วนอัปโหลดและกรองข้อมูลเหมือนเดิม) ...

if uploaded_file:
    # ... (ส่วนกรองข้อมูลจนได้ final_df) ...
    
    if not final_df.empty:
        st.success(f"✅ พบข้อมูล {len(final_df)} รายการ")
        st.dataframe(final_df)

        if st.button("🚀 ส่งแจ้งเตือนเข้า LINE อัตโนมัติ"):
            count = 0
            for _, row in final_df.iterrows():
                # สร้างข้อความแจ้งเตือน
                msg = f"⚠️ แจ้งเตือนพัสดุเสีย!\nParcel ID: {row['Parcel ID']}\nสาเหตุ: {row['Failure Reason']}\nส่งใหม่: {row['Next Delivery Date']}"
                
                # ส่งเข้า LINE
                res = send_line_message(msg)
                if res.status_code == 200:
                    count += 1
            
            st.success(f"🟢 ส่งเข้า LINE สำเร็จทั้งหมด {count} รายการ!")
