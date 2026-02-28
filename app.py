import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات التصميم الاحترافي (Dark Mode)
st.set_page_config(page_title="المحامي الذكي Pro", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #1a1c23; color: #00ffcc; border: 1px solid #4b5563; font-size: 18px !important; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. التحقق من الـ API Key وتهيئة الموديل
model = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["AIzaSyCztL9Vew1ISmm51LduhOzrxZc_yJxBaqg"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("❌ لم يتم العثور على API Key في Secrets. يرجى إضافته في إعدادات Streamlit Cloud.")
except Exception as e:
    st.error(f"⚠️ خطأ في تهيئة الذكاء الاصطناعي: {str(e)}")

st.title("⚖️ منصة المحامي الذكي - إصدار المحترفين")

# 3. واجهة العمل
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 رفع مستندات القضية")
    uploaded_file = st.file_uploader("اسحب صورة المحضر هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and model:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند الأصلي", use_container_width=True)
        
        if st.button("🔍 استخراج النص من الصورة"):
            with st.spinner("جاري قراءة خط اليد..."):
                try:
                    # قراءة الصورة وتحويلها لنص
                    response = model.generate_content(["قم بقراءة هذا المحضر المصري المكتوب بخط اليد بدقة وحوله لنص مكتوب باللغة العربية.", img])
                    st.session_state['extracted_text'] = response.text
                except Exception as e:
                    st.error(f"خطأ أثناء القراءة: {str(e)}")

# 4. مربع التعديل (المكان اللي هتقدر تعدل فيه)
with col2:
    if 'extracted_text' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل ما تراه خطأ)")
        # المربع ده تقدر تكتب وتمسح فيه براحتك
        user_edited_text = st.text_area("النص المكتوب:", value=st.session_state['extracted_text'], height=350)
        
        st.markdown("---")
        if st.button("⚖️ تحليل الثغرات القانونية"):
            if model:
                with st.spinner("جاري البحث عن ثغرات في القانون المصري..."):
                    try:
                        prompt = f"بناءً على نص المحضر التالي: {user_edited_text}\nاستخرج ثغرات بطلان الإجراءات طبقاً لقانون الإجراءات الجنائية المصري والدستور."
                        analysis = model.generate_content(prompt)
                        st.subheader("📋 تقرير محامي الشيطان:")
                        st.success(analysis.text)
                    except Exception as e:
                        st.error(f"خطأ في التحليل: {str(e)}")
