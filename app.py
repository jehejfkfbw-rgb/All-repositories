import streamlit as st
from g4f.client import Client

# تصميم الواجهة (Custom CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 ميمو: المساعد الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع ميمو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ميمو يفكر..."):
            try:
                client = Client()
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception:
                st.error("عذراً، ميمو يحتاج لحظة للاتصال. حاول مرة أخرى!")
