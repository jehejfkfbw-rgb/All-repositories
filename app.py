import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from datetime import datetime
import pytz
import requests
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعدادات التطبيق وتليجرام
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

TELEGRAM_BOT_TOKEN = "8394900129:AAENOZw1Zz0SNImSZB97ZKSMXUMudQRePg"     
TELEGRAM_CHAT_ID = "8672781771"          

# بيانات الإيميل الخاص بك الذي ستقوم بالارسال منه
SENDER_EMAIL = "jehejfkfbw@gmail.com"        
SENDER_PASSWORD = "هنا_كلمة_مرور_التطبيق_الخاصة_بك"  # ضع هنا كلمة مرور التطبيق المكونة من 16 حرف الخاصة بحسابك

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

# نظام حفظ الجلسة (تسجيل الدخول مرة واحدة فقط للأبد على الجهاز)
SESSION_FILE = "user_saved_session.txt"

if "logged_in" not in st.session_state:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            saved_email = f.read().strip()
            if saved_email and "@gmail.com" in saved_email:
                st.session_state.logged_in = True
                st.session_state.user_email = saved_email
            else:
                st.session_state.logged_in = False
                st.session_state.user_email = ""
    else:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

if "verification_code" not in st.session_state:
    st.session_state.verification_code = None
if "pending_email" not in st.session_state:
    st.session_state.pending_email = ""
if "step" not in st.session_state:
    st.session_state.step = "register"

# ==========================================
# دالة إرسال رسالة الترحيب والأربع أرقام للبريد
# ==========================================
def send_welcome_and_code_email(receiver_email, code):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "مرحباً بك في تطبيق ميمو - رمز التحقق"
        
        # رسالة ترحيب مدمجة مع الأربع أرقام
        body = f"أهلاً بك في تطبيق ميمو الذكي! نحن سعداء انضمامك إلينا.\n\nرمز التحقق الخاص بك هو:\n{code}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

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

# ==========================================
# 2. شاشة تسجيل الدخول المتكاملة (مرة واحدة فقط)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1>🤖 مرحباً بك في ميمو الذكي</h1>
                <p style="color: gray;">تسجيل الدخول بالبريد وكلمة المرور (لمرة واحدة فقط)</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.step == "register":
            user_input_email = st.text_input("أدخل بريدك الإلكتروني (Gmail):", placeholder="example@gmail.com")
            user_password = st.text_input("أدخل كلمة المرور:", type="password", placeholder="أدخل كلمة مرور قوية")
            
            if st.button("إرسال رمز التحقق إلى البريد", use_container_width=True):
                if user_input_email and "@gmail.com" in user_input_email and len(user_password) >= 6:
                    code = str(random.randint(1000, 9999))
                    st.session_state.verification_code = code
                    st.session_state.pending_email = user_input_email
                    
                    # إرسال رسالة الترحيب والكود للإيميل
                    sent_success = send_welcome_and_code_email(user_input_email, code)
                    
                    if sent_success:
                        st.session_state.step = "verify"
                        st.success("تم إرسال رسالة الترحيب ورمز التحقق إلى بريدك الإلكتروني بنجاح!")
                        st.rerun()
                    else:
                        st.error("فشل إرسال البريد الإلكتروني، تأكد من إدخال كلمة مرور التطبيق (App Password) بشكل صحيح في الكود.")
                else:
                    st.error("الرجاء إدخال بريد جوجل صحيح وكلمة مرور لا تقل عن 6 أحرف.")
                    
        elif st.session_state.step == "verify":
            st.info(f"تم إرسال رسالة الترحيب والرمز المكون من 4 أرقام إلى: **{st.session_state.pending_email}**")
            
            entered_code = st.text_input("أدخل الأربع أرقام الموجودة في بريدك:", max_chars=4)
            
            if st.button("تأكيد الدخول النهائي", use_container_width=True):
                if entered_code == st.session_state.verification_code:
                    st.session_state.logged_in = True
                    st.session_state.user_email = st.session_state.pending_email
                    
                    # حفظ الجلسة ليدخل مرة واحدة للأبد
                    with open(SESSION_FILE, "w", encoding="utf-8") as f:
                        f.write(st.session_state.user_email)
                    
                    # إرسال إشعار تليجرام فوري بتسجيل دخول المستخدم بالبريد
                    send_telegram_notification(st.session_state.user_email, f"تم تسجيل دخول المستخدم بنجاح بالبريد: {st.session_state.user_email}")
                    
                    st.success("تم تسجيل الدخول بنجاح ولن يطلب منك مرة أخرى عند فتح التطبيق!")
                    st.rerun()
                else:
                    st.error("رمز التحقق غير صحيح، حاول مرة أخرى.")
    
    st.stop()

# ==========================================
# 3. واجهة التطبيق الرئيسية (بعد تسجيل الدخول)
# ==========================================
st.sidebar.title("🤖 ميمو AI - InnovaSoft")
st.sidebar.success(f"مرحباً: {st.session_state.user_email}")

if st.sidebar.button("تسجيل الخروج تماماً"):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.step = "register"
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "💬 الشات الصوتي الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "📊 لوحة تحكم الأدمن (سجل الأبحاث)"
]
app_mode = st.sidebar.radio("اختر القسم:", menu_options)

if app_mode == "💬 الشات الصوتي الذكي":
    st.title("💬 ميمو - الشات الصوتي الذكي")
    st.write(f"أهلاً بك يا {st.session_state.user_email}، اسأل عن أي شيء وسأرد عليك فوراً!")
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك أو بحثك هنا..."):
        send_telegram_notification(st.session_state.user_email, f"البحث عن: {user_prompt}")
        
        if "طورك" in user_prompt or "صنعك" in user_prompt or "من أنت" in user_prompt or "صاحب الشركة" in user_prompt:
            bot_reply = "Mohamed Adel"
        else:
            try:
                response = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": user_prompt}])
                bot_reply = str(response)
            except Exception as e:
                bot_reply = f"عذراً حدث خطأ: {e}"

        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة التي تريد توليدها:")
    if st.button("توليد الصورة"):
        if image_prompt:
            send_telegram_notification(st.session_state.user_email, f"البحث وتوليد صورة عن: {image_prompt}")
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(image_prompt)}?width=1024&height=1024&nologo=true", caption=image_prompt)

elif app_mode == "📊 لوحة تحكم الأدمن (سجل الأبحاث)":
    st.title("📊 لوحة تحكم الأدمن - السجلات")
    if os.path.exists("search_logs.txt"):
        with open("search_logs.txt", "r", encoding="utf-8") as f:
            st.code(f.read(), language="text")
    else:
        st.info("لا توجد سجلات بحث حتى الآن.")
