from datetime import datetime, timedelta
import random
import string
import sqlite3
import urllib.parse
import pandas as pd
import requests
import streamlit as st

# =========================================================
# 1. إعدادات وتصميم الصفحة
# =========================================================
st.set_page_config(page_title="منصة نوفا التعليمية", page_icon="🌟", layout="centered")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-baseweb="input"] { text-align: right; }
    .stButton>button { width: 100%; background-color: #2e7d32; color: white; font-weight: bold; border-radius: 8px; height: 45px; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. إدارة قاعدة البيانات
# =========================================================
DB_NAME = "nova_platform.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pending_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_code TEXT UNIQUE,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                governorate TEXT NOT NULL,
                course_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP
            )
        """)
        conn.commit()

def generate_random_student_code():
    prefix = "NOVA"
    while True:
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        code = f"{prefix}-{random_chars}"
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM pending_students WHERE student_code = ?", (code,))
            if not cursor.fetchone():
                return code

def register_application(name, phone, governorate, course):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pending_students (full_name, phone, governorate, course_name)
                VALUES (?, ?, ?, ?)
            """, (name, phone, governorate, course))
            conn.commit()
            return True, "تم تقديم طلبك بنجاح!"
    except Exception as e:
        return False, str(e)

def approve_student_and_generate_code(student_id):
    student_code = generate_random_student_code()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pending_students 
            SET status = 'approved', student_code = ?, approved_at = ?
            WHERE id = ?
        """, (student_code, now_str, student_id))
        conn.commit()
    return student_code

# =========================================================
# 3. إرسال تنبيهات الواتساب
# =========================================================
def send_whatsapp_msg(target_phone, text):
    admin_phone = st.secrets.get("ADMIN_WHATSAPP_PHONE", target_phone)
    apikey = st.secrets.get("CALLMEBOT_APIKEY", "")

    if not apikey:
        return False

    clean_phone = target_phone.replace("+", "").replace(" ", "").strip()
    if not clean_phone.startswith("2"):
        clean_phone = "2" + clean_phone

    encoded_text = urllib.parse.quote(text)
    url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={apikey}"
    try:
        res = requests.get(url, timeout=10)
        return res.ok
    except Exception:
        return False

# =========================================================
# 4. الواجهة الرئيسية والتنقل
# =========================================================
init_db()

page = st.sidebar.radio("القائمة:", ["استمارة التقديم", "لوحة تحكم المطور"])

if page == "استمارة التقديم":
    st.title("🌟 منصة نوفا التعليمية")
    st.subheader("📝 طلب الالتحاق بالكورسات")
    st.info("قم بملء البيانات، وسيتم مراجعة طلبك وقبوله خلال 24 ساعة وإرسال كود الطالب الخاص بك عبر الواتساب.")

    with st.form("apply_form"):
        full_name = st.text_input("الاسم الرباعي:")
        phone = st.text_input("رقم الواتساب:", placeholder="010xxxxxxx")
        governorate = st.selectbox("المحافظة:", ["الدقهلية", "القاهرة", "الجيزة", "الإسكندرية", "أخرى"])
        course = st.selectbox("الكورس المطلوب:", ["كورس البرمجة والبايثون", "كورس تطوير المواقع", "كورس الذكاء الاصطناعي"])
        
        submit = st.form_submit_button("إرسال طلب التقديم 🚀")

    if submit:
        if not full_name.strip() or not phone.strip():
            st.error("⚠️ يرجى كتابة كافة البيانات.")
        else:
            ok, msg = register_application(full_name, phone, governorate, course)
            if ok:
                st.success("🎉 تم تقديم طلبك بنجاح! طلبك قيد المراجعة حالياً، وسنرسل لك كود الطالب على الواتساب فور التفعيل خلال 24 ساعة.")
                
                # إشعار سريع للمطور بوجود طلب جديد
                admin_phone = st.secrets.get("ADMIN_WHATSAPP_PHONE", "")
                if admin_phone:
                    send_whatsapp_msg(admin_phone, f"📥 طلب جديد مقدم في منصة نوفا من: {full_name} ({phone})")
            else:
                st.error(f"حدث خطأ: {msg}")

else:
    st.title("⚙️ لوحة إدارة منصة نوفا")
    admin_pass = st.text_input("كلمة سر المطور:", type="password")
    
    if admin_pass == st.secrets.get("ADMIN_PASSWORD", "2010"):
        st.success("مرحباً بك يا مطور المنصة 👋")
        
        with sqlite3.connect(DB_NAME) as conn:
            df_pending = pd.read_sql_query("SELECT * FROM pending_students WHERE status = 'pending'", conn)
            df_approved = pd.read_sql_query("SELECT * FROM pending_students WHERE status = 'approved'", conn)

        st.subheader("📌 الطلبات المنتظرة للقبول (خلال 24 ساعة)")
        if df_pending.empty:
            st.info("لا توجد طلبات معلقة حالياً.")
        else:
            for _, row in df_pending.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"👤 **{row['full_name']}** | 📱 {row['phone']} | 📚 {row['course_name']} ({row['created_at']})")
                with col2:
                    if st.button(f"قبول وإرسال الكود", key=f"app_{row['id']}"):
                        code = approve_student_and_generate_code(row['id'])
                        
                        # نص رسالة القبول للطالب
                        msg_to_student = (
                            f"🎉 *مبروك! تم قبولك في منصة نوفا التعليمية*\n\n"
                            f"👤 الطالب: {row['full_name']}\n"
                            f"📚 الكورس: {row['course_name']}\n"
                            f"🔑 *كود الطالب الخاص بك:* `{code}`\n\n"
                            f"احتفظ بهذا الكود للدخول للبث المباشر وإصدار الشهادة."
                        )
                        send_whatsapp_msg(row['phone'], msg_to_student)
                        st.success(f"تم قبول الطالب وتوليد الكود: {code}")
                        st.rerun()

        st.divider()
        st.subheader("✅ الطلاب المقبولين ومفعلين")
        st.dataframe(df_approved, use_container_width=True)
