import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ميمو - النسخة المستقرة", page_icon="🤖", layout="centered")

# --- تهيئة الاتصال بـ Gemini ---
# ملاحظة: تأكد من وجود GEMINI_API_KEY في صفحة Secrets على Streamlit
def initialize_model():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # استخدام نموذج مستقر ومتوافق
        return genai.GenerativeModel('gemini-1.0-pro')
    except Exception as e:
        st.error("⚠️ خطأ في الاتصال: يرجى التأكد من إضافة GEMINI_API_KEY في الـ Secrets.")
        return None

model = initialize_model()

# --- واجهة المستخدم ---
st.title("🤖 ميمو الذكي")
st.caption("المساعد الشخصي - تطوير: محمد عادل أحمد")

# --- إدارة الحالة (سجل المحادثة) ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً يا محمد! أنا ميمو، كيف يمكنني مساعدتك اليوم؟"}]

# --- عرض تاريخ المحادثة ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- معالجة الرسائل ---
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    if model is None:
        st.error("الموديل غير متاح.")
        st.stop()
        
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # عرض رد ميمو
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ أثناء توليد الرد: {e}")

# --- القائمة الجانبية (الأقسام) ---
with st.sidebar:
    st.header("أقسام ميمو")
    st.success("✅ الدردشة الذكية (مفعل)")
    st.divider()
    st.write("🛠️ تحليل البيانات (قيد التطوير)")
    st.write("🛠️ المساعد البرمجي (قيد التطوير)")
    st.write("🛠️ نظام التنبيهات (قيد التطوير)")
    st.divider()
    st.info("تطوير: المطور محمد عادل أحمد")
    
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
