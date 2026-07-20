import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="ميمو", layout="centered")

# إعداد الـ API Key من الـ Secrets بأمان
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("لم يتم العثور على الـ API Key في الـ Secrets. تأكد من إضافته هناك.")
    st.stop()

st.title("🤖 ميمو: السيستم الذكي")

# تهيئة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# استقبال رسائل المستخدم
if prompt := st.chat_input("تحدث مع ميمو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("حدث خطأ في الاتصال بجوجل.")
