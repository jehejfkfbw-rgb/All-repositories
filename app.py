import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from gtts import gTTS
import os
from datetime import datetime
import pytz
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات تطبيق ميمو الذكي والتليجرام
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

# 🔴 تم وضع التوكن والـ Chat ID الخاص بك هنا
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

ADMIN_EMAIL = "mohamed@gmail.com"  # إيميلك الشخصي

# ==========================================
# دالة إرسال إشعار فوري على تليجرام
# ==========================================
def send_telegram_notification(email, query_text):
    current_time = datetime.now(pytz.timezone('Africa/Cairo')).strftime('%Y-%m-%d %I:%M:%S %p')
    message = f"🚨 بحث أو سؤال جديد في تطبيق ميمو!\n\n👤 المستخدم: {email}\n🔍 النص: {query_text}\n⏰ الوقت: {current_time}"
    
    # حفظ محلياً أيضاً كنسخة احتياطية
    log_entry = f"[{current_time}] | User: {email} | Search: {query_text}\n"
    with open("search_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    # إرسال رسالة تليجرام فورية لك
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
# 2. شاشة تسجيل الدخول بحساب جوجل
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1>🤖 مرحباً بك في ميمو الذكي</h1>
                <p style="color: gray;">يرجى تسجيل الدخول بحساب جوجل للوصول إلى التطبيق</p>
            </div>
        """, unsafe_allow_html=True)
        
        user_input_email = st.text_input("أدخل بريد جوجل (Gmail):", placeholder="example@gmail.com")
        
        if st.button("تسجيل الدخول باستخدام جوجل", use_container_width=True):
            if user_input_email and "@gmail.com" in user_input_email:
                st.session_state.logged_in = True
                st.session_state.user_email = user_input_email
                st.success("تم تسجيل الدخول بنجاح! جاري التوجيه...")
                st.rerun()
            else:
                st.error("الرجاء إدخال بريد جوجل صحيح يحتوي على @gmail.com")
    
    st.stop()

# ==========================================
# دوال المساعدة (الصوت والمواقيت)
# ==========================================
def text_to_speech(text, filename="memo_voice.mp3"):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("-", " ")
        tts = gTTS(text=clean_text, lang='ar', slow=False)
        tts.save(filename)
        return filename
    except:
        return None

def get_prayer_times(country):
    cities = {
        'مصر': 'Cairo', 'السعودية': 'Riyadh', 'الإمارات': 'Dubai',
        'الكويت': 'Kuwait', 'قطر': 'Doha', 'البحرين': 'Manama',
        'عمان': 'Muscat', 'الأردن': 'Amman', 'فلسطين': 'Jerusalem',
        'لبنان': 'Beirut', 'سوريا': 'Damascus', 'العراق': 'Baghdad',
        'اليمن': 'Sana a', 'السودان': 'Khartoum', 'ليبيا': 'Tripoli',
        'تونس': 'Tunis', 'الجزائر': 'Algiers', 'المغرب': 'Rabat',
        'موريتانيا': 'Nouakchott', 'أمريكا': 'New York'
    }
    city = cities.get(country, 'Cairo')
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=5"
        response = requests.get(url)
        data = response.json()
        if data['code'] == 200:
            return data['data']['timings']
    except:
        pass
    return None

# ==========================================
# 3. القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.title("🤖 ميمو AI - InnovaSoft")
st.sidebar.success(f"مرحباً: {st.session_state.user_email}")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.rerun()

st.sidebar.markdown("---")

menu_options = [
    "💬 الشات الصوتي الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "✏️ محرر الصور والفلاتر"
]

if st.session_state.user_email.strip().lower() == ADMIN_EMAIL.strip().lower():
    menu_options.append("📊 لوحة تحكم الأدمن (سجل الأبحاث)")

app_mode = st.sidebar.radio("اختر القسم:", menu_options)

st.sidebar.markdown("---")
st.sidebar.subheader("🕌 مواقيت الصلاة")
selected_country_sidebar = st.sidebar.selectbox("اختر الدولة:", [
    'مصر', 'السعودية', 'الإمارات', 'الكويت', 'قطر', 'البحرين', 'عمان', 
    'الأردن', 'فلسطين', 'لبنان', 'سوريا', 'العراق', 'اليمن', 'السودان', 
    'ليبيا', 'تونس', 'الجزائر', 'المغرب', 'موريتانيا', 'أمريكا'
])

# ==========================================
# 4. قسم الشات الصوتي الذكي (مع إرسال إشعار تليجرام)
# ==========================================
if app_mode == "💬 الشات الصوتي الذكي":
    st.title("💬 ميمو - الشات الصوتي الذكي")
    st.write(f"أهلاً بك يا {st.session_state.user_email}، اسأل عن أي شيء وسأرد عليك فوراً!")
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("🗑️ مسح الذاكرة وبدء محادثة جديدة"):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "audio" in message:
                st.audio(message["audio"], format="audio/mp3")

    if user_prompt := st.chat_input("اكتب سؤالك أو بحثك هنا..."):
        
        # 🚨 إرسال إشعار فوري إلى تليجرام لديك
        send_telegram_notification(st.session_state.user_email, user_prompt)

        # الرد بالإنجليزية بالاسم المطلوب عند السؤال عن صاحب الشركة أو صانع التطبيق
        if "طورك" in user_prompt or "صنعك" in user_prompt or "عملك" in user_prompt or "من أنت" in user_prompt or "انت مين" in user_prompt or "صاحب الشركة" in user_prompt or "مين صاحبك" in user_prompt or "company" in user_prompt.lower() or "who" in user_prompt.lower():
            bot_reply = "Mohamed Adel"
        elif "صلاة" in user_prompt or "أذان" in user_prompt or "مواقيت" in user_prompt:
            bot_reply = "مواقيت الصلاة متاحة في القائمة الجانبية حسب دولتك."
        else:
            with st.spinner("جاري التفكير وتوليد الصوت..."):
                try:
                    messages_list = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                    messages_list.append({"role": "user", "content": user_prompt})
                    response = g4f.ChatCompletion.create(model=g4f.models.default, messages=messages_list)
                    bot_reply = str(response)
                except Exception as e:
                    bot_reply = f"عذراً حدث خطأ: {e}"

        audio_filename = f"memo_voice_{len(st.session_state.chat_history)}.mp3"
        audio_path = text_to_speech(bot_reply, filename=audio_filename)

        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        assistant_message = {"role": "assistant", "content": bot_reply}
        if audio_path:
            assistant_message["audio"] = audio_path
        st.session_state.chat_history.append(assistant_message)

        with st.chat_message("user"):
            st.markdown(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            if audio_path:
                st.audio(audio_path, format="audio/mp3")

# ==========================================
# 5. قسم توليد الصور (مع إرسال إشعار تليجرام)
# ==========================================
elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة التي تريد البحث عنها وتوليدها:", placeholder="مثال: مدينة مستقبلية")

    if st.button("توليد الصورة"):
        if image_prompt:
            send_telegram_notification(st.session_state.user_email, f"Image Search: {image_prompt}")
            
            with st.spinner("جاري رسم الصورة..."):
                encoded_prompt = urllib.parse.quote(image_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                st.success("تم توليد الصورة بنجاح!")
                st.image(image_url, caption=image_prompt, use_column_width=True)
        else:
            st.warning("الرجاء كتابة وصف للصورة أولاً.")

# ==========================================
# 6. قسم محرر الصور
# ==========================================
elif app_mode == "✏️ محرر الصور والفلاتر":
    st.title("✏️ ميمو - محرر الصور")
    file = st.file_uploader("اختر صورة...", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="الصورة الأصلية", use_column_width=True)
        brightness = st.sidebar.slider("الإضاءة", 0.1, 3.0, 1.0)
        contrast = st.sidebar.slider("التباين", 0.1, 3.0, 1.0)
        edited = ImageEnhance.Brightness(img).enhance(brightness)
        edited = ImageEnhance.Contrast(edited).enhance(contrast)
        st.image(edited, caption="بعد التعديل", use_column_width=True)

# ==========================================
# 7. لوحة تحكم الأدمن
# ==========================================
elif app_mode == "📊 لوحة تحكم الأدمن (سجل الأبحاث)":
    st.title("📊 لوحة تحكم الأدمن - سجل عمليات البحث والأسئلة")
    st.write("هنا يمكنك متابعة كل كلمة بحث أو سؤال كتبه أي مستخدم دخل التطبيق:")
    st.markdown("---")

    if os.path.exists("search_logs.txt"):
        if st.button("🔄 تحديث السجل"):
            st.rerun()
            
        with open("search_logs.txt", "r", encoding="utf-8") as f:
            logs_data = f.readlines()
            
        if logs_data:
            st.download_button(
                label="📥 تحميل سجل الأبحاث كملف نصي",
                data="".join(logs_data),
                file_name="all_user_searches.txt",
                mime="text/plain"
            )
            st.markdown("---")
            for log in reversed(logs_data):
                st.code(log.strip(), language="text")
        else:
            st.info("لا توجد عمليات بحث مسجلة حتى الآن.")
    else:
        st.info("لم يتم تسجيل أي عمليات بحث بعد.")
