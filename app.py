import streamlit as st
import os
from groq import Groq
from PIL import Image

# 1. إعدادات المنصة (هيبة محامي الشيطان)
st.set_page_config(page_title="محامي الشيطان Pro - الدفاع الجبار", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea, .stTextInput input { background-color: #161b22; color: #ff4b4b; border: 1px solid #30363d; font-size: 17px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #8b0000 0%, #000000 100%); color: white; border-radius: 10px; height: 55px; font-weight: bold; border: 1px solid #ff0000; }
    .stButton>button:hover { box-shadow: 0px 0px 20px #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; text-align: right; }
    .charge-box { background-color: #260101; padding: 20px; border-radius: 10px; border: 1px solid #ff0000; margin-top: 10px; }
    .witness-box { background-color: #1e252e; padding: 15px; border-radius: 10px; border-right: 5px solid #ff0000; margin-bottom: 10px; }
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

st.title("😈 منصة محامي الشيطان - الدفاع الانتحاري")

tab1, tab2, tab3 = st.tabs(["🔍 تحليل المحضر والتهمة", "👥 الشهود والأدلة", "🔥 مذكرة الدفاع الجبارة"])

with tab1:
    col_in, col_out = st.columns([1, 1])
    with col_in:
        st.subheader("📁 رفع وتجهيز المحضر")
        file = st.file_uploader("ارفع المحضر هنا", type=["jpg", "png", "jpeg"])
        mahdar_input = st.text_area("انسخ نص المحضر هنا (ضروري للتحليل):", height=300)
        
        if st.button("⚖️ تكييف التهمة والعقوبة"):
            if mahdar_input:
                with st.spinner("محامي الشيطان يحدد مصيرك القانوني..."):
                    charge_resp = client.chat.completions.create(
                        messages=[{"role": "system", "content": f"أنت خبير قانوني مصري. بناءً على هذا المحضر والمرجع {LAW_BASE}، حدد التهمة الموجهة بدقة، والمواد القانونية المنطبقة، والعقوبة المتوقعة (سجن/غرامة) بوضوح تام وبدون تجميل."},
                                  {"role": "user", "content": mahdar_input}],
                        model="llama-3.3-70b-versatile"
                    )
                    st.session_state.charge_info = charge_resp.choices[0].message.content
            else: st.error("حط نص المحضر الأول!")

    with col_out:
        st.subheader("⚖️ التكييف القانوني والعقوبة")
        if 'charge_info' in st.session_state:
            st.markdown(f"<div class='charge-box'>{st.session_state.charge_info}</div>", unsafe_allow_html=True)
            st.warning("⚠️ هذه هي العقوبة لو استسلمت.. انتقل لقسم الشهود ثم المذكرة لننسف هذا الاتهام.")

with tab2:
    st.subheader("👥 إضافة شهود النفي (بلا حدود)")
    with st.expander("➕ إضافة شاهد جديد", expanded=True):
        w_name = st.text_input("اسم الشاهد")
        w_say = st.text_area("ماذا سيقول لنسف التهمة؟")
        w_status = st.checkbox("طلب استدعاء جبري من المحكمة")
        if st.button("✅ حفظ الشاهد"):
            if w_name and w_say:
                st.session_state.witnesses.append({"name": w_name, "say": w_say, "status": "استدعاء جبري" if w_status else "حاضر"})
                st.success(f"تم تسجيل الشاهد: {w_name}")
            else: st.error("اكمل البيانات!")

    for i, wit in enumerate(st.session_state.witnesses):
        st.markdown(f"<div class='witness-box'><b>{i+1}. {wit['name']}</b>: {wit['say']} ({wit['status']})</div>", unsafe_allow_html=True)
    if st.session_state.witnesses and st.button("🗑️ تفريغ الشهود"): 
        st.session_state.witnesses = []; st.rerun()

with tab3:
    st.subheader("📜 صياغة المذكرة الجبارة")
    if st.button("🔥 استخراج المذكرة بنهج محامي الشيطان"):
        if not mahdar_input: st.error("فين المحضر؟")
        else:
            with st.spinner("جاري صياغة مرافعة لا ترحم..."):
                wit_sum = "\n".join([f"- {w['name']}: {w['say']} ({w['status']})" for w in st.session_state.witnesses])
                final_prompt = f"""
                أنت 'محامي الشيطان'. لا تجمل الحقيقة. حلل هذا المحضر: {mahdar_input}
                بناءً على التهمة والعقوبة التي حددتها سابقاً: {st.session_state.get('charge_info', '')}
                وباستخدام هؤلاء الشهود: {wit_sum}
                والمرجع القانوني: {LAW_BASE}
                
                المطلوب:
                صياغة مذكرة دفاع "جبارة" تهدف للبراءة التامة أو أدنى عقوبة ممكنة.
                1. اضرب في مقتل بإثبات بطلان الإجراءات (المادة 30 إجراءات، 54 دستور).
                2. استغل التناقضات (مثل قصة المبالغ المالية والطلقات) لتسفيه الاتهام.
                3. صغ "طلبات ختامية" بصيغة هجومية تفرض على المحكمة سماع شهودك أو البراءة.
                يجب أن تكون اللهجة قانونية، شرسة، وحاسمة.
                """
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": "أنت محامي شيطان جنائي، لا تعرف الرحمة في الدفاع."},
                              {"role": "user", "content": final_prompt}],
                    model="llama-3.3-70b-versatile"
                )
                final_memo = response.choices[0].message.content
                st.markdown("### 📄 المذكرة النهائية:")
                st.success(final_memo)
                st.download_button("📥 تحميل مذكرة البراءة", final_memo, file_name="devil_defense.txt")
