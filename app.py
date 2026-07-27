from gtts import gTTS
import google.generativeai as genai
import os
import requests
import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق ميمو - Memo AI", page_icon="🤖", layout="centered")

# بيانات بوت التليجرام والـ Chat ID الخاص بك
TELEGRAM_BOT_TOKEN = "حط_التوكن_بتاع_البوت_هنا"
TELEGRAM_CHAT_ID = "8672781771"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

if "app_opened_alert" not in st.session_state:
    send_telegram_alert("🚨 *تنبيه:* تم فتح تطبيق ميمو الذكي بنجاح!")
    st.session_state.app_opened_alert = True

st.title("تطبيق ميمو - Memo AI 🤖")
st.write("أهلاً بك يا فنان! اسأل أي سؤال وميمو هيجاوبك فوراً وبصوت كمان.")

# مفتاح جوجل جيمناي الرسمي
GEMINI_API_KEY = "حط_مفتاح_جيمناي_هنا"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

with st.sidebar:
    st.header("لوحة التحكم")
    if st.button("🗑️ مسح محادثة الشات"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if user_input := st.chat_input("اكتب سؤالك هنا يا فنان..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    
    send_telegram_alert(f"💬 *سؤال جديد:*\n{user_input}")

    with st.chat_message("assistant"):
        with st.spinner("ميمو بيفكر وبيكتب الإجابة..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                bot_response = response.text
            except Exception as e:
                bot_response = "عفواً يا فنان، اتأكد من صحة مفتاح الجيمناي (API Key) في الكود."

            st.markdown(bot_response)
            
            try:
                tts = gTTS(text=bot_response[:300], lang='ar')
                tts.save("response.mp3")
                st.audio("response.mp3", format="audio/mp3")
            except:
                pass
