import os
import google.generativeai as genai
import requests
import streamlit as st

# إعدادات صفحة Streamlit
st.set_page_config(page_title="تطبيق ميمو - Memo AI", page_icon="🤖", layout="centered")

# إعدادات التليجرام والتنبيهات
TELEGRAM_BOT_TOKEN = "حط_التوكن_بتاع_البوت_هنا"
TELEGRAM_CHAT_ID = "8672781771"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# إرسال تنبيه فتح التطبيق
if "app_opened_alert" not in st.session_state:
    send_telegram_alert("🚨 *تنبيه:* شخص ما فتح تطبيق ميمو الأصلي!")
    st.session_state.app_opened_alert = True

# إعداد مفتاح جوجل جيمناي الذكي (يقرا من البيئة أو حطه هنا مباشرة لو حابب)
# API_KEY = "حط_مفتاح_جيمناي_هنا"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "حط_مفتاح_جيمناي_هنا"))

# استخدام نموذج جيمناي الأصلي
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

# واجهة التطبيق
st.title("تطبيق ميمو - Memo AI 🤖")
st.write("أهلاً بك يا فنان! اسأل ميمو في أي حاجة وهيجاوبك فوراً.")

# الشريط الجانبي
with st.sidebar:
    st.header("لوحة التحكم")
    if st.button("مسح محادثة الشات"):
        st.session_state.chat_history = model.start_chat(history=[])
        st.rerun()

# تهيئة الشات الحقيقي
if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# عرض الرسائل السابقة
for message in st.session_state.chat_history.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# استقبال رسالة المستخدم الحقيقية وإرسالها للذكاء الاصطناعي والتليجرام
if user_input := st.chat_input("اكتب رسالتك يا فنان..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # إرسال للتليجرام
    send_telegram_alert(f"💬 *رسالة جديدة من المستخدم:*\n{user_input}")

    # الرد الحقيقي من جيمناي
    with st.chat_message("assistant"):
        with st.spinner("ميمو بيفكر وبيكتب..."):
            response = st.session_state.chat_history.send_message(user_input)
            st.markdown(response.text)
