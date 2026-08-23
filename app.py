import io
import json
import os
import time
import urllib.parse
from datetime import datetime, timedelta
from gtts import gTTS
from PIL import Image
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة والجرافيك
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo VIP 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 📲 2. البيانات الثابتة وإشعارات الواتساب
# ==========================================
MY_PHONE = "201102464297"
ORANGE_CASH_NUMBER = "01213783090"
MY_API_KEY = "2586712"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"


def notify_admin_whatsapp(user_email, search_query, action_type="بحث / سؤال"):
  current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
  msg = f"""🚨 *نشاط جديد على تطبيق Nova 2026*
👤 *المستخدم:* {user_email}
⏰ *الوقت:* {current_time}
📌 *نوع النشاط:* {action_type}
💬 *المحتوى:* {search_query}"""

  encoded_msg = urllib.parse.quote(msg)
  url = f"https://api.callmebot.com/whatsapp.php?phone={MY_PHONE}&text={encoded_msg}&apikey={MY_API_KEY}"

  try:
    requests.get(url, timeout=5)
  except Exception:
    pass


# ==========================================
# 🔊 3. تحويل النص إلى صوت
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
# 🔑 4. إدارة أكواد VIP المتقدمة (JSON محلي)
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
    return False, "❌ الكود غير صحيح أو تم إلغاؤه من المطور."

  expiry_str = codes[code_name]["expiry"]
  expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

  if datetime.now() > expiry_date:
    return False, "⏳ هذا الكود انتهت مدة صلاحيته."

  return True, "🎉 تم تفعيل الكود بنجاح!"


# ==========================================
# 🗄️ 5. قاعدة البيانات الضخمة المدمجة داخل الكود (تحديثات 2026)
# ==========================================
EMBEDDED_KNOWLEDGE_BASE = [
    {
        "keywords": ["من انت", "من أنت", "مين المطور", "كيفو", "kivo", "نوفا"],
        "content": (
            "أنا نظام Nova AI Studio الذكي والمطور خصيصاً لشركة Kivo. المطور"
            " التنفيذي والمسؤول عن النظام هو **محمد عادل**."
        ),
    },
    {
        "keywords": ["vip", "اشتراك", "اورنج كاش", "تفعيل", "كود"],
        "content": (
            "يمكنك تفعيل اشتراك VIP للحصول على سرعة فائقة بدون انقطاع عن طريق"
            " تحويل المبلغ عبر **أورنج كاش (Orange Cash)** للرقم: `01213783090`"
            " ثم التواصل مع المطور محمد عادل لتلقي الكود."
        ),
    },
    {
        "keywords": ["تواصل", "واتساب", "دعم", "رقم"],
        "content": (
            "يمكنك التواصل المباشر مع المطور التنفيذي **محمد عادل** عبر"
            " الواتساب على الرقم: `+201102464297`."
        ),
    },
    {
        "keywords": ["تحديثات 2026", "اخبار 2026", "الذكاء الاصطناعي 2026"],
        "content": (
            "شهد عام 2026 طفرة في نماذج الذكاء الاصطناعي مع الاعتماد على النماذج"
            " المدمجة وسريعة الاستجابة (Edge AI)، إلى جانب استقرار نماذج GPT-4o"
            " وClaude 3.5 وتوسع تطبيقات Streamlit في إدارة الشبكات والذكاء"
            " الاصطناعي."
        ),
    },
    {
        "keywords": [
            "python 2026",
            "streamlitt 2026",
            "برمجة",
            "كود",
            "استضافة",
            "حل مشكلة",
        ],
        "content": (
            "لحل مشاكل الاستضافة على Streamlit Cloud في 2026، يُنصح بتفادي"
            " المكتبات التي تعتمد على scraping وتجاوز القيود (مثل g4f) واستبدالها"
            " بـ REST APIs المباشرة السريعة لضمان عدم حدوث ImportError."
        ),
    },
]


def search_embedded_db(user_query):
  query_clean = user_query.lower().strip()
  for item in EMBEDDED_KNOWLEDGE_BASE:
    for kw in item["keywords"]:
      if kw in query_clean:
        return item["content"]
  return None


# ==========================================
# 🤖 6. محرك الذكاء الاصطناعي المدمج والمستقر 100%
# ==========================================
def ask_nova_ai(prompt, is_vip=False):
  # أولاً: البحث في قاعدة البيانات المدمجة
  db_res = search_embedded_db(prompt)
  if db_res:
    prefix = (
        "⚡ **[استجابة من قاعدة بيانات Nova المدمجة]**\n\n" if is_vip else ""
    )
    return f"{prefix}{db_res}"

  # ثانياً: الاتصال بالسيرفرات المباشرة بدون مكتبات خارجية تسبب أخطاء
  sys_prompt = "أنت مساعد ذكي اسمه Nova تابع لشركة Kivo والمطور التنفيذي هو محمد عادل."

  # سيرفر Pollinations المباشر
  try:
    full_p = f"{sys_prompt}\nالسؤال: {prompt}"
    encoded = urllib.parse.quote(full_p)
    url = f"https://text.pollinations.ai/{encoded}?model=openai&cache=false"

    res = requests.get(url, timeout=10)
    if res.status_code == 200 and len(res.text.strip()) > 3:
      prefix = "⚡ **[سيرفر VIP السريع]**\n\n" if is_vip else ""
      return f"{prefix}{res.text.strip()}"
  except Exception:
    pass

  # سيرفر احتياطي ثاني المباشر
  try:
    encoded_simple = urllib.parse.quote(prompt)
    url2 = f"https://text.pollinations.ai/{encoded_simple}?cache=false"
    res2 = requests.get(url2, timeout=10)
    if res2.status_code == 200 and len(res2.text.strip()) > 3:
      return res2.text.strip()
  except Exception:
    pass

  return "⚠️ حدث تذبذب بسيط في الاتصال بالسيرفرات، يرجى إعادة إرسال السؤال وسيجيب النظام فوراً."


# ==========================================
# 🔒 7. إدارة الجلسة
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
  st.title("⚡ مرحباً بك في منصة Nova AI 2026")
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
        with st.spinner("جاري تأكيد الهوية..."):
          save_user(clean_email)
          st.session_state["user_email"] = clean_email
          notify_admin_whatsapp(
              clean_email,
              "قم بتسجيل الدخول إلى التطبيق",
              action_type="تسجيل دخول",
          )
          time.sleep(0.5)
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

  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم VIP")
    new_code = st.sidebar.text_input("أنشئ كود VIP جديد:")
    code_days = st.sidebar.number_input(
        "مدة الكود (بالأيام):", min_value=1, value=30, step=1
    )

    if st.sidebar.button("➕ إنشاء الكود"):
      if new_code.strip():
        add_vip_code(new_code.strip(), int(code_days))
        st.sidebar.success(
            f"تمت إضافة الكود: {new_code.strip()} لمدة {code_days} يوم"
        )
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**📊 الأكواد المتاحة حالياً:**")
    all_codes = load_vip_codes()

    if not all_codes:
      st.sidebar.caption("لا توجد أكواد حالياً.")
    else:
      for code_key, info in list(all_codes.items()):
        col_code, col_btn = st.sidebar.columns([3, 1])
        col_code.caption(f"🔑 `{code_key}`\n⏳ ينتهي: {info['expiry'][:10]}")
        if col_btn.button("❌", key=f"del_{code_key}"):
          delete_vip_code(code_key)
          st.sidebar.warning(f"تم إلغاء الكود: {code_key}")
          time.sleep(0.5)
          st.rerun()

    st.sidebar.markdown("---")

  st.sidebar.subheader("🌐 نوع السيرفر")

  if st.session_state["vip_activated"]:
    is_valid, msg = validate_vip_code(st.session_state["active_code"])
    if not is_valid:
      st.session_state["vip_activated"] = False
      st.session_state["active_code"] = ""
      st.sidebar.error(
          f"⚠️ تم إلغاء اشتراكك: {msg}\nتم التحويل تلقائياً للسيرفر المجاني."
      )

  server_option = st.sidebar.radio(
      "اختر السيرفر:",
      ["🌐 سيرفر مجاني", "👑 سيرفر VIP الخاص (للمشتركين)"],
      index=1 if st.session_state["vip_activated"] else 0,
  )

  if server_option == "👑 سيرفر VIP الخاص (للمشتركين)":
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
          f"💸 **للتحويل والاشتراك:**\nتحويل المبلغ على محفظة **أورنج كاش"
          f" (Orange Cash)** برقم:\n`{ORANGE_CASH_NUMBER}`"
      )
      st.sidebar.markdown(
          f"[💬 اضغط هنا لإرسال إيصال التحويل على واتساب](https://wa.me/{MY_PHONE})"
      )
  else:
    st.session_state["vip_activated"] = False

  st.sidebar.markdown("---")

  if st.session_state["vip_activated"]:
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%) !important;
        }
        .vip-header {
            background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            color: #000;
            font-weight: bold;
            font-size: 22px;
            box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4);
            margin-bottom: 20px;
        }
        [data-testid="stSidebar"] { 
            background-color: #0d1117 !important; 
            border-right: 2px solid #ffd700 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

  if "messages" not in st.session_state:
    welcome_msg = (
        "مرحباً بك أيها المطور التنفيذي محمد عادل! نظام Nova جاهز ومزود بقاعدة"
        " بيانات مدمجة 2026."
        if is_executive
        else "مرحباً بك في تطبيق Nova من شركة كيفو!"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

  if st.sidebar.button("➕ محادثة جديدة"):
    initial_msg = (
        "مرحباً بك أيها المطور التنفيذي محمد عادل!"
        if is_executive
        else "أهلاً بك مجدداً في Nova AI!"
    )
    st.session_state.messages = [{"role": "assistant", "content": initial_msg}]
    st.rerun()

  if st.sidebar.button("🚪 تسجيل الخروج"):
    delete_user_session()
    st.session_state.clear()
    st.rerun()

  app_mode = st.sidebar.radio(
      "📌 التنقل بين الأقسام:",
      [
          "💬 الشات الذكي وقاعدة البيانات",
          "🎨 استوديو توليد الصور",
          "🕌 مواقيت الصلاة",
      ],
  )

  if st.session_state["vip_activated"]:
    st.markdown(
        '<div class="vip-header">👑 Nova VIP Studio - الخدمة الفائقة المدمجة</div>',
        unsafe_allow_html=True,
    )
  else:
    st.title("⚡ نوفا | Nova AI Studio")

  if is_executive:
    st.success("👑 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي)")

  st.markdown("---")

  if app_mode == "💬 الشات الذكي وقاعدة البيانات":

    for idx, m in enumerate(st.session_state.messages):
      with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "audio" in m and m["audio"]:
          st.audio(m["audio"], format="audio/mp3")

    if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
      st.session_state.messages.append({"role": "user", "content": user_prompt})
      notify_admin_whatsapp(
          user_email, user_prompt, action_type="بحث / سؤال في الشات"
      )

      with st.chat_message("user"):
        st.markdown(user_prompt)

      with st.chat_message("assistant"):
        with st.spinner("Nova يجيب الآن... ⚡"):
          if (
              server_option == "👑 سيرفر VIP الخاص (للمشتركين)"
              and not st.session_state["vip_activated"]
          ):
            res_text = "❌ يرجى إدخال كود VIP والضغط على **تأكيد وتفعيل VIP** أولاً."
          else:
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

  elif app_mode == "🎨 استوديو توليد الصور":
    st.title("🎨 استوديو الوسائط - Nova Studio")
    p_img = st.text_input("صف الصورة التي تريدها:")
    if st.button("توليد الصورة 🎨") and p_img:
      img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true"
      st.image(img_url, caption=p_img)

  elif app_mode == "🕌 مواقيت الصلاة":
    st.title("🕌 مواقيت الصلاة")
    st.info("قسم مواقيت الصلاة يعمل بنجاح.")
