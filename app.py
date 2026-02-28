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

# 2. استخدام مفتاحك الجديد المباشر
API_KEY = "AIzaSyCS9Tg2paPy96YCjvfywQz3DHn8JM99Qsg"

def start_ai():
    genai.configure(api_key=API_KEY)
    # هنجرب أكتر من نسخة عشان نتخطى خطأ 404
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro-vision']:
        try:
            model = genai.GenerativeModel(model_name)
            return model
        except:
            continue
    return None

model = start_ai()

st.title("⚖️ منصة المحامي الذكي - إصدار المحترفين")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and model:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل النص"):
            with st.spinner("جاري فك شفرة الخط..."):
                try:
                    # طلب القراءة
                    response = model.generate_content(["اقرأ هذا المحضر المصري بدقة وحوله لنص مكتوب.", img])
                    st.session_state['processed_text'] = response.text
                except Exception as e:
                    st.error(f"تنبيه: جوجل تطلب المحاولة مرة أخرى (Reboot). الخطأ: {str(e)}")

with col2:
    if 'processed_text' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل هنا)")
        # المربع السحري للتعديل
        final_text = st.text_area("", value=st.session_state['processed_text'], height=450)
        
        if st.button("⚖️ استخراج ثغرات البطلان"):
            with st.spinner("جاري تحليل الثغرات..."):
                analysis = model.generate_content(f"بناءً على نص المحضر: {final_text}، استخرج ثغرات البطلان القانونية.")
                st.success(analysis.text)
