import streamlit as st
import os
from groq import Groq

# 1. إعدادات المظهر (الأسود والأحمر - هيبة المحاماة)
st.set_page_config(page_title="محامي الشيطان Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; border-radius: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #8b0000 0%, #000000 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; border: 1px solid #444; }
    .stButton>button:hover { border: 1px solid #ff0000; box-shadow: 0px 0px 15px #ff0000; }
    h1, h2 { color: #ff0000 !important; text-align: right; font-family: 'Cairo', sans-serif; }
    .law-sidebar { background-color: #1e252e; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. سحب الدستور المصري أوتوماتيكياً من ملفك
def load_law_reference():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

LAW_BASE = load_law_reference()

# 3. إعداد محرك Groq بمفتاحك الجديد
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.title("⚖️ منصة محامي الشيطان - التحليل الدستوري الذكي")
st.markdown("---")

# 4. تقسيم واجهة المستخدم
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 تفاصيل القضية الجديدة")
    # بما أن Groq متخصص نصوص، سنضع مربع إدخال نص المحضر مباشرة
    case_text = st.text_area("انسخ نص محضر الشرطة هنا للتحليل:", height=450, placeholder="اكتب أو انسخ نص المحضر هنا...")
    
    with st.expander("📚 المرجع القانوني المستخدم حالياً"):
        st.info(LAW_BASE)

with col2:
    st.subheader("🔥 تحليل محامي الشيطان")
    if st.button("⚖️ استخراج ثغرات البطلان الآن"):
        if not case_text:
            st.error("من فضلك أدخل نص المحضر أولاً!")
        else:
            with st.spinner("جاري مطابقة النص مع الدستور المصري واستخراج الثغرات..."):
                try:
                    # بناء أمر "محامي الشيطان"
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"""أنت 'محامي الشيطان'، أكبر خبير قانوني في القانون الجنائي المصري. 
                                مرجعك هو: {LAW_BASE}. 
                                مهمتك: تحليل النص الذي سيقدمه المستخدم واستخراج كل ثغرات بطلان (القبض، التفتيش، الاستيقاف، التلبس) بناءً على الدستور المصري وقانون الإجراءات. 
                                كن حاداً، دقيقاً، واستخدم مواد القانون بقوة."""
                            },
                            {
                                "role": "user",
                                "content": f"حلل هذا النص واستخرج الثغرات القانونية فوراً: {case_text}",
                            }
                        ],
                        model="llama-3.3-70b-versatile", # أحدث وأقوى موديل متاح لك
                    )
                    
                    # عرض النتيجة
                    st.markdown("### 📋 التقرير القانوني النهائي:")
                    st.success(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التحليل: {str(e)}")

# 5. تذييل الصفحة
st.sidebar.markdown(f"### 🛡️ الحالة: متصل بالدستور المصري")
st.sidebar.write("المكتبة القانونية نشطة وجاهزة لسحب البيانات أوتوماتيكياً عند كل طلب.")
