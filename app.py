import io
import json
import os
import sqlite3
from datetime import datetime, timedelta
import streamlit as st
from gtts import gTTS
from google import genai

# ==========================================
# ⚙️ 1. إعدادات الصفحة والمفتاح
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio 2026", 
    page_icon="⚡", 
    layout="wide"
)

ORANGE_CASH_NUMBER = "01213783090"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
CODES_FILE = "vip_codes.json"
DB_FILE = "nova_database.db"

# المفتاح الخاص بك
GEMINI_API_KEY = "AQ.Ab8RN6LKT2joUyWc5npc7lCZcQ26uhSPsw_nxEHyeNFQuG3FiA"

@st.cache_resource
def get_gemini_client(api_key):
    if api_key:
        try:
            return genai.Client(api_key=api_key)
        except Exception:
            return None
    return None

gemini_client = get_gemini_client(GEMINI_API_KEY)

# ==========================================
# 💾 2. قاعدة البيانات المحفوظة (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY, 
                    vip_activated INTEGER DEFAULT 0, 
                    active_code TEXT DEFAULT ''
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    role TEXT,
                    content TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 🔊 3. محرك تحويل النص إلى صوت (gTTS)
# ==========================================
def text_to_audio_bytes(text):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("`", "").replace("- ", "")
        if not clean_text.strip():
            return None
        tts = gTTS(text=clean_text, lang="ar")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None

# ==========================================
# 🔑 4. نظام الأكواد والاشتراكات
# ==========================================
def load_vip_codes():
    if not os.path.exists(CODES_FILE):
        default_codes = {"NOVA2026": {"expiry": "2030-01-01 00:00:00", "days": 365}}
        with open(CODES_FILE, "w", encoding="utf-8") as f:
            json.dump(default_codes, f, ensure_ascii=False, indent=4)
        return default_codes
    try:
        with open(CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def validate_code(code_name):
    codes = load_vip_codes()
    if code_name not in codes:
        return False, "❌ الكود غير صحيح."
    return True, "🎉 تم تفعيل اشتراك VIP بنجاح!"

# تعاملات قاعدة البيانات لثبات الجلسة
def db_get_user(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT email, vip_activated, active_code FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def db_save_user(email, vip_activated=0, active_code=''):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (email, vip_activated, active_code) VALUES (?, ?, ?)",
              (email, vip_activated, active_code))
    conn.commit()
    conn.close()

def db_save_chat(email, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (email, role, content) VALUES (?, ?, ?)", (email, role, content))
    conn.commit()
    conn.close()

def db_get_chat_history(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history WHERE email = ?", (email,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

# ==========================================
# 🤖 5. محركات الرد الذكي
# ==========================================
def ask_free_server(prompt):
    now = datetime.now()
    p = prompt.strip().lower()
    
    if any(x in p for x in ["مرحبا", "أهلا", "السلام عليكم", "ازيك"]):
        return "أهلاً بك في منصة Nova AI Studio! كيف يمكنني مساعدتك اليوم؟"
    elif any(x in p for x in ["الساعه", "الساعة", "التاريخ", "اليوم", "الوقت"]):
        days_ar = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        return f"📅 اليوم: {days_ar[now.weekday()]}\n📆 التاريخ: {now.strftime('%Y-%m-%d')}\n⏰ الوقت: {now.strftime('%I:%M:%S %p')}"
    else:
        return f"🤖 **السيرفر المجاني:** تم استلام سؤالك: '{prompt}'. لتلقي الإجابات الكاملة بالذكاء الاصطناعي، قم بتفعيل كود VIP."

def ask_vip_server(prompt):
    if not gemini_client:
        return "⚠️ **تنبيه VIP:** يرجى التأكد من استخراج مفتاح Gemini الصحيح (يبدأ بـ AIzaSy) ليعمل السيرفر."
    
    sys_p = "أنت مساعد VIP ذكي وفائق القدرات لمنصة Nova AI Studio. المطور هو محمد عادل لشركة Kivo."
    try:
        response = gemini_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={"system_instruction": sys_p}
        )
        return response.text if response and response.text else "لم يتوفر رد من السيرفر."
    except Exception as e:
        return f"⚡ **خطأ في السيرفر:** {e}\n(تأكد من استخدام مفتاح Gemini يبدأ بـ AIzaSy)"

# ==========================================
# 🚀 6. الواجهة وتجربة المستخدم
# ==========================================
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

if not st.session_state["user_email"]:
    st.title("⚡ منصة Nova AI Studio 2026")
    email_input = st.text_input("البريد الإلكتروني:")
    passw_input = st.text_input("كلمة السر:", type="password")
    
    if st.button("تسجيل الدخول"):
        if email_input and passw_input:
            email_clean = email_input.strip().lower()
            if not db_get_user(email_clean):
                db_save_user(email_clean, 0, '')
            st.session_state["user_email"] = email_clean
            st.rerun()
else:
    user_email = st.session_state["user_email"]
    user_db = db_get_user(user_email)
    vip_status = bool(user_db[1])
    active_code = user_db[2]

    st.sidebar.title("☰ لوحة التحكم")
    st.sidebar.caption(f"المستخدم: {user_email}")
    
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state["user_email"] = None
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("💳 تفعيل حساب VIP")
    if not vip_status:
        st.sidebar.info(f"للاشتراك، قم بالتحويل إلى: `{ORANGE_CASH_NUMBER}`")
        v_code = st.sidebar.text_input("أدخل كود VIP الخاص بك:", type="password")
        if st.sidebar.button("⚡ تفعيل VIP"):
            ok, msg = validate_code(v_code.strip())
            if ok:
                db_save_user(user_email, 1, v_code.strip())
                st.sidebar.success(msg)
                st.rerun()
            else:
                st.sidebar.error(msg)
    else:
        st.sidebar.success(f"👑 VIP مفعل بكود: `{active_code}`")

    # المحادثة الرئيسية
    st.title("⚡ Nova AI Studio 2026")

    messages = db_get_chat_history(user_email)
    if not messages:
        welcome_msg = "أهلاً بك في منصة Nova AI Studio! اكتب سؤالك هنا وسأجيبك فوراً."
        db_save_chat(user_email, "assistant", welcome_msg)
        messages = [{"role": "assistant", "content": welcome_msg}]

    for m in messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        db_save_chat(user_email, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                if vip_status:
                    ans = ask_vip_server(prompt)
                else:
                    ans = ask_free_server(prompt)

                st.markdown(ans)
                db_save_chat(user_email, "assistant", ans)

                audio_fp = text_to_audio_bytes(ans)
                if audio_fp:
                    st.audio(audio_fp, format="audio/mp3")
