import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الثيم الأسود الاحترافي
st.set_page_config(page_title="المحامي الذكي Pro", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #1a1c23; color: #00ffcc; border: 1px solid #4b5563; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border: none; padding: 10px; font-weight: bold; border-radius: 8px; }
    .stInfo { background-color: #1e293b; color: #38bdf8; border-right: 5px solid #38bdf8; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الـ AI (تم تحديث اسم الموديل لحل الخطأ)
try:
    genai.configure(api_key=st.secrets["AIzaSyCztL9Vew1ISmm51LduhOzrxZc_yJxBaqg"])
    # استخدمنا flash لأنه أسرع وأحدث في التعامل مع الصور
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("خطأ في الـ API Key: تأكد من وضعه في Secrets")

st.title("⚖️ منصة المحامي الذكي - إصدار المحترفين")
st.info("ارفع صور المحضر الآن. النظام سيقوم بتحويلها لنص قابل للتعديل فوراً.")

# 3. واجهة الرفع والعمليات
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("📁 اسحب صور المحضر هنا (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند المرفوع", use_container_width=True)
        
        if st.button("🔍 قراءة وتحليل النص"):
            with st.spinner("جاري فك شفرة الخط..."):
                try:
                    # طلب القراءة من AI
                    response = model.generate_content(["اقرأ النص في هذه الصورة بدقة وحوله لنص مكتوب باللغة العربية.", img])
                    st.session_state['text_output'] = response.text
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")

# 4. مربع التعديل والتحليل (بيظهر بعد القراءة)
with col2:
    if 'text_output' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل عليه هنا)")
        # ده المربع اللي سألت عليه، تقدر تمسح وتكتب فيه
        edited_text = st.text_area("النص المكتوب:", value=st.session_state['text_output'], height=400)
        
        st.markdown("---")
        analysis_btn = st.button("⚖️ تحليل الثغرات القانونية وإعداد المرافعة")
        
        if analysis_btn:
            with st.spinner("جاري استخراج الثغرات من الدستور..."):
                prompt = f"بناءً على هذا النص: {edited_text}، استخرج ثغرات بطلان المحضر طبقاً لقانون الإجراءات الجنائية المصري."
                analysis = model.generate_content(prompt)
                st.subheader("📋 تقرير محامي الشيطان:")
                st.success(analysis.text)
