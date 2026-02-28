import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. حطينا المفتاح بتاعك "AIzaSy..." بطريقة الحقن المباشر
# ده المفتاح اللي في صورتك يا بطل
MY_VAL_KEY = "AIzaSyCztL9Vewl1Smm51LduhOzrxZc_yJxBaqg"

try:
    genai.configure(api_key=MY_VAL_KEY)
    # جربنا flash لأنه الأنسب للصور والمحاضر
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"مشكلة فنية في الربط: {str(e)}")

st.title("⚖️ منصة المحامي الذكي - إصدار المحترفين")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل النص"):
            with st.spinner("جاري فك شفرة الخط اليدوي..."):
                try:
                    # طلب القراءة
                    response = model.generate_content(["اقرأ هذا المحضر المصري وحوله لنص مكتوب.", img])
                    st.session_state['processed_text'] = response.text
                except Exception as e:
                    # لو المفتاح فيه مشكلة هيظهر هنا بالظبط إيه هي
                    st.error(f"خطأ من جوجل: {str(e)}")

with col2:
    if 'processed_text' in st.session_state:
        st.subheader("📝 مربع التعديل (عدل هنا)")
        # المربع اللي إنت عايزه عشان تعدل براحتك
        edited_text = st.text_area("", value=st.session_state['processed_text'], height=450)
        
        if st.button("⚖️ استخراج ثغرات البطلان"):
            with st.spinner("جاري تحليل الثغرات..."):
                try:
                    analysis = model.generate_content(f"بناءً على هذا النص: {edited_text}، استخرج ثغرات البطلان القانونية.")
                    st.success(analysis.text)
                except Exception as e:
                    st.error(f"عطل في التحليل: {str(e)}")
