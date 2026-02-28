import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 12px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. مفتاحك الجديد
MY_KEY = "AIzaSyCS9Tg2paPy96YCjvfywQz3DHn8JM99Qsg"

genai.configure(api_key=MY_KEY)

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل النص"):
            with st.spinner("جاري تجربة أفضل محرك قراءة..."):
                # محاولة استخدام الموديل المستقر
                success = False
                for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro']:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(["اقرأ النص في الصورة بدقة وحوله لنص عربي.", img])
                        st.session_state['law_text'] = response.text
                        success = True
                        break
                    except:
                        continue
                
                if not success:
                    st.error("عذراً، جوجل تواجه ضغطاً حالياً. يرجى المحاولة مرة أخرى بعد ثوانٍ.")

with col2:
    if 'law_text' in st.session_state:
        st.subheader("📝 مربع التعديل (عدل هنا)")
        final_text = st.text_area("", value=st.session_state['law_text'], height=450)
        
        if st.button("⚖️ تحليل ثغرات البطلان"):
            with st.spinner("جاري التحليل القانوني..."):
                try:
                    model_text = genai.GenerativeModel('gemini-1.5-flash')
                    analysis = model_text.generate_content(f"بناءً على هذا النص: {final_text}، استخرج ثغرات البطلان في القانون المصري.")
                    st.success(analysis.text)
                except Exception as e:
                    st.error(f"خطأ في التحليل: {str(e)}")
