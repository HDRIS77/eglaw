import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. وضع المفتاح "كـ نص" لحل مشكلة الـ Invalid Key (من صورتك image_9cece6.png)
# تأكد أن المفتاح بين علامات التنصيص ""
MY_API_KEY = "AIzaSyCztL9Vewl1Smm51LduhOzrxZc_yJxBaqg" 

try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في تهيئة المفتاح: {str(e)}")

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")

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
                    # طلب قراءة الصورة (Vision)
                    response = model.generate_content([
                        "اقرأ هذا المحضر المصري المكتوب بخط اليد وحوله لنص عربي مكتوب بدقة.", 
                        img
                    ])
                    st.session_state['text_out'] = response.text
                except Exception as e:
                    st.error(f"حدث خطأ أثناء القراءة: {str(e)}")

with col2:
    if 'text_out' in st.session_state:
        st.subheader("📝 النص المستخرج (عدل عليه هنا)")
        # المربع الذي طلبته للتعديل اليدوي
        edited_text = st.text_area("راجع النص وقم بتصحيحه قبل التحليل:", value=st.session_state['text_out'], height=450)
        
        if st.button("⚖️ استخراج ثغرات بطلان المحضر"):
            with st.spinner("جاري مراجعة القوانين المصرية..."):
                try:
                    analysis = model.generate_content(f"بناءً على نص هذا المحضر: {edited_text}، استخرج كل ثغرات البطلان القانونية الممكنة طبقاً لقانون الإجراءات الجنائية المصري.")
                    st.subheader("📋 تقرير محامي الشيطان:")
                    st.success(analysis.text)
                except Exception as e:
                    st.error(f"خطأ في التحليل: {str(e)}")
