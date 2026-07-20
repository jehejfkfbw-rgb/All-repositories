import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="ميمو الذكي", layout="centered")

# إعداد الاتصال
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام هذا النموذج المستقر
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")
    st.stop()

st.title("🤖 ميمو الذكي")
st.caption("تطوير: محمد عادل أحمد")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً! كيف أساعدك اليوم؟"}]

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
            st.error("حدث خطأ، تأكد من أن مفتاح الـ API يعمل.")

with st.sidebar:
    st.header("الأقسام")
    st.success("🤖 الدردشة (مفعل)")
    st.divider()
    st.write("🛠️ تحليل البيانات (قيد التطوير)")
    st.write("🛠️ المساعد البرمجي (قيد التطوير)")
    st.info("تطوير: محمد عادل أحمد")
