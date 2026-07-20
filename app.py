import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="ميمو الذكي", layout="wide")

# إعداد الـ API Key من الـ Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("مشكلة في الربط: تأكد من وضع الـ API Key في الـ Secrets بشكل صحيح.")
    st.stop()

st.title("🤖 ميمو: السيستم الذكي")

# التبويبات
tab1, tab2, tab3 = st.tabs(["💬 ميمو الذكي", "✅ المهام", "💻 مكتبة الأكواد"])

with tab1:
    # تهيئة الشات
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل القديمة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال سؤال المستخدم
    if prompt := st.chat_input("اسأل ميمو أي شيء..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ميمو بيفكر..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("حدث خطأ أثناء الرد، تأكد من صحة الـ API Key.")

with tab2:
    st.info("⚠️ قسم المهام قيد التطوير.")

with tab3:
    st.warning("🚧 قسم الأكواد قيد التطوير.")
