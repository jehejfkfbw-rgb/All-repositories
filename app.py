import streamlit as st
import google.generativeai as genai

# إعداد الـ API باستخدام الـ Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("تأكد من وضع الـ API Key في الـ Secrets")

st.set_page_config(page_title="ميمو الذكي", layout="wide")
st.title("🤖 ميمو: السيستم الذكي")

tab1, tab2, tab3 = st.tabs(["💬 ميمو الذكي", "✅ المهام", "💻 مكتبة الأكواد"])

with tab1:
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
                st.error("حدث خطأ في الاتصال بجوجل، تأكد من الـ API Key.")

with tab2:
    st.info("⚠️ هذا القسم قيد التطوير حالياً، انتظر التحديثات القادمة!")

with tab3:
    st.warning("🚧 هذا القسم قيد التطوير حالياً، ترقبوا الإضافات قريباً!")
