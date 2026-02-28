import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. المفتاح الجديد بتاعك (AIzaSyCS9Tg2...)
API_KEY = "AIzaSyCS9Tg2paPy96YCjvfywQz3DHn8JM99Qsg"

# محاولة الاتصال بالموديل المستقر
try:
    genai.configure(api_key=API_KEY)
    # جربنا نحدد الموديل بدون كلمة models/ وبدون تحديد beta لتجنب خطأ 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"عطل في التهيئة: {str(e)}")

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل النص"):
            with st.spinner("جاري محاولة القراءة..."):
                try:
                    # طلب القراءة
                    response = model.generate_content(["اقرأ هذا المحضر المصري بدقة وحوله لنص عربي.", img])
                    st.session_state['processed_text'] = response.text
                except Exception as e:
                    # محاولة أخيرة بموديل بديل لو الـ flash فيه مشكلة 404
                    try:
                        model_alt = genai.GenerativeModel('gemini-pro-vision')
                        response = model_alt.generate_content(["اقرأ النص في الصورة.", img])
                        st.session_state['processed_text'] = response.text
                    except:
                        st.error("جوجل تواجه مشكلة في التعرف على الموديل. يرجى عمل Reboot للموقع.")

with col2:
    if 'processed_text' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل عليه هنا)")
        # المربع اللي تقدر تمسح وتعدل فيه
        user_text = st.text_area("", value=st.session_state['processed_text'], height=450)
        
        if st.button("⚖️ استخراج ثغرات البطلان"):
            with st.spinner("جاري التحليل..."):
                analysis = model.generate_content(f"بناءً على نص المحضر: {user_text}، استخرج ثغرات البطلان القانونية.")
                st.success(analysis.text)
