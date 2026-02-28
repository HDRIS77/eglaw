import streamlit as st
import os
from groq import Groq

# 1. إعدادات المظهر (الثيم الأسود لمحامي الشيطان)
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

# 2. وظيفة سحب الدستور المصري أوتوماتيكياً من ملفك
def load_law_reference():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية المصري."

LAW_BASE = load_law_reference()

# 3. إعداد محرك Groq بمفتاحك اللي عملتله Allow
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("⚖️ منصة محامي الشيطان - التحليل الدستوري")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 تفاصيل المحضر")
    # هنا هتحط نص المحضر اللي عايز تحلله
    case_text = st.text_area("انسخ نص المحضر هنا:", height=500, placeholder="اكتب أو انسخ نص المحضر هنا للتحليل...")

with col2:
    st.subheader("🔥 التحليل القانوني")
    if st.button("⚖️ استخراج ثغرات البطلان (محامي الشيطان)"):
        if not case_text:
            st.error("من فضلك أدخل نص المحضر أولاً في الخانة المخصصة!")
        else:
            with st.spinner("جاري فحص النصوص ومطابقتها بالدستور المصري..."):
                try:
                    # إرسال البيانات للمحرك الجديد
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"""أنت 'محامي الشيطان'، خبير في الثغرات القانونية المصرية. 
                                مرجعك هو: {LAW_BASE}. 
                                حلل النص واستخرج بطلان القبض أو التفتيش أو الإجراءات بأسلوب قانوني قوي."""
                            },
                            {
                                "role": "user",
                                "content": f"حلل هذا المحضر واستخرج الثغرات: {case_text}",
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    # عرض النتيجة النهائية
                    st.markdown("### 📋 تقرير الثغرات المستخرجة:")
                    st.success(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال: {str(e)}")

# 4. حالة النظام في الجنب
st.sidebar.markdown(f"### 🛡️ المكتبة القانونية\nتم تحميل مرجع: **الدستور المصري**")
