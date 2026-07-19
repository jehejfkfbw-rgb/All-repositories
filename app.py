import streamlit as st
from datetime import date

# إعدادات الصفحة
st.set_page_config(page_title="ميمو", page_icon="🤖")

# كود إخفاء العلامات
hide_style = "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🤖 أهلاً بك في ميمو الذكي")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال الرسالة
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ذكاء ميمو في الرد
    response = "أنا ميمو، لم أفهم هذا السؤال بعد." # الرد الافتراضي
    
    if "النهارده" in prompt or "تاريخ" in prompt:
        response = f"النهارده {date.today().strftime('%A %d-%m-%Y')} يا محمد!"
    elif "حالك" in prompt:
        response = "أنا بخير يا بطل، بفضل شغلك الجامد في الكود!"
    elif "اسمك" in prompt:
        response = "اسمي ميمو، المساعد الذكي الخاص بك."

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
