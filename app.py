import streamlit as st
import os

# --- إعدادات الواجهة (اللون الأسود) ---
st.set_page_config(page_title="محامي الشيطان Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #00ffcc; border: 1px solid #30363d; font-size: 18px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #ff4b4b 0%, #000000 100%); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
    h1, h2 { color: #ff4b4b !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# --- وظيفة السحب الأوتوماتيكي للمرجع القانوني ---
def load_law_reference():
    if os.path.exists("law_reference.txt"):
        with open("law_reference.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "الدستور المصري وقانون الإجراءات الجنائية."

# سحب البيانات أوتوماتيكياً عند بداية التشغيل
LAW_BASE = load_law_reference()

st.title("😈 منصة محامي الشيطان - التحليل الدستوري")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📂 رفع قضية جديدة")
    file = st.file_uploader("ارفع المحضر (JPG/PNG)", type=["jpg", "png", "jpeg"])
    if file:
        st.image(file, use_container_width=True)
        if st.button("🔍 استخراج النص بالذكاء الاصطناعي"):
            st.info("سيتم الربط مع الـ API في الخطوة النهائية..")

with col2:
    st.subheader("📝 مربع التعديل والتحليل")
    # النص المستخرج سيظهر هنا
    extracted_text = st.text_area("راجع النص هنا:", height=350, placeholder="بانتظار رفع القضية...")
    
    if st.button("⚖️ تفعيل وضع محامي الشيطان (تحليل الثغرات)"):
        # هنا السحر: دمج المرجع أوتوماتيكياً مع التفكير
        st.warning("جاري مطابقة النص مع الدستور المصري المستند من الملف...")
        
        # التفكير اللي هيروح للـ API (بشكل مخفي)
        devil_prompt = f"""
        بصفتك 'محامي الشيطان'، حلل المحضر التالي بناءً على المرجع القانوني: {LAW_BASE}
        النص المراد تحليله: {extracted_text}
        المطلوب: استخرج كل الثغرات الدستورية والقانونية بلهجة حادة وذكية.
        """
        # st.write(devil_prompt) # لو عايز تشوف الأمر اللي بيروح للـ AI
