import base64
from datetime import datetime, timedelta
import io
import json
import os
import time
import urllib.parse
from g4f.client import Client
from g4f.Provider import Blackbox, DuckDuckGo, PollinationsAI
from gtts import gTTS
from PIL import Image
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة والجرافيك
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo VIP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 📲 2. إشعارات الواتساب وأرقام التواصل
# ==========================================
MY_PHONE = "201102464297"
ORANGE_CASH_NUMBER = "01213783090"
MY_API_KEY = "2586712"


def notify_admin_whatsapp(user_email, search_query, action_type="بحث / سؤال"):
  current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
  msg = f"""🚨 *نشاط جديد على تطبيق Nova*
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
# 🔑 4. إدارة أكواد VIP المتقدمة (تواريخ + حذف)
# ==========================================
CODES_FILE = "vip_codes.json"


def load_vip_codes():
  """تحميل الأكواد وبيانات انتهاء صلاحيتها"""
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
  """حفظ الأكواد في ملف JSON"""
  with open(CODES_FILE, "w", encoding="utf-8") as f:
    json.dump(codes_dict, f, ensure_ascii=False, indent=4)


def add_vip_code(code_name, days=30):
  """إضافة كود جديد مع مدة محددة بالأيام"""
  codes = load_vip_codes()
  expiry_date = (datetime.now() + timedelta(days=days)).strftime(
      "%Y-%m-%d %H:%M:%S"
  )
  codes[code_name.strip()] = {"expiry": expiry_date, "days": days}
  save_vip_codes(codes)


def delete_vip_code(code_name):
  """حذف كود وإلغاؤه فوراً"""
  codes = load_vip_codes()
  if code_name in codes:
    del codes[code_name]
    save_vip_codes(codes)


def validate_vip_code(code_name):
  """التحقق من صحة الكود وعدم انتهاء صلاحيته"""
  codes = load_vip_codes()
  if code_name not in codes:
    return False, "❌ الكود غير صحيح أو تم إلغاؤه من المطور."

  expiry_str = codes[code_name]["expiry"]
  expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

  if datetime.now() > expiry_date:
    return False, "⏳ هذا الكود انتهت مدة صلاحيته."

  return True, "🎉 تم تفعيل الكود بنجاح!"


# ==========================================
# 🤖 5. محرك الذكاء الاصطناعي القوي والمتعدد السيرفرات
# ==========================================
def ask_nova_ai(prompt, is_vip=False):
  sys_prompt = (
      "أنت مساعد ذكي ومتطور اسمه Nova تابع لشركة Kivo والمطور التنفيذي هو"
      " محمد عادل. أجب بأسلوب مفصل، شامل، وغني بالمعلومات والملاحظات الدقيقة"
      " دون اختصار."
  )
  client = Client()

  # 1. المحاولة الأولى: سيرفر Blackbox (سريع وممتاز جداً)
  try:
    response = client.chat.completions.create(
        model="gpt-4o",
        provider=Blackbox,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    res_text = response.choices[0].message.content
    if res_text and len(res_text.strip()) > 5:
      prefix = (
          "⚡ **[سيرفر VIP الفائق - استجابة فائقة السرعة]**\n\n"
          if is_vip
          else ""
      )
      return f"{prefix}{res_text.strip()}"
  except Exception:
    pass

  # 2. المحاولة الثانية: سيرفر DuckDuckGo
  try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        provider=DuckDuckGo,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    res_text = response.choices[0].message.content
    if res_text and len(res_text.strip()) > 5:
      return res_text.strip()
  except Exception:
    pass

  # 3. المحاولة الثالثة: Pollinations المباشر
  try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        provider=PollinationsAI,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    res_text = response.choices[0].message.content
    if res_text and len(res_text.strip()) > 5:
      return res_text.strip()
  except Exception:
    pass

  # 4. المحاولة الرابعة الاحتياطية المباشرة مع Pollinations API
  try:
    encoded_p = urllib.parse.quote(f"{sys_prompt}\nالسؤال: {prompt}")
    url = f"https://text.pollinations.ai/{encoded_p}?cache=false"
    res = requests.get(url, timeout=12)
    if res.status_code == 200 and len(res.text.strip()) > 5:
      return res.text.strip()
  except Exception:
    pass

  return "حدث ضغط مفاجئ على السيرفرات، يرجى إعادة إرسال سؤالك وسيجيب النظام فوراً."


# ==========================================
# 🔒 6. إدارة الجلسة
# ==========================================
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
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
# 🔑 7. شاشة التسجيل
# ==========================================
if not st.session_state["user_email"]:
  st.title("⚡ مرحباً بك في منصة Nova AI")
  st.caption("إحدى تطويرات شركة كيفو (Kivo)")
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
# 🚀 8. التطبيق الرئيسي
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

  # 🛠️ لوحة تحكم المطور (إضافة + تحديد أيام + حذف الأكواد)
  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم الاشتراك و الأكواد")
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

  # ⚙️ قسم اختيار السيرفر والاشتراك
  st.sidebar.subheader("🌐 نوع السيرفر")

  # التحقق التلقائي من صلاحية الكود المفعل
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

  # تصميم واجهة VIP
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
        "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! نظام Nova"
        " جاهز ومستعد للإجابة على كل الأسئلة بنجاح."
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
          "💬 الشات الذكي (صور + فيديوهات)",
          "🎨 استوديو توليد الصور والفيديوهات",
          "🕌 مواقيت الصلاة والعداد التنازلي",
      ],
  )

  if st.session_state["vip_activated"]:
    st.markdown(
        '<div class="vip-header">👑 Nova VIP Studio - الخادم الخاص السريع'
        " الفاخر</div>",
        unsafe_allow_html=True,
    )
  else:
    st.title("⚡ نوفا | Nova AI Studio")

  if is_executive:
    st.success("👑 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي)")

  st.markdown("---")

  if app_mode == "💬 الشات الذكي (صور + فيديوهات)":

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

  elif app_mode == "🎨 استوديو توليد الصور والفيديوهات":
    st.title("🎨 استوديو الوسائط - Nova Studio")
    p_img = st.text_input("صف الصورة التي تريدها:")
    if st.button("توليد الصورة 🎨") and p_img:
      img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true"
      st.image(img_url, caption=p_img)

  elif app_mode == "🕌 مواقيت الصلاة والعداد التنازلي":
    st.title("🕌 مواقيت الصلاة")
    st.info("قسم مواقيت الصلاة يعمل بنجاح.")
