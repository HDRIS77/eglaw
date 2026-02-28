import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعدادات الصفحة والذكاء الاصطناعي
st.set_page_config(page_title="المحامي الذكي - النسخة الاحترافية", layout="wide", page_icon="⚖️")

# استدعاء المفتاح من إعدادات Streamlit السرية
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# تصميم الواجهة
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منصة (المحامي الذكي) للتحليل القانوني والدستوري")
st.info("ارفع صور المحضر أو ملف القضية، وسيقوم النظام باستخراج النص، تحليل الثغرات، وإعداد مسودة مرافعة.")

# 2. منطقة رفع الملفات
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_files = st.file_uploader("ارفع صور المحضر (JPG/PNG)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# 3. معالجة النصوص (OCR والتحويل)
extracted_text = ""
if uploaded_files:
    st.subheader("📝 النص المستخرج من المحضر (يمكنك التعديل)")
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        # إرسال الصورة لـ Gemini لقراءتها (OCR متطور جداً للخط اليدوي)
        response = model.generate_content(["اقرأ هذا الخط اليدوي في المحضر المصري بدقة وحوله لنص مكتوب. حافظ على المصطلحات القانونية كما هي.", image])
        extracted_text += response.text + "\n"
    
    # مربع النص القابل للتعديل اللي طلبته
    final_text = st.text_area("راجع النص هنا وعدل أي كلمة غير مفهومة:", value=extracted_text, height=300)

# 4. محرك "محامي الشيطان" والتحليل القانوني
if extracted_text:
    with col2:
        st.subheader("🛠️ أدوات التحليل")
        analysis_type = st.selectbox("اختر نوع التحليل المطلوبة:", 
                                   ["استخراج ثغرات بطلان المحضر", "إعداد مسودة مرافعة كاملة", "مطابقة الواقعة بالدستور المصري", "استشارة قانونية حرة"])
        
        witnesses = st.text_input("أسماء الشهود أو الأدلة الإضافية (كاميرات، صور):")
        
        if st.button("إرسال القضية لـ (محامي الشيطان) للتحليل"):
            prompt = f"""
            أنت الآن تلعب دور "محامي الشيطان" ومستشار قانوني مصري خبير.
            بناءً على نص المحضر التالي:
            {final_text}
            
            وبناءً على الأدلة الإضافية: {witnesses}
            
            المطلوب:
            1. استخرج ثغرات البطلان (بطلان القبض، بطلان التفتيش، التناقض في أقوال الشهود).
            2. اربط كل ثغرة بمادة محددة من قانون الإجراءات الجنائية المصري أو الدستور المصري.
            3. صغ لي مرافعة قوية بصيغة PDF تتضمن الدفوع والطلبات.
            4. كن ناقداً جداً وحاول إيجاد أضعف نقطة في محضر الشرطة.
            """
            
            with st.spinner("جاري مراجعة الدستور والقوانين وتحضير الدفاع..."):
                full_analysis = model.generate_content(prompt)
                st.markdown("### 📄 تقرير التحليل القانوني")
                st.write(full_analysis.text)
                
                # إمكانية التحميل كملف نصي (مبدئياً)
                st.download_button("تحميل المرافعة والتحليل", full_analysis.text, file_name="defense_draft.txt")
