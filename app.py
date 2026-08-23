import io
import json
import os
import time
from datetime import datetime
from gtts import gTTS
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 📲 2. البيانات الثابتة وإعدادات الاشتراك
# ==========================================
ORANGE_CASH_NUMBER = "01213783090"
MY_PHONE = "201102464297"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
CODES_FILE = "vip_codes.json"
VIP_PRICE = "50 جنيه مصري / شهرياً"

# ==========================================
# 🔊 3. دالة تحويل النص إلى صوت (Voice AI)
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
# 🔑 4. نظام إدارة الأكواد والتفعيل التلقائي
# ==========================================
def load_vip_codes():
  if not os.path.exists(CODES_FILE):
    default_codes = {
        "NOVA2026": {"days": 30},
        "KIVO_VIP": {"days": 30},
        "MOHAMED50": {"days": 30},
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
  codes[code_name.strip()] = {"days": days}
  save_vip_codes(codes)


def delete_vip_code(code_name):
  codes = load_vip_codes()
  if code_name in codes:
    del codes[code_name]
    save_vip_codes(codes)


def validate_vip_code(code_name):
  codes = load_vip_codes()
  if code_name in codes:
    return True, "🎉 تم تفعيل سيرفر VIP الشامل تلقائياً!"
  return False, "❌ الكود غير صحيح، يرجى التاكد من الكود أو دفع الاشتراك."


# ==========================================
# 🌐 5. محرك السيرفر المحلي (بسيط ومحدود)
# ==========================================
def ask_local_server(prompt):
  p = prompt.strip().lower()
  now = datetime.now()

  # الوقت والتاريخ والثواني
  if any(
      x in p
      for x in ["الساعه", "الساعة", "التاريخ", "اليوم", "الوقت", "الثانيه", "الدقيقه"]
  ):
    days_ar = [
        "الإثنين",
        "الثلاثاء",
        "الأربعاء",
        "الخميس",
        "الجمعة",
        "السبت",
        "الأحد",
    ]
    day_name = days_ar[now.weekday()]
    return f"📅 **اليوم:** {day_name}\n📆 **التاريخ:** {now.strftime('%Y-%m-%d')}\n⏰ **الوقت بالثواني:** {now.strftime('%I:%M:%S %p')}"

  # معلومات الأهلي
  elif any(x in p for x in ["اهلي", "الأهلي", "مباراه", "مباراة"]):
    return "⚽ **النادي الأهلي:** موعد مباراة الأهلي القادمة متاح ضمن جدول المباريات المحلي (يرجى مراجعة الجدول الرسمي للبطولة)."

  elif any(x in p for x in ["سلام", "ازيك", "مرحبا", "هاي"]):
    return "أهلاً بك في السيرفر المحلي البسيط! للحصول على الذكاء الاصطناعي الشامل والرد الصوتي المباشر، يرجى التفعيل لـ VIP."

  else:
    return "⚠️ **السيرفر المحلي محدود:** لا يحتوي على إجابة لهذا السؤال. اشترك في سيرفر **VIP** للحصول على الذكاء الاصطناعي الشامل (برمجة، رياضة، حل واجبات، محادثة صوتية)."


# ==========================================
# 👑 6. محرك سيرفر VIP (الذكاء الاصطناعي الشامل)
# ==========================================
def ask_vip_server(prompt):
  sys_prompt = "أنت ذكاء اصطناعي خارق متطور وشامل في كافة المجالات (برمجة، رياضة، حل واجبات، وإجابة أي سؤال). أنت تابع لشركة Kivo والمطور التنفيذي هو محمد عادل."
  try:
    full_prompt = f"{sys_prompt}\n\nسؤال المستخدم: {prompt}"
    url = f"https://text.pollinations.ai/{requests.utils.quote(full_prompt)}?model=openai&cache=false"
    res = requests.get(url, timeout=12)
    if res.status_code == 200 and len(res.text.strip()) > 2:
      return res.text.strip()
  except Exception:
    pass

  return "⚡ **VIP AI:** أنا جاهز لإجابتك في كافة المجالات، يرجى إعادة إرسال السؤال مرة أخرى."


# ==========================================
# 🔒 7. إدارة الجلسة
# ==========================================
if "user_email" not in st.session_state:
  st.session_state["user_email"] = None

if "vip_activated" not in st.session_state:
  st.session_state["vip_activated"] = False

if "active_code" not in st.session_state:
  st.session_state["active_code"] = ""

# ==========================================
# 🔑 8. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["user_email"]:
  st.title("⚡ منصة Nova AI Studio")
  st.caption("تطوير شركة كيفو (Kivo) - المطور التنفيذي محمد عادل")
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.subheader("🔑 دخول المنصة")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة السر", type="password")
    if st.button("دخول المنصة"):
      if email.strip() and password.strip():
        st.session_state["user_email"] = email.strip().lower()
        st.rerun()
      else:
        st.error("يرجى إدخال البريد وكلمة السر.")

# ==========================================
# 🚀 9. واجهة التطبيق الرئيسية
# ==========================================
else:
  user_email = st.session_state["user_email"]
  is_executive = user_email == EXECUTIVE_EMAIL.lower()

  st.sidebar.title("☰ القائمة الرئيسية")
  if is_executive:
    st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
  else:
    st.sidebar.info(f"👤 {user_email}")

  st.sidebar.markdown("---")

  # 🛠️ لوحة تحكم المطور (إضافة وإلغاء الأكواد)
  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم الأكواد (Executive)")
    new_code = st.sidebar.text_input("إضافة كود VIP جديد:")
    if st.sidebar.button("➕ إنشاء الكود"):
      if new_code.strip():
        add_vip_code(new_code.strip())
        st.sidebar.success("تمت إضافة الكود بنجاح!")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**🔑 الأكواد المتاحة في السيستم:**")
    all_codes = load_vip_codes()
    for c_key in list(all_codes.keys()):
      c1, c2 = st.sidebar.columns([3, 1])
      c1.caption(f"• `{c_key}`")
      if c2.button("❌", key=f"del_{c_key}"):
        delete_vip_code(c_key)
        st.rerun()

    st.sidebar.markdown("---")

  # 💳 قسم الاشتراك والتفعيل التلقائي المباشر
  st.sidebar.subheader("💳 الاشتراك وتفعيل VIP")

  if not st.session_state["vip_activated"]:
    st.sidebar.info(f"""
        💰 **المبلغ المطلوب:** {VIP_PRICE}
        📱 **طريقة الدفع:** تحويل كاش إلى الرقم:
        `{ORANGE_CASH_NUMBER}`
        """)

    vip_input = st.sidebar.text_input(
        "🔑 أدخل كود VIP للتفعيل التلقائي:",
        type="password",
        placeholder="أدخل الكود هنا...",
    )
    if st.sidebar.button("⚡ تأكيد وتفعيل VIP فوراً"):
      ok, msg = validate_vip_code(vip_input.strip())
      if ok:
        st.session_state["vip_activated"] = True
        st.session_state["active_code"] = vip_input.strip()
        st.sidebar.success(msg)
        time.sleep(0.8)
        st.rerun()
      else:
        st.sidebar.error(msg)
  else:
    st.sidebar.success(
        f"🎉 **سيرفر VIP مفعل بنجاح!**\nالكود النشط: `{st.session_state['active_code']}`"
    )

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.clear()
    st.rerun()

  # 🖥️ واجهة العرض الشاشة الرئيسية
  st.title("⚡ Nova AI Studio - Kivo")

  if st.session_state["vip_activated"]:
    st.success(
        "👑 **الوضع الحالي:** سيرفر VIP المباشر مفعل (ذكاء اصطناعي شامل +"
        " محادثة صوتية Face-to-Face)."
    )
  else:
    st.warning(
        "🌐 **الوضع الحالي:** السيرفر المحلي (يحتوي فقط على الساعة، الأهلي،"
        " والردود البسيطة). قم بتفعيل VIP للوصول للذكاء الكامل."
    )

  # 💬 نظام المحادثة والصوت التفاعلي
  if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! كيف يمكنني مساعدتك اليوم؟"}
    ]

  for m in st.session_state.messages:
    with st.chat_message(m["role"]):
      st.markdown(m["content"])
      if "audio" in m and m["audio"]:
        st.audio(m["audio"], format="audio/mp3")

  if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
      st.markdown(user_prompt)

    with st.chat_message("assistant"):
      if not st.session_state["vip_activated"]:
        answer = ask_local_server(user_prompt)
        audio_fp = None
      else:
        with st.spinner("VIP AI يجيب ويدعم الرد الصوتي... ⚡"):
          answer = ask_vip_server(user_prompt)
          audio_fp = text_to_audio(answer)

      st.markdown(answer)
      if audio_fp:
        st.audio(audio_fp, format="audio/mp3")

      st.session_state.messages.append({
          "role": "assistant",
          "content": answer,
          "audio": audio_fp,
      })
