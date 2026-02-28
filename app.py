import streamlit as st
from PIL import Image
import os

# 1. الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="منصة المحامي الذكي - المرجع الدستوري", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    .law-box { background-color: #1e252e; padding: 20px; border-radius: 10px; border-right: 5px solid #00ffcc; margin-bottom: 20px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منصة المحامي الذكي - الإصدار القانوني الشامل")

# 2. قسم المرجع القانوني (تحميل ملف القانون)
with st.sidebar:
    st.header("📚 المكتبة القانونية")
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            law_content = f.read()
        st.success("✅ تم تحميل الدستور المصري كمرجع")
        with st.expander("استعراض نصوص المواد"):
            st.write(law_content)
    else:
        st.warning("⚠️ لم يتم العثور على ملف law_reference.txt")

# 3. واجهة العمل الرئيسية
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 رفع محضر القضية")
    uploaded_file = st.file_uploader("اسحب صورة المحضر هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند المرفوع", use_container_width=True)
        
        # الزرار ده دلوقتي كشكل (هيكل) عشان الأخطاء متطلعش
        if st.button("🔍 قراءة وتحويل النص (قيد التفعيل)"):
            st.info("سيتم تفعيل الربط مع الذكاء الاصطناعي في الخطوة الأخيرة.")

with col2:
    st.subheader("📝 مربع التعديل والتحليل")
    # مربع التعديل اللي طلبته
    user_text = st.text_area("النص المستخرج سيظهر هنا، ويمكنك تعديله يدوياً:", height=400, placeholder="بانتظار رفع المحضر وقراءته...")
    
    st.markdown("---")
    if st.button("⚖️ استخراج ثغرات البطلان بناءً على الدستور"):
        st.info("جاري تجهيز محرك التحليل القانوني...")

# 4. قسم "تقرير الثغرات" (هيكل)
st.markdown("### 📋 التقرير القانوني المتوقع")
st.info("هنا سيقوم النظام بمطابقة نص المحضر مع مواد الدستور في المكتبة لاستخراج الدفوع القانونية.")
