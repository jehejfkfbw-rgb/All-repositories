import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from gtts import gTTS
import os
from datetime import datetime
import pytz
import requests
import random

# ==========================================
# 1. إعدادات تطبيق ميمو الذكي والتليجرام
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

TELEGRAM_BOT_TOKEN = "8394900129:AAENOZw1Zz0SNImSZB97ZKSMXUMudQRePg"     
TELEGRAM_CHAT_ID = "8672781771"          

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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "verification_code" not in st.session_state:
    st.session_state.verification_code = None
if "pending_email" not in st.session_state:
    st.session_state.pending_email = ""
if "step" not in st.session_state:
    st.session_state.step = "register"

# ==========================================
# دالة إرسال إشعار فوري على تليجرام
# ==========================================
def send_telegram_notification(email, action_text):
    current_time = datetime.now(pytz.timezone('Africa/Cairo')).strftime('%Y-%m-%d %I:%M:%S %p')
    message = f"🚨 تنبيه جديد من تطبيق ميمو!\n\n👤 المستخدم: {email}\n⚡ الحدث: {action_text}\n⏰ الوقت: {current_time}"
    
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

# ==========================================
# 2. شاشة تسجيل الدخول والتحقق
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1>🤖 مرحباً بك في ميمو الذكي</h1>
                <p style="color: gray;">تسجيل الدخول بالبريد الإلكتروني للوصول الشامل</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.step == "register":
            user_input_email = st.text_input("أدخل بريدك الإلكتروني (Gmail):", placeholder="example@gmail.com")
            
            if st.button("إرسال كود التحقق", use_container_width=True):
                if user_input_email and "@gmail.com" in user_input_email:
                    code = str(random.randint(1000, 9999))
                    st.session_state.verification_code = code
                    st.session_state.pending_email = user_input_email
                    st.session_state.step = "verify"
                    st.success(f"تم توليد كود التحقق! (للاستخدام المباشر، الكود هو: {code})")
                    st.rerun()
                else:
                    st.error("الرجاء إدخال بريد جوجل صحيح يحتوي على @gmail.com")
                    
        elif st.session_state.step == "verify":
            st.info(f"أدخل الكود المرسل للبريد: {st.session_state.pending_email}")
            entered_code = st.text_input("أدخل رمز التحقق (4 أرقام):")
            
            if st.button("تأكيد وتسجيل الدخول", use_container_width=True):
                if entered_code == st.session_state.verification_code:
                    st.session_state.logged_in = True
                    st.session_state.user_email = st.session_state.pending_email
                    
                    # 🚀 إرسال إشعار فوري لتليجرام لحظة نجاح تسجيل الدخول!
                    send_telegram_notification(st.session_state.user_email, "قام بتسجيل الدخول إلى التطبيق بنجاح!")
                    
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("رمز التحقق غير صحيح.")
    
    st.stop()

# ==========================================
# بقية أقسام التطبيق (شات وتوليد صور والأدمن)
# ==========================================
def text_to_speech(text, filename="memo_voice.mp3"):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("-", " ")
        tts = gTTS(text=clean_text, lang='ar', slow=False)
        tts.save(filename)
        return filename
    except:
        return None

st.sidebar.title("🤖 ميمو AI - InnovaSoft")
st.sidebar.success(f"مرحباً: {st.session_state.user_email}")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.step = "register"
    st.rerun()

st.sidebar.markdown("---")
menu_options = ["💬 الشات الصوتي الذكي", "🎨 توليد الصور بالذكاء الاصطناعي", "📊 لوحة تحكم الأدمن (سجل الأبحاث)"]
app_mode = st.sidebar.radio("اختر القسم:", menu_options)

if app_mode == "💬 الشات الصوتي الذكي":
    st.title("💬 ميمو - الشات الصوتي الذكي")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك..."):
        send_telegram_notification(st.session_state.user_email, f"سؤال في الشات: {user_prompt}")
        
        if "طورك" in user_prompt or "صنعك" in user_prompt or "من أنت" in user_prompt or "صاحب الشركة" in user_prompt:
            bot_reply = "Mohamed Adel"
        else:
            try:
                response = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": user_prompt}])
                bot_reply = str(response)
            except Exception as e:
                bot_reply = f"خطأ: {e}"

        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة:")
    if st.button("توليد"):
        if image_prompt:
            send_telegram_notification(st.session_state.user_email, f"بحث عن صورة: {image_prompt}")
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(image_prompt)}?width=1024&height=1024&nologo=true")

elif app_mode == "📊 لوحة تحكم الأدمن (سجل الأبحاث)":
    st.title("📊 لوحة تحكم الأدمن")
    if os.path.exists("search_logs.txt"):
        with open("search_logs.txt", "r", encoding="utf-8") as f:
            st.code(f.read(), language="text")
    else:
        st.info("لا توجد سجلات حتى الآن.")
