import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="ميمو", layout="wide")

# محاولة قراءة الـ Key بطريقة أكثر مرونة
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("خطأ: لم يتم العثور على GEMINI_API_KEY في إعدادات الـ Secrets.")
        st.stop()
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في الإعداد: {e}")
    st.stop()

st.title("🤖 ميمو: السيستم الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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
            st.error("حدث خطأ أثناء الاتصال بجوجل، تأكد من الرمز في الـ Secrets.")
