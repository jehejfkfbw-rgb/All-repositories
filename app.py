import sqlite3
import random
import datetime
import urllib.parse
import requests
import streamlit as st

# =========================================================
# 1. إعدادات الصفحة والتصميم
# =========================================================
st.set_page_config(
    page_title="تسجيل طلاب المنصة",
    page_icon="🎓",
    layout="centered"
)

# إضافة تنسيق بسيط لدعم اللغة العربية والاتجاه من اليمين للشمال
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-baseweb="input"] { text-align: right; }
    .stButton>button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; border-radius: 8px; height: 50px; }
    .code-card { background-color: #f0f8ff; border: 2px dashed #1e90ff; padding: 20px; border-radius: 12px; text-align: center; margin-top: 15px; }
    .code-title { color: #333; font-size: 18px; margin-bottom: 5px; }
    .code-val { color: #1e90ff; font-size: 32px; font-weight: bold; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. إدارة قاعدة البيانات وتوليد كود الطالب
# =========================================================
DB_NAME = "students_system.db"

def init_db():
    """إنشاء جدول الطلاب إذا لم يكن موجوداً"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registered_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_code TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                governorate TEXT NOT NULL,
                course_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def generate_unique_student_code():
    """توليد كود طالب فريد ومميز مثل STU-2026-8492"""
    year = datetime.datetime.now().year
    while True:
        random_num = random.randint(1000, 9999)
        code = f"STU-{year}-{random_num}"
        
        # التأكد من عدم تكرار الكود في قاعدة البيانات
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM registered_students WHERE student_code = ?", (code,))
            if not cursor.fetchone():
                return code

def save_student(student_code, name, phone, governorate, course):
    """حفظ بيانات الطالب في السيستم"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO registered_students (student_code, full_name, phone, governorate, course_name)
                VALUES (?, ?, ?, ?, ?)
            """, (student_code, name, phone, governorate, course))
            conn.commit()
            return True, "تم الحفظ بنجاح"
    except Exception as e:
        return False, str(e)

# =========================================================
# 3. نظام إرسال إشعارات الواتساب للمطور/الإدارة
# =========================================================
def send_admin_whatsapp_notification(student_code, name, phone, governorate, course):
    """
    إرسال رسالة واتساب للإدارة عند تسجيل طالب جديد.
    تستخدم خدمة CallMeBot المجانية للتنبيهات.
    """
    # احصل على رقمك و APIKEY من st.secrets أو ضعهم هنا للتجربة
    admin_phone = st.secrets.get("ADMIN_WHATSAPP_PHONE", "") # مثال: "2010xxxxxxx"
    apikey = st.secrets.get("CALLMEBOT_APIKEY", "")

    if not admin_phone or not apikey:
        # إذا لم يتم ضبط التنسيق، يتم تخطي الإرسال دون إيقاف البرنامج
        return False

    # رابط الواتساب المباشر للرد على الطالب بضغطة واحدة
    clean_phone = phone.replace("+", "").replace(" ", "")
    if not clean_phone.startswith("2"): # إضافة كود مصر مثلاً لو لم يكن موجوداً
        clean_phone = "2" + clean_phone
    wa_reply_link = f"https://wa.me/{clean_phone}"

    # نص الرسالة التي ستصلك على الواتساب
    message_text = (
        f"🚨 *تسجيل طالب جديد في المنصة!*\n\n"
        f"🆔 *كود الطالب:* `{student_code}`\n"
        f"👤 *الاسم للشهادة:* {name}\n"
        f"📱 *رقم الواتساب:* {phone}\n"
        f"📍 *المحافظة:* {governorate}\n"
        f"📚 *الكورس المطلوب:* {course}\n\n"
        f"💬 *للرد المباشر على الطالب انقر هنا:* {wa_reply_link}"
    )

    encoded_msg = urllib.parse.quote(message_text)
    url = f"https://api.callmebot.com/whatsapp.php?phone={admin_phone}&text={encoded_msg}&apikey={apikey}"
    
    try:
        res = requests.get(url, timeout=10)
        return res.ok
    except Exception:
        return False

# =========================================================
# 4. واجهة المستخدم (Streamlit UI)
# =========================================================
init_db()

st.title("🎓 استمارة تسجيل طالب جديد")
st.write("برجاء إدخال البيانات بدقة، حيث سيتمد استخدام الاسم في **شهادة اكتمال الدورة**.")

with st.form("student_registration_form"):
    full_name = st.text_input("الاسم الثلاثي أو الرباعي (كما يظهر بالشهادة):", placeholder="مثال: أحمد محمد علي محمود")
    phone_number = st.text_input("رقم الهاتف / الواتساب المفعل:", placeholder="010xxxxxxx")
    
    col1, col2 = st.columns(2)
    with col1:
        governorate = st.selectbox("المحافظة:", [
            "القاهرة", "الجيزة", "الإسكندرية", "الدقهلية", "الشرقية", 
            "المنوفية", "الغربية", "القليوبية", "البحيرة", "كفر الشيخ", 
            "دمياط", "بورسعيد", "الإسماعيلية", "السويس", "أخرى"
        ])
    with col2:
        course_name = st.selectbox("الكورس المراد الاشتراك فيه:", [
            "كورس برمجة المواقع (Web Dev)",
            "كورس بايثون وتطوير الذكاء الاصطناعي",
            "كورس تصميم واجهات المستخدم (UI/UX)",
            "كورس الأساسيات والبرمجة للمبتدئين"
        ])

    submit_btn = st.form_submit_button("تسجيل والحصول على كود الطالب 🚀")

if submit_btn:
    if not full_name.strip() or not phone_number.strip():
        st.error("⚠️ برجاء ملء كافة البيانات المطلوبة قبل إرسال الاستمارة.")
    elif len(phone_number.strip()) < 10:
        st.error("⚠️ برجاء كتابة رقم هاتف صحيح.")
    else:
        # 1. توليد كود الطالب
        new_student_code = generate_unique_student_code()
        
        # 2. حفظ الطالب في قاعدة البيانات
        success, msg = save_student(new_student_code, full_name, phone_number, governorate, course_name)
        
        if success:
            st.balloons()
            st.success("🎉 تم تسجيل بياناتك بنجاح في المنصة!")
            
            # عرض بطاقة كود الطالب بشكل واضح
            st.markdown(f"""
                <div class="code-card">
                    <div class="code-title">📌 كود الطالب الخاص بك (احتفظ به):</div>
                    <div class="code-val">{new_student_code}</div>
                    <p style="color: #666; font-size: 13px; margin-top: 8px;">
                        استخدم هذا الكود عند التواصل معنا وفي طباعة شهادة التخرج لاحقاً.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # 3. إرسال إشعار الواتساب للآدمن
            sent = send_admin_whatsapp_notification(new_student_code, full_name, phone_number, governorate, course_name)
            if sent:
                st.info("📲 تم إرسال إشعار بالتسجيل لخدمة العملاء وسنتواصل معك عبر الواتساب قريباً.")
            else:
                st.info("✅ تم تسجيل بياناتك بالسيستم بنجاح.")
        else:
            st.error(f"حدث خطأ أثناء التسجيل: {msg}")

# =========================================================
# 5. عرض سريع للبيانات المسجلة (لوحة الإدارة المصغرة)
# =========================================================
st.divider()
with st.expander("🔍 عرض السجلات المسجلة (خاص بالإدارة)"):
    with sqlite3.connect(DB_NAME) as conn:
        import pandas as pd
        df = pd.read_sql_query("SELECT id, student_code, full_name, phone, governorate, course_name, created_at FROM registered_students ORDER BY id DESC", conn)
        st.dataframe(df, use_container_width=True)
```eof

### مميزات هذا الكود:
1. **توليد تلقائي لكود الطالب (`Student Code`):** يولد كوداً منسقاً وغير مكرر مثل (`STU-2026-4891`) ويُعرض للطالب في بطاقة بارزة ليحتفظ به.
2. **إشعار الواتساب الفوري:** يرسل لك رسالة فورية على الواتساب عند تسجيل أي طالب تحتوي على:
   - بيانات الطالب كاملة (الاسم للشهادة، الرقم، الكورس، المحافظة).
   - كود الطالب الخاص به.
   - **رابط مباشر بضغطة واحدة (`wa.me`)** لفتح الشات مع الطالب فوراً والرد عليه في الواتساب.
3. **حفظ في قاعدة البيانات:** البيانات محفوظة في جدول `registered_students` لإصدار الشهادات منه لاحقاً.

بعد اعتماد هذه الخطوة وتجربتها، الخطوة التالية مباشرةً سنقوم بربط هذا الكود بصفحة الاشتراك في الكورسات والبث المباشر.
