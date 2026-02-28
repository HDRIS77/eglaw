import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. التصميم الأسود الفخم (Dark Mode)
st.set_page_config(page_title="المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 12px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. حطيت المفتاح بتاعك مباشرة هنا عشان نلغي الـ KeyError خالص
# ده المفتاح اللي ظاهر في صورتك Active
MY_KEY = "AIzaSyCztL9Vewl1Smm51LduhOzrxZc_yJxBaqg"

genai.configure(api_key=MY_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

# 3. الواجهة
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل النص"):
            with st.spinner("جاري القراءة..."):
                # قراءة الصورة
                response = model.generate_content(["اقرأ النص في الصورة بدقة.", img])
                st.session_state['law_text'] = response.text

with col2:
    if 'law_text' in st.session_state:
        st.subheader("📝 مربع التعديل (عدل هنا)")
        # المربع اللي طلبته للتعديل
        final_text = st.text_area("", value=st.session_state['law_text'], height=400)
        
        if st.button("⚖️ تحليل ثغرات البطلان"):
            with st.spinner("جاري التحليل..."):
                analysis = model.generate_content(f"بناءً على هذا النص: {final_text}، استخرج ثغرات البطلان في القانون المصري.")
                st.success(analysis.text)
