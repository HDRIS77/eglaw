import streamlit as st
import os
from groq import Groq
from PIL import Image

# 1. إعدادات المظهر (ثيم محامي الشيطان الأسود)
st.set_page_config(page_title="محامي الشيطان Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #ff0000 0%, #000000 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; border: 1px solid #444; }
    h1, h2 { color: #ff0000 !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. سحب المرجع القانوني أوتوماتيكياً
def load_law_reference():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

LAW_BASE = load_law_reference()

# 3. إعداد محرك Groq (المفتاح السري)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("⚖️ منصة محامي الشيطان - إصدار الصور والتحليل")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 ارفع صورة المحضر")
    uploaded_file = st.file_uploader("اختر صورة (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    # سيتم عرض الصورة هنا
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="المحضر المرفوع", use_container_width=True)
        st.info("💡 نصيحة: حالياً يفضل نسخ نص المحضر يدوياً في المربع المقابل لضمان أعلى دقة في التحليل القانوني.")

with col2:
    st.subheader("📝 مربع النص والتحليل")
    # المربع اللي هتحط فيه نص المحضر
    case_text = st.text_area("راجع النص هنا قبل التحليل:", height=400, placeholder="انسخ نص المحضر المكتوب هنا...")
    
    if st.button("⚖️ استخراج ثغرات البطلان"):
        if not case_text:
            st.error("يا بطل، لازم تحط نص المحضر في المربع ده الأول!")
        else:
            with st.spinner("محامي الشيطان يطابق النص مع الدستور المصري..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"أنت محامي الشيطان، خبير جنائي مصري. مرجعك: {LAW_BASE}. استخرج ثغرات بطلان الإجراءات بدقة."
                            },
                            {
                                "role": "user",
                                "content": f"حلل هذا المحضر: {case_text}"
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("### 📋 التقرير القانوني:")
                    st.success(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {str(e)}")

# 4. الشريط الجانبي
st.sidebar.markdown(f"### 🛡️ الحالة\nالمرجع القانوني: **نشط**\nالمحرك: **Groq Llama 3**")
