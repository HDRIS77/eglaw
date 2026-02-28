import streamlit as st
import os
from groq import Groq
from PIL import Image

# 1. إعدادات المظهر (ثيم محامي الشيطان - أسود وأحمر)
st.set_page_config(page_title="محامي الشيطان Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #ff0000 0%, #000000 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; border: 1px solid #444; }
    .stButton>button:hover { border: 1px solid #ff0000; box-shadow: 0px 0px 15px #ff0000; }
    h1, h2 { color: #ff0000 !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة سحب المرجع القانوني أوتوماتيكياً
def load_law_reference():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

LAW_BASE = load_law_reference()

# 3. إعداد محرك Groq بمفتاحك gsk_...
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("⚖️ منصة محامي الشيطان - إصدار الصور والتحليل")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    # رجوع زرار الرفع اللي سألت عليه
    uploaded_file = st.file_uploader("اختر صورة المحضر (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المستند الذي سيتم تحليله", use_container_width=True)
        st.info("ℹ️ ملاحظة: قم بنسخ نص المحضر في المربع المقابل لضمان دقة تحليل 'محامي الشيطان'.")

with col2:
    st.subheader("📝 مربع التعديل والتحليل")
    # المربع السحري اللي هتحط فيه نص المحضر
    case_text = st.text_area("راجع أو انسخ نص المحضر هنا:", height=450, placeholder="ضع نص المحضر المكتوب هنا لتحويله لثغرات قانونية...")
    
    if st.button("⚖️ استخراج ثغرات البطلان"):
        if not case_text:
            st.error("يا بطل، لازم تحط نص المحضر في المربع ده الأول!")
        else:
            with st.spinner("جاري مطابقة النص مع الدستور المصري واستخراج الثغرات..."):
                try:
                    # إرسال البيانات للمحرك
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"أنت 'محامي الشيطان'، خبير في الثغرات القانونية المصرية. مرجعك هو: {LAW_BASE}. حلل النص بذكاء لاستخراج بطلان الإجراءات."
                            },
                            {
                                "role": "user",
                                "content": f"حلل هذا المحضر واستخرج ثغرات البطلان: {case_text}"
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.markdown("### 📋 التقرير القانوني النهائي:")
                    st.success(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال: {str(e)}")

# 4. الحالة في الجانب
st.sidebar.markdown(f"### 🛡️ مرجع القانون\nالحالة: **متصل بالدستور**")
