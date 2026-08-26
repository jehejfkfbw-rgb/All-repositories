import io
import json
import os
import sqlite3
from datetime import datetime, timedelta
import streamlit as st
from gtts import gTTS
from huggingface_hub import InferenceClient
from google import genai

# ==========================================
# ⚙️ 1. إعدادات الصفحة وقاعدة البيانات الدائمة
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

# إنشاء وتجهيز قاعدة البيانات لحفظ المستخدمين والمحادثات تلقائياً
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # جدول المستخدمين والجلسات
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY, 
                    vip_activated INTEGER DEFAULT 0, 
                    active_code TEXT DEFAULT ''
                )''')
    # جدول المحادثات الدائمة
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

# تهيئة Gemini API عبر المكتبة الحديثة (google-genai)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

@st.cache_resource
def get_gemini_client(api_key):
    if api_key:
        return genai.Client(api_key=api_key)
    return None

gemini_client = get_gemini_client(GEMINI_API_KEY)


# ==========================================
# 🔊 2. محرك تحويل النص إلى صوت (gTTS)
# ==========================================
def text_to_audio_bytes(text):
    try:
        clean_text = (
            text.replace("*", "")
            .replace("#", "")
            .replace("`", "")
            .replace("- ", "")
        )
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
# 🔑 3. نظام إدارة الأكواد وقاعدة البيانات
# ==========================================
def load_vip_codes():
    if not os.path.exists(CODES_FILE):
        now = datetime.now()
        default_codes = {
            "NOVA2026": {
                "expiry": (now + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "days": 30,
            },
        }
        save_vip_codes(default_codes)
        return default_codes
    try:
        with open(CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_vip_codes(codes_dict):
    with open(CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(codes_dict, f, ensure_ascii=False, indent=4)

def add_vip_code(code_name, days=30):
    codes = load_vip_codes()
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    codes[code_name.strip()] = {"expiry": expiry_date, "days": days}
    save_vip_codes(codes)

def delete_vip_code(code_name):
    codes = load_vip_codes()
    if code_name in codes:
        del codes[code_name]
        save_vip_codes(codes)

def validate_and_check_expiry(code_name):
    codes = load_vip_codes()
    if code_name not in codes:
        return False, "❌ الكود غير صحيح."

    expiry_str = codes[code_name]["expiry"]
    expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

    if datetime.now() > expiry_dt:
        return False, "⏳ انتهت مدة صلاحية اشتراك VIP."

    return True, "🎉 اشتراك VIP يعمل بنجاح."

# دواع التعامل مع قاعدة البيانات لثبات الجلسات والمحادثات
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
    c.execute("SELECT role, content FROM chat_history WHERE email = ? ORDER BY id ASC", (email,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]


# ==========================================
# 🌐 4. السيرفر المجاني و سيرفر VIP
# ==========================================
def ask_local_server(prompt):
    try:
        client = InferenceClient("Qwen/Qwen2.5-Coder-32B-Instruct")
        messages = [
            {"role": "system", "content": "أنت المساعد الذكي المجاني لمنصة نوفا (Nova AI Studio)."},
            {"role": "user", "content": prompt},
        ]
        response = client.chat_completion(messages=messages, max_tokens=600, temperature=0.7)
        return response.choices[0].message.content
    except Exception:
        return "🤖 **السيرفر المجاني:** تعذر الاتصال بالمحرك المجاني مؤقتاً."

def ask_vip_server(prompt):
    if not gemini_client:
        return "⚠️ **تنبيه VIP:** لم يتم إضافة GEMINI_API_KEY في secrets المنصة بعد."

    sys_p = "أنت مساعد VIP ذكي وفائق القدرات لمنصة Nova AI Studio. المطور هو محمد عادل لشركة Kivo."
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"system_instruction": sys_p}
        )
        if response and response.text:
            return response.text
        return "⚡ **خطأ VIP:** لم يتم استلام رد من السيرفر."
    except Exception as e:
        return f"⚡ **خطأ VIP:** تعذر الاتصال بسيرفر Gemini ({e})."


# ==========================================
# 🚀 5. إدارة تسجيل الدخول والواجهة
# ==========================================
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# تسجيل الدخول
if not st.session_state["user_email"]:
    st.title("⚡ منصة Nova AI Studio 2026")
    email_input = st.text_input("البريد الإلكتروني:")
    passw_input = st.text_input("كلمة السر:", type="password")
    
    if st.button("تسجيل الدخول"):
        if email_input and passw_input:
            email_clean = email_input.strip().lower()
            user_data = db_get_user(email_clean)
            
            if not user_data:
                db_save_user(email_clean, 0, '')
            
            st.session_state["user_email"] = email_clean
            st.rerun()
else:
    user_email = st.session_state["user_email"]
    user_db = db_get_user(user_email)
    
    vip_status = bool(user_db[1])
    active_code = user_db[2]
    is_exec = (user_email == EXECUTIVE_EMAIL.lower())

    # التحقق التلقائي من صلاحية الكود المخزن
    if vip_status:
        ok, msg = validate_and_check_expiry(active_code)
        if not ok:
            vip_status = False
            active_code = ""
            db_save_user(user_email, 0, "")
            st.error(f"⚠️ {msg}")

    st.sidebar.title("☰ لوحة التحكم")

    # زر تسجيل الخروج إذا أردت الانتقال لحساب آخر
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state["user_email"] = None
        st.rerun()

    # لوحة تحكم المطور
    if is_exec:
        st.sidebar.success("👑 مرحباً بك يا مطور المنصة")
        st.sidebar.subheader("🛠️ إدارة الاشتراكات للأكواد")
        c_name = st.sidebar.text_input("كود VIP جديد:")
        c_days = st.sidebar.number_input("مدة الصلاحية (بالأيام):", min_value=1, value=30)
        if st.sidebar.button("➕ إنشاء الكود"):
            if c_name:
                add_vip_code(c_name, c_days)
                st.sidebar.success(f"تم إنشاء الكود `{c_name}`!")
                st.rerun()

        st.sidebar.markdown("**الأكواد المسجلة:**")
        all_c = load_vip_codes()
        for k, v in list(all_c.items()):
            c1, c2 = st.sidebar.columns([3, 1])
            c1.caption(f"🔑 `{k}` | ⏳ {v['expiry'][:10]}")
            if c2.button("❌", key=f"del_{k}"):
                delete_vip_code(k)
                st.rerun()

    # تفعيل حسابات VIP
    st.sidebar.divider()
    st.sidebar.subheader("💳 تفعيل حساب VIP")
    if not vip_status:
        st.sidebar.info(f"للاشتراك، قم بالتحويل إلى: `{ORANGE_CASH_NUMBER}`")
        v_code = st.sidebar.text_input("أدخل كود VIP الخاص بك:", type="password")
        if st.sidebar.button("⚡ تفعيل VIP"):
            ok, msg = validate_and_check_expiry(v_code.strip())
            if ok:
                db_save_user(user_email, 1, v_code.strip())
                st.sidebar.success(msg)
                st.rerun()
            else:
                st.sidebar.error(msg)
    else:
        st.sidebar.success(f"👑 VIP مفعل بكود: `{active_code}`")

    # الواجهة الرئيسية وشات المحادثة المخزن
    st.title("⚡ Nova AI Studio 2026")

    # تحميل سجل المحادثة المخزن دائماً من SQLite
    messages = db_get_chat_history(user_email)
    if not messages:
        welcome_msg = "أهلاً بك في منصة Nova AI Studio! اكتب سؤالك هنا وسأجيبك فوراً."
        db_save_chat(user_email, "assistant", welcome_msg)
        messages = [{"role": "assistant", "content": welcome_msg}]

    # عرض كافة المحادثات المحفوظة
    for m in messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # استقبال السؤال وحفظه في القاعدة
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        db_save_chat(user_email, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير والتوليد الصوتي..."):
                if vip_status:
                    ans = ask_vip_server(prompt)
                else:
                    ans = ask_local_server(prompt)

                st.markdown(ans)
                db_save_chat(user_email, "assistant", ans)

                # توليد وتشغيل الصوت
                audio_fp = text_to_audio_bytes(ans)
                if audio_fp:
                    st.audio(audio_fp, format="audio/mp3")
