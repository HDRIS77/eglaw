import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي
st.set_page_config(page_title="المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 12px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. حطينا المفتاح مباشرة كـ نص String عشان نلغي الـ KeyError خالص
# المفتاح ده هو اللي ظهر في صورتك إنه Active
MY_KEY = "AIzaSyCztL9Vewl1Smm51LduhOzrxZc_yJxBaqg"

try:
    genai.configure(api_key=MY_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"مشكلة في تشغيل الـ AI: {str(e)}")

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

# 3. تقسيم الواجهة (رفع وقراءة)
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
                    # قراءة الصورة
                    response = model.generate_content(["اقرأ النص في هذه الصورة بدقة وحوله لنص عربي.", img])
                    st.session_state['law_text'] = response.text
                except Exception as e:
                    st.error(f"عطل في القراءة: {str(e)}")

# 4. مربع التعديل والتحليل (العمود الثاني)
with col2:
    if 'law_text' in st.session_state:
        st.subheader("📝 مربع التعديل (عدل هنا)")
        # المربع السحري اللي طلبته
        final_text = st.text_area("", value=st.session_state['law_text'], height=450)
        
        if st.button("⚖️ تحليل ثغرات البطلان"):
            with st.spinner("جاري البحث في القانون المصري..."):
                analysis = model.generate_content(f"بناءً على هذا النص: {final_text}، استخرج ثغرات البطلان في القانون المصري.")
                st.subheader("📋 تقرير محامي الشيطان:")
                st.success(analysis.text)
