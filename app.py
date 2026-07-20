import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ميمو - النسخة الاحترافية", page_icon="🤖", layout="centered")

# --- تهيئة الاتصال بـ Gemini ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("⚠️ خطأ: يرجى التأكد من إضافة GEMINI_API_KEY في صفحة الـ Secrets.")
    st.stop()

# --- عنوان وتصميم التطبيق ---
st.title("🤖 ميمو الذكي")
st.subheader("مساعدك الشخصي المطور بلغة بايثون")

# --- إدارة تاريخ المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً يا محمد! أنا ميمو، كيف يمكنني مساعدتك اليوم؟"}
    ]

# --- عرض سجل الرسائل ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وظيفة إرسال الرسائل ---
def get_gemini_response(chat_history, user_input):
    # إنشاء جلسة دردشة ليتذكر ميمو السياق
    chat = model.start_chat(history=[])
    response = chat.send_message(user_input)
    return response.text

# --- منطقة إدخال المستخدم ---
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # عرض رد ميمو
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # استدعاء النموذج
            response_text = get_gemini_response(st.session_state.messages, prompt)
            
            # عرض الرد بشكل تدريجي (أنيق)
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")

# --- القائمة الجانبية (لمسات إضافية) ---
with st.sidebar:
    st.info("💡 نصيحة: ميمو يتذكر سياق حديثك الآن!")
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
