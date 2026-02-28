import streamlit as st
import os
from groq import Groq
from PIL import Image
import pytesseract # المكتبة المسؤولة عن القراءة التلقائية

# 1. ثيم محامي الشيطان
st.set_page_config(page_title="محامي الشيطان Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #ff0000 0%, #000000 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2 { color: #ff0000 !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. المرجع القانوني
def load_law():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري."

LAW_BASE = load_law()
client = Groq(api_key="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")

st.title("⚖️ منصة محامي الشيطان - القراءة والتحليل الأوتوماتيكي")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    extracted_text = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        with st.spinner("جاري قراءة نص المحضر أوتوماتيكياً..."):
            try:
                # هنا السحر: تحويل الصورة لنص أوتوماتيكياً
                extracted_text = pytesseract.image_to_string(img, lang='ara')
                st.success("✅ تمت القراءة بنجاح!")
            except:
                st.warning("⚠️ القراءة التلقائية تتطلب تثبيت Tesseract على السيرفر. يمكنك نسخ النص يدوياً مؤقتاً.")

with col2:
    st.subheader("📝 نص المحضر المستخرج")
    # النص بيظهر هنا لوحده بعد الرفع
    final_text = st.text_area("راجع النص وعدله لو فيه غلطات:", value=extracted_text, height=400)
    
    if st.button("⚖️ تحليل ثغرات البطلان"):
        if not final_text:
            st.error("ارفع صورة أولاً أو اكتب النص!")
        else:
            with st.spinner("جاري التحليل القانوني..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"أنت محامي الشيطان. مرجعك: {LAW_BASE}. حلل الثغرات بذكاء."},
                        {"role": "user", "content": final_text}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.markdown("### 📋 النتيجة:")
                st.success(chat_completion.choices[0].message.content)
