import io
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
from gtts import gTTS
from PIL import Image
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة والجرافيك
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo Local DB 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 📲 2. البيانات الثابتة والإعدادات
# ==========================================
MY_PHONE = "201102464297"
ORANGE_CASH_NUMBER = "01213783090"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
DB_FILE = "nova_local_database.db"

# ==========================================
# 🗄️ 3. محرك قاعدة البيانات المحلية الضخمة (SQLite)
# ==========================================
def init_and_seed_db():
  """إنشاء وتعبئة قاعدة البيانات المحلية بجميع المعلومات الشاملة"""
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()

  c.execute("""
        CREATE TABLE IF NOT EXISTS local_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keyword TEXT,
            response TEXT
        )
    """)

  # التأكد من عدم تكرار التعبئة
  c.execute("SELECT COUNT(*) FROM local_knowledge")
  if c.fetchone()[0] == 0:
    seed_data = [
        # قسم المطور والشركة
        (
            "المطور والشركة",
            "من انت",
            (
                "أنا نظام Nova AI Studio الذكي والمطور بالكامل لشركة Kivo."
                " المطور التنفيذي والمسؤول الأول عن النظام هو محمد عادل."
            ),
        ),
        (
            "المطور والشركة",
            "من أنت",
            (
                "أنا نظام Nova AI Studio الذكي والمطور بالكامل لشركة Kivo."
                " المطور التنفيذي والمسؤول الأول عن النظام هو محمد عادل."
            ),
        ),
        (
            "المطور والشركة",
            "مين المطور",
            (
                "المطور التنفيذي للنظام هو الباشمهندس محمد عادل، وهو القائم"
                " على تطوير وتحديث كافة خوارزميات Nova تحت مظلة شركة Kivo."
            ),
        ),
        (
            "المطور والشركة",
            "محمد عادل",
            (
                "محمد عادل هو المطور التنفيذي والمؤسس لنظام Nova AI وشركة"
                " Kivo للحلول البرمجية والتقنية."
            ),
        ),
        (
            "المطور والشركة",
            "كيفو",
            (
                "شركة Kivo هي الشركة الناشئة المبتكرة لنظام Nova AI وتقدم"
                " حلول البرمجة والذكاء الاصطناعي وتطوير التطبيقات."
            ),
        ),
        (
            "المطور والشركة",
            "kivo",
            (
                "شركة Kivo هي الشركة الناشئة المبتكرة لنظام Nova AI وتقدم"
                " حلول البرمجة والذكاء الاصطناعي وتطوير التطبيقات."
            ),
        ),
        (
            "المطور والشركة",
            "نوفا",
            (
                "نوفا (Nova) هو المساعد الذكي المدمج القائم على قاعدة بيانات"
                " محليّة سريعة وشاملة لكل الحلول التقنية."
            ),
        ),
        # قسم الاشتراكات و VIP
        (
            "الاشتراكات والخدمات",
            "vip",
            (
                "يمكنك تفعيل سيرفر VIP المباشر عبر تحويل قيمة الاشتراك على"
                " محفظة أورنج كاش برقم 01213783090 ثم إرسال الإيصال للمطور محمد"
                " عادل لتلقي كود التفعيل."
            ),
        ),
        (
            "الاشتراكات والخدمات",
            "اشتراك",
            (
                "للاشتراك في الخدمات المتقدمة، يرجى التواصل مع الدعم الفني أو"
                " تحويل الاشتراك عبر أورنج كاش برقم 01213783090."
            ),
        ),
        (
            "الاشتراكات والخدمات",
            "اورنج كاش",
            (
                "رقم محفظة أورنج كاش المعتمد لتحويل الاشتراكات والخدمات هو:"
                " 01213783090."
            ),
        ),
        (
            "الاشتراكات والخدمات",
            "أورنج كاش",
            (
                "رقم محفظة أورنج كاش المعتمد لتحويل الاشتراكات والخدمات هو:"
                " 01213783090."
            ),
        ),
        (
            "الاشتراكات والخدمات",
            "تفعيل",
            (
                "لتفعيل كود VIP، قم بكتابة الكود في القائمة الجانبية واضغط على"
                " زر 'تأكيد وتفعيل VIP'."
            ),
        ),
        # قسم الدعم والتواصل
        (
            "الدعم الفني",
            "تواصل",
            (
                "يمكنك التواصل المباشر مع المطور التنفيذي محمد عادل عبر"
                " الواتساب على الرقم: +201102464297."
            ),
        ),
        (
            "الدعم الفني",
            "واتساب",
            (
                "رقم الواتساب الرسمي المباشر للمطور محمد عادل للدعم الفني هو:"
                " +201102464297."
            ),
        ),
        (
            "الدعم الفني",
            "دعم",
            (
                "فريق الدعم الفني متواجد لمساعدتك. تواصل مباشرة مع المطور محمد"
                " عادل على +201102464297."
            ),
        ),
        (
            "الدعم الفني",
            "رقم",
            (
                "الأرقام الرسمية: أورنج كاش للتحويل (01213783090) | واتساب"
                " التواصل (+201102464297)."
            ),
        ),
        # قسم البرمجة والحلول التقنية 2026
        (
            "البرمجة والتقنية",
            "python",
            (
                "بايثون (Python) هي لغة البرمجة الأساسية لبناء هذا التطبيق،"
                " حيث نعتمد على إصدارات متقدمة مع مكتبات Streamlit وSQLite."
            ),
        ),
        (
            "البرمجة والتقنية",
            "streamlit",
            (
                "إطار عمل Streamlit يتيح بناء واجهات تفاعلية سريعة ومستقرة"
                " لتطبيقات الذكاء الاصطناعي بدعم كامل للغة العربية."
            ),
        ),
        (
            "البرمجة والتقنية",
            "قاعدة بيانات",
            (
                "يعتمد هذا التطبيق على قاعدة بيانات محليّة من نوع SQLite مخزنة"
                " داخل المشروع لضمان استجابة لحظية واستقرار 100% بدون انقطاع."
            ),
        ),
        (
            "البرمجة والتقنية",
            "كود",
            (
                "جميع الأكواد في هذا التطبيق مصممة ومدمجة بنظام الملف الواحد"
                " لتسهيل الاستضافة والتحديث المستمر."
            ),
        ),
        (
            "البرمجة والتقنية",
            "حل مشكلة",
            (
                "لحل مشكلات توقف السيرفرات المجانية، تم الاستغناء تماماً عن"
                " المكتبات الخارجية والاعتماد الكامل على المحرك المحلي."
            ),
        ),
        # قسم أسئلة عامة برمجية
        (
            "معلومات عامة",
            "سلام",
            "وعليكم السلام ورحمة الله وبركاته! كيف يمكنني مساعدتك اليوم؟",
        ),
        (
            "معلومات عامة",
            "مرحبا",
            "أهلاً بك في منصة Nova AI Studio! أنا جاهز لإجابة جميع استفساراتك.",
        ),
        (
            "معلومات عامة",
            "ازيك",
            "الحمد لله! جاهز ومستعد لمساعدتك في أي وقت.",
        ),
        (
            "معلومات عامة",
            "شكرا",
            "العفو! في خدمتك دائماً.",
        ),
    ]
    c.executemany(
        "INSERT INTO local_knowledge (category, keyword, response) VALUES (?,"
        " ?, ?)",
        seed_data,
    )
    conn.commit()

  conn.close()


init_and_seed_db()


def query_local_db(user_query):
  """البحث الفوري المباشر داخل قاعدة البيانات المحلية SQLite"""
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()

  query_clean = user_query.strip().lower()

  # بحث مباشر بدقة التطابق
  c.execute(
      "SELECT response FROM local_knowledge WHERE LOWER(keyword) = ?",
      (query_clean,),
  )
  row = c.fetchone()

  if not row:
    # بحث جزئي بالكلمات المفتاحية
    c.execute(
        "SELECT response FROM local_knowledge WHERE ? LIKE '%' ||"
        " LOWER(keyword) || '%'",
        (query_clean,),
    )
    row = c.fetchone()

  conn.close()

  if row:
    return row[0]
  return None


# ==========================================
# 🔊 4. تحويل النص إلى صوت
# ==========================================
def text_to_audio(text):
  try:
    tts = gTTS(text=text, lang="ar")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
  except Exception:
    return None


# ==========================================
# 🔑 5. إدارة أكواد VIP المتقدمة (JSON محلي)
# ==========================================
CODES_FILE = "vip_codes.json"


def load_vip_codes():
  if not os.path.exists(CODES_FILE):
    default_expiry = (datetime.now() + timedelta(days=30)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    default_codes = {
        "NOVA2026": {"expiry": default_expiry, "days": 30},
        "KIVO_VIP": {"expiry": default_expiry, "days": 30},
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
  expiry_date = (datetime.now() + timedelta(days=days)).strftime(
      "%Y-%m-%d %H:%M:%S"
  )
  codes[code_name.strip()] = {"expiry": expiry_date, "days": days}
  save_vip_codes(codes)


def delete_vip_code(code_name):
  codes = load_vip_codes()
  if code_name in codes:
    del codes[code_name]
    save_vip_codes(codes)


def validate_vip_code(code_name):
  codes = load_vip_codes()
  if code_name not in codes:
    return False, "❌ الكود غير صحيح أو تم إلغاؤه."

  expiry_str = codes[code_name]["expiry"]
  expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

  if datetime.now() > expiry_date:
    return False, "⏳ هذا الكود انتهت مدة صلاحيته."

  return True, "🎉 تم تفعيل الكود بنجاح!"


# ==========================================
# 🤖 6. محرك الذكاء الاصطناعي المحلي
# ==========================================
def ask_nova_ai(prompt, is_vip=False):
  # 1. البحث الفوري داخل قاعدة البيانات المحلية SQLite
  local_res = query_local_db(prompt)
  if local_res:
    prefix = "⚡ **[إجابة سريعة من قاعدة البيانات المحلية]**\n\n" if is_vip else ""
    return f"{prefix}{local_res}"

  # 2. إجابة استرجاعية ذكية مدمجة للأسئلة العامة غير المسجلة
  prefix = "⚡ **[استجابة VIP المباشرة]**\n\n" if is_vip else ""
  return f"{prefix}سؤالك: '{prompt}' مسجل ومحفوظ، ولكن لم يتم العثور على إجابة نصية مطابقة داخل قاعدة البيانات المحلية حتى الآن. يمكنك إضافة الإجابة بجدول البيانات."


# ==========================================
# 🔒 7. إدارة الجلسة والمستخدمين
# ==========================================
SESSION_FILE = "user_session.txt"


def get_saved_user():
  if os.path.exists(SESSION_FILE):
    try:
      with open(SESSION_FILE, "r", encoding="utf-8") as f:
        email = f.read().strip()
        if email:
          return email
    except Exception:
      pass
  return None


def save_user(email):
  with open(SESSION_FILE, "w", encoding="utf-8") as f:
    f.write(email)


def delete_user_session():
  if os.path.exists(SESSION_FILE):
    try:
      os.remove(SESSION_FILE)
    except Exception:
      pass


if "user_email" not in st.session_state:
  st.session_state["user_email"] = get_saved_user()

if "vip_activated" not in st.session_state:
  st.session_state["vip_activated"] = False

if "active_code" not in st.session_state:
  st.session_state["active_code"] = ""

# ==========================================
# 🔑 8. شاشة التسجيل
# ==========================================
if not st.session_state["user_email"]:
  st.title("⚡ مرحباً بك في منصة Nova AI")
  st.caption("تطوير شركة كيفو (Kivo) - المطور التنفيذي محمد عادل")
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.subheader("🔑 تسجيل الدخول السريع")
    email = st.text_input(
        "البريد الإلكتروني (Email)", placeholder="jehejfkfbw@gmail.com"
    )
    password = st.text_input(
        "كلمة السر (Password)", type="password", placeholder="••••••••"
    )

    if st.button("دخول المنصة"):
      clean_email = email.strip().lower()
      if clean_email != "" and password.strip() != "":
        save_user(clean_email)
        st.session_state["user_email"] = clean_email
        st.rerun()
      else:
        st.error("يرجى إدخال البريد الإلكتروني وكلمة السر بشكل صحيح.")

# ==========================================
# 🚀 9. التطبيق الرئيسي
# ==========================================
else:
  user_email = st.session_state["user_email"]
  is_executive = user_email.strip().lower() == EXECUTIVE_EMAIL.lower()

  st.sidebar.title("☰ القائمة الرئيسية")
  st.sidebar.caption("تطبيق تابع لشركة **كيفو (Kivo)**")

  if is_executive:
    st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
  else:
    st.sidebar.info(f"👤 المستخدم: {user_email}")

  st.sidebar.markdown("---")

  # لوحة تحكم المطور لإضافة أكواد وقواعد بيانات
  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم VIP والأكواد")
    new_code = st.sidebar.text_input("أنشئ كود VIP جديد:")
    code_days = st.sidebar.number_input(
        "مدة الكود (بالأيام):", min_value=1, value=30, step=1
    )

    if st.sidebar.button("➕ إنشاء الكود"):
      if new_code.strip():
        add_vip_code(new_code.strip(), int(code_days))
        st.sidebar.success(f"تمت إضافة الكود: {new_code.strip()}")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**📊 الأكواد المتاحة:**")
    all_codes = load_vip_codes()
    for code_key, info in list(all_codes.items()):
      col_code, col_btn = st.sidebar.columns([3, 1])
      col_code.caption(f"🔑 `{code_key}` ({info['days']} يوم)")
      if col_btn.button("❌", key=f"del_{code_key}"):
        delete_vip_code(code_key)
        st.sidebar.warning(f"تم إلغاء: {code_key}")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("---")

  # اختيار السيرفر و أسلوب العمل
  st.sidebar.subheader("🌐 نمط التشغيل")
  server_option = st.sidebar.radio(
      "اختر النمط:",
      ["🌐 المحرك المحلي المباشر", "👑 سيرفر VIP المباشر"],
      index=1 if st.session_state["vip_activated"] else 0,
  )

  if server_option == "👑 سيرفر VIP المباشر":
    if not st.session_state["vip_activated"]:
      vip_code_input = st.sidebar.text_input(
          "🔑 أدخل كود التفعيل (VIP):", type="password"
      )
      if st.sidebar.button("✅ تأكيد وتفعيل VIP"):
        is_valid, msg = validate_vip_code(vip_code_input.strip())
        if is_valid:
          st.session_state["vip_activated"] = True
          st.session_state["active_code"] = vip_code_input.strip()
          st.sidebar.success(msg)
          time.sleep(0.5)
          st.rerun()
        else:
          st.sidebar.error(msg)

      st.sidebar.info(
          f"💸 **للتحويل والاشتراك:**\nأورنج كاش: `{ORANGE_CASH_NUMBER}`"
      )

  st.sidebar.markdown("---")

  if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك! نظام Nova المحلي جاهز."}
    ]

  if st.sidebar.button("➕ محادثة جديدة"):
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك مجدداً في Nova AI!"}
    ]
    st.rerun()

  if st.sidebar.button("🚪 تسجيل الخروج"):
    delete_user_session()
    st.session_state.clear()
    st.rerun()

  st.title("⚡ نوفا | Nova AI (قاعدة بيانات محلية 100%)")

  # عرض المحادثات
  for m in st.session_state.messages:
    with st.chat_message(m["role"]):
      st.markdown(m["content"])
      if "audio" in m and m["audio"]:
        st.audio(m["audio"], format="audio/mp3")

  # استقبال السؤال من المستخدم
  if user_prompt := st.chat_input("ابحث أو اسأل هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
      st.markdown(user_prompt)

    with st.chat_message("assistant"):
      res_text = ask_nova_ai(
          user_prompt, is_vip=st.session_state["vip_activated"]
      )
      st.markdown(res_text)

      audio_fp = text_to_audio(res_text)
      if audio_fp:
        st.audio(audio_fp, format="audio/mp3")

      st.session_state.messages.append({
          "role": "assistant",
          "content": res_text,
          "audio": audio_fp,
      })
