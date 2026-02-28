import streamlit as st
import os
from groq import Groq
from PIL import Image

# 1. إعدادات المنصة (هيبة محامي الشيطان)
st.set_page_config(page_title="منصة محامي الشيطان Pro - إصدار المستشارين", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea, .stTextInput input { background-color: #161b22; color: #ff4b4b; border: 1px solid #30363d; font-size: 17px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #8b0000 0%, #000000 100%); color: white; border-radius: 10px; height: 55px; font-weight: bold; border: 1px solid #ff0000; }
    .stButton>button:hover { box-shadow: 0px 0px 20px #ff0000; cursor: pointer; }
    h1, h2, h3 { color: #ff0000 !important; text-align: right; }
    .charge-box { background-color: #260101; padding: 20px; border-radius: 10px; border: 1px solid #ff0000; margin-top: 10px; }
    .witness-box { background-color: #1e252e; padding: 15px; border-radius: 10px; border-right: 5px solid #ff0000; margin-bottom: 10px; }
    .pro-tips { background-color: #002244; padding: 20px; border-radius: 10px; border-right: 5px solid #00aaff; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة المحرك
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if 'witnesses' not in st.session_state: st.session_state.witnesses = []

def load_law():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f: return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

LAW_BASE = load_law()

st.title("😈 منصة محامي الشيطان - إصدار المستشار القانوني")

tab1, tab2, tab3 = st.tabs(["🔍 تحليل التهمة والمصير", "👥 بنك الشهود والأدلة", "🔥 مذكرة الدفاع وتوصيات الجلسة"])

with tab1:
    col_in, col_out = st.columns([1, 1])
    with col_in:
        st.subheader("📁 فحص المحضر")
        file = st.file_uploader("ارفع المحضر", type=["jpg", "png", "jpeg"])
        mahdar_input = st.text_area("نص المحضر (المادة الخام للثغرات):", height=300)
        
        if st.button("⚖️ تحليل التهمة والعقوبة المتوقعة"):
            if mahdar_input:
                with st.spinner("جاري استخراج المواد العقابية..."):
                    charge_resp = client.chat.completions.create(
                        messages=[{"role": "system", "content": f"أنت خبير جنائي مصري. حدد التهمة، المواد العقابية، والعقوبة المتوقعة من هذا المحضر: {mahdar_input} بناءً على {LAW_BASE}"}],
                        model="llama-3.3-70b-versatile"
                    )
                    st.session_state.charge_info = charge_resp.choices[0].message.content
            else: st.error("أدخل النص أولاً!")

    with col_out:
        st.subheader("⚖️ المصير القانوني (قبل الدفاع)")
        if 'charge_info' in st.session_state:
            st.markdown(f"<div class='charge-box'>{st.session_state.charge_info}</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("👥 إدارة شهود النفي")
    with st.expander("➕ إضافة شاهد جديد للقائمة", expanded=True):
        w_name = st.text_input("الاسم")
        w_say = st.text_area("الأقوال التي ستنسف الاتهام")
        w_status = st.checkbox("طلب استدعاء رسمي")
        if st.button("✅ تسجيل الشاهد"):
            if w_name and w_say:
                st.session_state.witnesses.append({"name": w_name, "say": w_say, "status": "رسمي" if w_status else "ودي"})
                st.success(f"تم تسجيل: {w_name}")
            else: st.error("بيانات ناقصة!")

    for i, wit in enumerate(st.session_state.witnesses):
        st.markdown(f"<div class='witness-box'><b>{i+1}. {wit['name']}</b>: {wit['say']} ({wit['status']})</div>", unsafe_allow_html=True)

with tab3:
    st.subheader("📜 المخرجات النهائية للمحامي")
    if st.button("🚀 توليد المذكرة + خطة إدارة الجلسة"):
        if not mahdar_input: st.error("أين بيانات القضية؟")
        else:
            with st.spinner("جاري صياغة الاستراتيجية الهجومية..."):
                wit_sum = "\n".join([f"- {w['name']}: {w['say']}" for w in st.session_state.witnesses])
                
                final_prompt = f"""
                أنت 'محامي الشيطان'. حلل المحضر: {mahdar_input} والشهود: {wit_sum}.
                المطلوب مخرجان منفصلان:
                1. مذكرة دفاع رسمية: (دفوع بطلان، تناقض أقوال، طلبات ختامية بالبراءة).
                2. قسم 'توصيات سرية للمحامي': (نصائح للمحامي كيف يستجوب المجني عليه، أسئلة فخ للشهود، ماذا يطلب من القاضي تحديداً في أول جلسة بناءً على الثغرات).
                استخدم لهجة حاسمة ومواد القانون المصري.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": "أنت مستشار قانوني جنائي لا يرحم."},
                              {"role": "user", "content": final_prompt}],
                    model="llama-3.3-70b-versatile"
                )
                
                # عرض النتائج
                result = response.choices[0].message.content
                st.markdown("### 📄 مذكرة الدفاع وتوصيات الجلسة")
                st.success(result)
                st.download_button("📥 تحميل التقرير الكامل", result, file_name="pro_legal_strategy.txt")
