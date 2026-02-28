import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border-radius: 8px; border: none; padding: 15px; font-weight: bold; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط الـ API Key بطريقة آمنة
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ خطأ: الـ API Key غير مضبوط في الـ Secrets")
    st.stop()

st.title("⚖️ منصة المحامي الذكي - إصدار المحترفين")

# 3. تقسيم واجهة الموقع (رفع الملفات / النتائج)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 رفع محضر القضية")
    uploaded_file = st.file_uploader("اسحب صورة المحضر هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند الذي قمت برفعه", use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل خط اليد"):
            with st.spinner("جاري فك شفرة الخط..."):
                try:
                    # طلب قراءة الصورة من الذكاء الاصطناعي
                    response = model.generate_content(["اقرأ هذا المحضر المصري وحوله لنص مكتوب بدقة.", img])
                    st.session_state['processed_text'] = response.text
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")

# 4. مربع التعديل والتحليل (العمود الثاني)
with col2:
    if 'processed_text' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل عليه هنا)")
        # المربع ده هو اللي تقدر تعدل فيه النص يدوياً قبل التحليل
        user_text = st.text_area("راجع النص وقم بتصحيح أي كلمات:", value=st.session_state['processed_text'], height=450)
        
        st.markdown("---")
        if st.button("⚖️ استخراج ثغرات بطلان المحضر"):
            with st.spinner("جاري تحليل الثغرات بناءً على القانون المصري..."):
                try:
                    analysis = model.generate_content(f"بناءً على نص هذا المحضر: {user_text}، استخرج كل ثغرات البطلان القانونية الممكنة طبقاً لقانون الإجراءات الجنائية المصري.")
                    st.subheader("📋 تقرير محامي الشيطان:")
                    st.success(analysis.text)
                except Exception as e:
                    st.error(f"خطأ في التحليل: {str(e)}")
