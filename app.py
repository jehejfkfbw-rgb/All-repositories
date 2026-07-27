import streamlit as st
from groq import Groq
from PIL import Image, ImageEnhance
import urllib.parse
from datetime import datetime
import pytz
import requests
import os

# ==========================================
# 1. إعدادات التطبيق وتليجرام
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

TELEGRAM_BOT_TOKEN = "8394900129:AAENOZw1Zz0SNImSZB97ZKSMXUMudQRePg"     
TELEGRAM_CHAT_ID = "8672781771"          

# إعداد مفتاح Groq الذكي (حط مفتاح الـ Groq API هنا، بتب’ مجاناً من موقعهم)
GROQ_API_KEY = "حط_مفتاح_groq_هنا"
client = Groq(api_key=GROQ_API_KEY)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f4f4f4;
    }
    h1, h2, h3 {
        color: #C8102E;
    }
    .stButton>button {
        background-color: #C8102E;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# دالة إرسال إشعار فوري على تليجرام
# ==========================================
def send_telegram_notification(email, action_text):
    current_time = datetime.now(pytz.timezone('Africa/Cairo')).strftime('%Y-%m-%d %I:%M:%S %p')
    message = f"🚨 إشعار من تطبيق ميمو!\n\n👤 المستخدم: {email}\n🔍 التفاصيل: {action_text}\n⏰ الوقت: {current_time}"
    
    log_entry = f"[{current_time}] | User: {email} | Action: {action_text}\n"
    with open("search_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

current_user_email = "Mohamed Adel (عادل أحمد)"

# ==========================================
# 2. واجهة التطبيق الرئيسية
# ==========================================
st.sidebar.title("🤖 ميمو AI - InnovaSoft")
st.sidebar.success(f"مرحباً: {current_user_email}")

if st.sidebar.button("🗑️ مسح محادثة الشات"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "💬 الشات الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "📊 لوحة تحكم الأدمن (سجل الأبحاث)"
]
app_mode = st.sidebar.radio("اختر القسم:", menu_options)

if app_mode == "💬 الشات الذكي":
    st.title("💬 ميمو - الشات الذكي السريع (Groq)")
    st.write(f"أهلاً بك يا {current_user_email}، اسأل عن أي شيء وسأرد عليك فوراً بالإنترنت وبأعلى سرعة!")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "أهلاً يا فنان! أنا جاهز بمكتبة Groq السريعة، اسأل اللي يعجبك والدنيا هتمشي صواريخ."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك أو بحثك هنا..."):
        send_telegram_notification(current_user_email, f"البحث عن: {user_prompt}")
        
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("ميمو بيبحث وبيرد بالسرعة القصوى..."):
                try:
                    # استخدام نموذج Groq السارق للوقت (llama3) للرد الفوري
                    chat_completion = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    bot_reply = chat_completion.choices[0].message.content
                except Exception as e:
                    bot_reply = f"عذراً يا فنان، تأكد من صحة مفتاح Groq API في الكود: {e}"
                
                st.markdown(bot_reply)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة التي تريد توليدها:")
    if st.button("توليد الصورة"):
        if image_prompt:
            send_telegram_notification(current_user_email, f"البحث وتوليد صورة عن: {image_prompt}")
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(image_prompt)}?width=1024&height=1024&nologo=true", caption=image_prompt)

elif app_mode == "📊 لوحة تحكم الأدمن (سجل الأبحاث)":
    st.title("📊 لوحة تحكم الأدمن - السجلات")
    if os.path.exists("search_logs.txt"):
        with open("search_logs.txt", "r", encoding="utf-8") as f:
            st.code(f.read(), language="text")
    else:
        st.info("لا توجد سجلات بحث حتى الآن.")
