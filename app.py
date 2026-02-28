import streamlit as st
import os
from groq import Groq
from PIL import Image

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="منصة المحامي الذكي - مذكرات المرافعة", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea, .stTextInput input { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #ff0000 0%, #000000 100%); color: white; border-radius: 10px; height: 50px; font-weight: bold; }
    h1, h2, h3 { color: #ff0000 !important; text-align: right; }
    .law-card { background-color: #1e252e; padding: 20px; border-radius: 10px; border-right: 5px solid #ff0000; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة المحرك
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def load_law():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f: return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

LAW_BASE = load_law()

st.title("😈 منصة محامي الشيطان - إعداد مذكرة المرافعة")

# 3. تقسيم الواجهة لثلاثة أقسام (المحضر | الشهود والأدلة | المذكرة)
tab1, tab2, tab3 = st.tabs(["📝 نص المحضر", "👥 الشهود والأدلة", "⚖️ صياغة المذكرة"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📁 رفع المحضر")
        file = st.file_uploader("ارفع صورة المحضر", type=["jpg", "png", "jpeg"])
        if file: st.image(file, use_container_width=True)
    with col2:
        st.subheader("🖋️ مراجعة النص")
        mahdar_text = st.text_area("تأكد من النص المستخرج من المحضر هنا:", height=400)

with tab2:
    st.subheader("🕵️ إضافة عناصر الدفاع")
    
    # قسم الشهود
    st.markdown("### 👥 أقوال الشهود")
    witness_name = st.text_input("اسم الشاهد")
    witness_say = st.text_area("ماذا سيشهد به؟")
    witness_status = st.checkbox("تعذر إحضار الشاهد (اطلب من المحكمة استدعاءه)")
    
    st.markdown("---")
    
    # قسم الأدلة
    st.markdown("### 📂 الأدلة الفنية والمادية")
    evidence_type = st.selectbox("نوع الدليل", ["كاميرات مراقبة", "تقرير طبي", "مستند رسمي", "أخرى"])
    evidence_desc = st.text_area("تفاصيل الدليل")
    evidence_missing = st.checkbox("الدليل ليس معي (اطلب من النيابة التحفظ عليه/ضمه)")

with tab3:
    st.subheader("📜 المذكرة النهائية والمطالب")
    if st.button("🔥 صياغة مذكرة المرافعة وطلبات الدفاع"):
        if not mahdar_text:
            st.error("من فضلك ضع نص المحضر أولاً في القسم الأول!")
        else:
            with st.spinner("جاري دمج المحضر مع الشهود والأدلة لصياغة المذكرة..."):
                # بناء الـ Prompt المعقد
                full_context = f"""
                المحضر الأصلي: {mahdar_text}
                الشاهد: {witness_name} (قوله: {witness_say}) - حالة الشاهد: {'طلب استدعاء جبري' if witness_status else 'متاح'}
                الدليل: {evidence_type} ({evidence_desc}) - حالة الدليل: {'طلب ضم مستندات' if evidence_missing else 'مرفق'}
                المرجع القانوني: {LAW_BASE}
                """
                
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "أنت محامي جنائي مصري محترف. صغ مذكرة مرافعة رسمية للمحكمة تشمل: الدفوع القانونية، تحليل الأدلة والشهود، وخاتمة بطلبات ختامية جازمة (مثل براءة المتهم، طلب سماع شهود، أو ضم تقارير)."},
                        {"role": "user", "content": f"بناءً على المعطيات التالية، اكتب مذكرة الدفاع الكاملة: {full_context}"}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                st.markdown("### 📄 مسودة مذكرة المرافعة")
                st.success(response.choices[0].message.content)
                
                # زر التحميل (تجريبي)
                st.download_button("📥 تحميل المذكرة كملف نصي", response.choices[0].message.content, file_name="defense_memo.txt")
