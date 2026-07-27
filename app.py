import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from datetime import datetime
import pytz
import requests
import random
import os

# ==========================================
# 1. إعدادات التطبيق وتليجرام والواتساب
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

TELEGRAM_BOT_TOKEN = "8394900129:AAENOZw1Zz0SNImSZB97ZKSMXUMudQRePg"     
TELEGRAM_CHAT_ID = "8672781771"          

# الرقم الأساسي للمدير (Admin)
ADMIN_PHONE = "01213783090"

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

# نظام حفظ الجلسة
SESSION_FILE = "user_saved_phone_session.txt"

if "logged_in" not in st.session_state:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            saved_data = f.read().strip()
            if saved_data:
                st.session_state.logged_in = True
                st.session_state.user_phone = saved_data
            else:
                st.session_state.logged_in = False
                st.session_state.user_phone = ""
    else:
        st.session_state.logged_in = False
        st.session_state.user_phone = ""

if "whatsapp_code" not in st.session_state:
    st.session_state.whatsapp_code = None
if "pending_phone" not in st.session_state:
    st.session_state.pending_phone = ""
if "step" not in st.session_state:
    st.session_state.step = "phone_input"

# دالة إرسال كود التحقق عبر الواتساب
def send_whatsapp_code(phone, code):
    try:
        clean_phone = phone.strip().replace("+", "")
        message = f"أهلاً بك في تطبيق ميمو الذكي! رمز التحقق الخاص بك هو: {code}"
        encoded_message = urllib.parse.quote(message)
        api_url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_message}&apikey=YOUR_APIKEY"
        requests.get(api_url, timeout=10)
        return True
    except Exception as e:
        print(f"WhatsApp Error: {e}")
        return False

# دالة إرسال إشعار تليجرام مدعومة بـ utf-8
def send_telegram_notification(phone, action_text):
    current_time = datetime.now(pytz.timezone('Africa/Cairo')).strftime('%Y-%m-%d %I:%M:%S %p')
    message = f"🚨 إشعار من تطبيق ميمو!\n\n📱 الهاتف: {phone}\n🔍 التفاصيل: {action_text}\n⏰ الوقت: {current_time}"
    
    try:
        log_entry = f"[{current_time}] | Phone: {phone} | Action: {action_text}\n"
        with open("search_logs.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        pass
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram Error: {e}")

# ==========================================
# 2. شاشة تسجيل الدخول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1>🤖 تسجيل الدخول لتطبيق ميمو</h1>
                <p style="color: gray;">أدخل رقم هاتفك للمتابعة</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.step == "phone_input":
            user_phone = st.text_input("أدخل رقم الهاتف:", placeholder="01213783090")
            
            if st.button("متابعة", use_container_width=True):
                if user_phone:
                    clean_input = user_phone.strip()
                    if clean_input == ADMIN_PHONE:
                        # دخول مباشر وفوري للمدير بدون كود
                        st.session_state.logged_in = True
                        st.session_state.user_phone = ADMIN_PHONE
                        with open(SESSION_FILE, "w", encoding="utf-8") as f:
                            f.write(ADMIN_PHONE)
                        send_telegram_notification(ADMIN_PHONE, "دخول المدير (Admin) مباشرة بنجاح.")
                        st.success("أهلاً بك يا فنان (المدير)! جارٍ فتح التطبيق...")
                        st.rerun()
                    else:
                        # أي رقم تاني يبعت له كود تحقق
                        code = str(random.randint(1000, 9999))
                        st.session_state.whatsapp_code = code
                        st.session_state.pending_phone = clean_input
                        send_whatsapp_code(clean_input, code)
                        st.session_state.step = "verify_whatsapp"
                        st.success(f"تم إرسال كود التحقق! (رمز التجربة: {code})")
                        st.rerun()
                else:
                    st.error("الرجاء إدخال رقم الهاتف.")

        elif st.session_state.step == "verify_whatsapp":
            st.info(f"الرقم قيد التحقق: **{st.session_state.pending_phone}**")
            entered_code = st.text_input("أدخل رمز التحقق (4 أرقام):", max_chars=4)
            
            if st.button("تأكيد الدخول", use_container_width=True):
                if entered_code == st.session_state.whatsapp_code:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = st.session_state.pending_phone
                    with open(SESSION_FILE, "w", encoding="utf-8") as f:
                        f.write(st.session_state.user_phone)
                    send_telegram_notification(st.session_state.user_phone, "تسجيل دخول مستخدم جديد عبر الكود بنجاح.")
                    st.success("تم التحقق بنجاح! جارٍ فتح التطبيق...")
                    st.rerun()
                else:
                    st.error("رمز التحقق غير صحيح.")
    st.stop()

# ==========================================
# 3. واجهة التطبيق الرئيسية
# ==========================================
st.sidebar.title("🤖 ميمو AI - InnovaSoft")
role_text = "مدير النظام (Admin)" if st.session_state.user_phone == ADMIN_PHONE else "مستخدم مسجل"
st.sidebar.success(f"الهاتف: {st.session_state.user_phone}\nالصلاحية: {role_text}")

if st.sidebar.button("تسجيل الخروج تماماً"):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    st.session_state.logged_in = False
    st.session_state.user_phone = ""
    st.session_state.step = "phone_input"
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "💬 الشات الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "📊 لوحة تحكم الأدمن (سجل الأبحاث)"
]
app_mode = st.sidebar.radio("اختر القسم:", menu_options)

if app_mode == "💬 الشات الذكي":
    st.title("💬 ميمو - الشات الذكي السريع")
    st.write("أهلاً بك، اسأل عن أي شيء وسأرد عليك فوراً!")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "أهلاً يا فنان! أنا جاهز، اكتب سؤالك وهيجيلك الرد في ثانية."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك أو بحثك هنا..."):
        send_telegram_notification(st.session_state.user_phone, f"البحث عن: {user_prompt}")
        
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("ميمو بيكتب الرد..."):
                try:
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    bot_reply = str(response)
                except Exception as e:
                    bot_reply = f"عذراً حدث خطأ: {e}"
                
                st.markdown(bot_reply)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة التي تريد توليدها:")
    if st.button("توليد الصورة"):
        if image_prompt:
            send_telegram_notification(st.session_state.user_phone, f"البحث وتوليد صورة عن: {image_prompt}")
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(image_prompt)}?width=1024&height=1024&nologo=true", caption=image_prompt)

elif app_mode == "📊 لوحة تحكم الأدمن (سجل الأبحاث)":
    st.title("📊 لوحة تحكم الأدمن - السجلات")
    if os.path.exists("search_logs.txt"):
        with open("search_logs.txt", "r", encoding="utf-8") as f:
            st.code(f.read(), language="text")
    else:
        st.info("لا توجد سجلات بحث حتى الآن.")
