import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الثيم الأسود الاحترافي (Dark Mode)
st.set_page_config(page_title="منصة المحامي الذكي Pro", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; cursor: pointer; }
    .stButton>button:hover { background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%); }
    h1, h2, h3 { color: #00ffcc !important; text-align: right; font-family: 'Segoe UI', sans-serif; }
    .stImage { border-radius: 15px; border: 2px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. حطينا الـ API Key مباشرة في الكود عشان نحل مشكلة الـ Secrets
MY_API_KEY = "AIzaSyCztL9Vewl1Smm51LduhOzrxZc_yJxBaqg"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚖️ منصة المحامي الذكي - النسخة الاحترافية")
st.markdown("---")

# 3. تقسيم واجهة العمل
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 رفع محضر القضية")
    uploaded_file = st.file_uploader("اسحب صورة المحضر هنا (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند الذي قمت برفعه", use_container_width=True)
        
        if st.button("🔍 قراءة وتحويل خط اليد"):
            with st.spinner("جاري فك شفرة الخط باستخدام AI..."):
                try:
                    # طلب قراءة الصورة وتحويلها لنص
                    response = model.generate_content([
                        "أنت خبير في قراءة محاضر الشرطة المصرية. قم بتحويل الخط اليدوي في هذه الصورة لنص عربي مكتوب بدقة عالية جداً.", 
                        img
                    ])
                    st.session_state['text_out'] = response.text
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال: {str(e)}")

# 4. مربع التعديل والتحليل القانوني (العمود الثاني)
with col2:
    if 'text_out' in st.session_state:
        st.subheader("📝 النص المستخرج (يمكنك التعديل عليه)")
        # المربع السحري اللي تقدر تمسح وتعدل فيه براحتك
        user_text = st.text_area("راجع النص هنا وعدل أي كلمات غير واضحة:", value=st.session_state['text_out'], height=450)
        
        st.markdown("---")
        if st.button("⚖️ استخراج ثغرات بطلان المحضر"):
            with st.spinner("جاري تحليل الثغرات ومطابقتها بالقانون المصري..."):
                try:
                    analysis_prompt = f"""
                    بصفتك محامي جنائي خبير (محامي الشيطان)، حلل النص التالي المستخرج من محضر شرطة:
                    {user_text}
                    
                    المطلوب:
                    1. استخراج ثغرات البطلان (بطلان قبض، تفتيش، تناقض، إلخ).
                    2. ذكر مواد قانون الإجراءات الجنائية المصري ذات الصلة.
                    3. تقديم نصيحة للمحامي لكيفية استغلال هذه الثغرات في المرافعة.
                    """
                    analysis = model.generate_content(analysis_prompt)
                    st.subheader("📋 تقرير محامي الشيطان:")
                    st.success(analysis.text)
                except Exception as e:
                    st.error(f"خطأ أثناء التحليل: {str(e)}")
