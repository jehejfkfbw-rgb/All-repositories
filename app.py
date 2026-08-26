import io
import sqlite3
import streamlit as st
from gtts import gTTS
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ==========================================
# ⚙️ 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio 2026", 
    page_icon="⚡", 
    layout="wide"
)

DB_FILE = "nova_database.db"

# ==========================================
# 🤖 2. تحميل نموذج الذكاء الاصطناعي محلياً بالمكتبة
# ==========================================
MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

@st.cache_resource
def load_local_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        torch_dtype="auto", 
        device_map="auto"
    )
    return tokenizer, model

# ==========================================
# 💾 3. قاعدة البيانات المحفوظة لثبات الجلسة
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY, 
                    vip_activated INTEGER DEFAULT 1, 
                    active_code TEXT DEFAULT 'LOCAL_FULL'
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

def db_get_user(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT email, vip_activated, active_code FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def db_save_user(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (email, vip_activated, active_code) VALUES (?, 1, 'LOCAL_FULL')", (email,))
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
# 🔊 4. محرك الصوت (gTTS)
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
# 🧠 5. توليد الإجابة محلياً من المكتبة
# ==========================================
def ask_local_ai(prompt):
    try:
        tokenizer, model = load_local_model()
        messages = [
            {"role": "system", "content": "أنت مساعد ذكي ومطور محلي لمنصة Nova AI Studio. المطور هو محمد عادل لشركة Kivo."},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            temperature=0.7
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
    except Exception as e:
        return f"⚡ **خطأ في النموذج المحلي:** {e}"

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
                db_save_user(email_clean)
            st.session_state["user_email"] = email_clean
            st.rerun()
else:
    user_email = st.session_state["user_email"]

    st.sidebar.title("☰ لوحة التحكم")
    st.sidebar.caption(f"المستخدم: {user_email}")
    st.sidebar.success("🟢 السيرفر المحلي يعمل بالمكتبة مجاناً")
    
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state["user_email"] = None
        st.rerun()

    st.title("⚡ Nova AI Studio 2026")

    messages = db_get_chat_history(user_email)
    if not messages:
        welcome_msg = "أهلاً بك في منصة Nova AI Studio! السيرفر يعمل الآن محلياً بالكامل عبر مكتبة الذكاء الاصطناعي."
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
            with st.spinner("جاري التفكير والتوليد عبر المكتبة المحلية..."):
                ans = ask_local_ai(prompt)

                st.markdown(ans)
                db_save_chat(user_email, "assistant", ans)

                audio_fp = text_to_audio_bytes(ans)
                if audio_fp:
                    st.audio(audio_fp, format="audio/mp3")
