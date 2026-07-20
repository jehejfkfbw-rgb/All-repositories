import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ميمو - النسخة الاحترافية", page_icon="🤖", layout="centered")

# --- تهيئة الاتصال بـ Gemini ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام النموذج المحدث
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ خطأ في إعدادات المفتاح. تأكد من وضعه في الـ Secrets.")
    st.stop()

# --- التصميم والواجهة ---
st.title("🤖 ميمو الذكي")
st.caption("المساعد الشخصي الذكي - تطوير: محمد عادل أحمد")

# --- إدارة تاريخ المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً يا محمد! كيف أساعدك اليوم؟"}
    ]

# --- عرض سجل الرسائل ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- منطقة إدخال المستخدم ---
if prompt := st.chat_input("تحدث مع ميمو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # بدء محادثة
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")

# --- القائمة الجانبية (الأقسام) ---
with st.sidebar:
    st.header("أقسام ميمو")
    st.success("🤖 الدردشة الذكية (مفعل)")
    
    st.divider()
    
    st.subheader("أقسام قيد التطوير:")
    st.write("🛠️ تحليل البيانات (قيد التطوير)")
    st.write("🛠️ المساعد البرمجي (قيد التطوير)")
    st.write("🛠️ نظام التنبيهات (قيد التطوير)")
    
    st.divider()
    st.info("تطوير: المطور محمد عادل أحمد")
    
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
