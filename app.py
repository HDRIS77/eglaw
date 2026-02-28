import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 17px; }
    .stButton>button { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border-radius: 8px; border: none; padding: 12px; font-weight: bold; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    .stAlert { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط الذكاء الاصطناعي
model = None
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ يرجى ضبط GOOGLE_API_KEY في إعدادات Secrets")

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

# 3. تقسيم الشاشة
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 رفع محضر القضية")
    uploaded_file = st.file_uploader("اسحب صورة المحضر هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and model:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند المرفوع", use_container_width=True)
        
        if st.button("🔍 قراءة الخط اليدوي"):
            with st.spinner("جاري فك تشفير الخط..."):
                response = model.generate_content(["قم بتحويل هذا الخط اليدوي في المحضر لنص عربي مكتوب بدقة.", img])
                st.session_state['text_out'] = response.text

# 4. المربع السحري للتعديل والتحليل
with col2:
    if 'text_out' in st.session_state:
        st.subheader("📝 النص المستخرج (يمكنك التعديل عليه)")
        # ده المربع اللي تقدر تعدل فيه النص لو الـ AI غلط في كلمة
        final_text = st.text_area("راجع النص هنا:", value=st.session_state['text_out'], height=400)
        
        st.markdown("---")
        if st.button("⚖️ تحليل الثغرات القانونية ومحامي الشيطان"):
            with st.spinner("جاري مراجعة القوانين المصرية..."):
                analysis = model.generate_content(f"بناءً على هذا النص: {final_text}، استخرج كل ثغرات البطلان المحتملة في قانون الإجراءات الجنائية المصري.")
                st.subheader("📋 التقرير القانوني:")
                st.success(analysis.text)
