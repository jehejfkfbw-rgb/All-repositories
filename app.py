import io
import json
import os
import sqlite3
import time
from datetime import datetime
from gtts import gTTS
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 📲 2. البيانات الثابتة
# ==========================================
ORANGE_CASH_NUMBER = "01213783090"
MY_PHONE = "201102464297"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
CODES_FILE = "vip_codes.json"

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
# 🔑 4. إدارة أكواد VIP
# ==========================================
def load_vip_codes():
  if not os.path.exists(CODES_FILE):
    return {
        "NOVA2026": {"days": 30},
        "KIVO_VIP": {"days": 30},
    }
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
    return True, "🎉 تم تفعيل سيرفر VIP الشامل بنجاح!"
  return False, "❌ الكود غير صحيح."


# ==========================================
# 🌐 5. السيرفر المحلي (إجابات بسيطة ومحدودة)
# ==========================================
def ask_local_server(prompt):
  p = prompt.strip().lower()
  now = datetime.now()

  # الوقت والتاريخ والثواني
  if any(x in p for x in ["الساعه", "التاريخ", "اليوم", "الوقت", "الثانيه"]):
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
    return f"📅 **اليوم:** {day_name}\n📆 **التاريخ:** {now.strftime('%Y-%m-%d')}\n⏰ **الوقت الحالي:** {now.strftime('%I:%M:%S %p')}"

  # الأهلي
  elif "اهلي" in p or "الأهلي" in p or "مباراه" in p:
    return "⚽ **النادي الأهلي:** موعد مباراة الأهلي القادمة متاح ضمن جدول المباريات المحلي (يرجى مراجعة الجدول الرسمي للبطولة)."

  elif "سلام" in p or "ازيك" in p or "مرحبا" in p:
    return "أهلاً بك في السيرفر المحلي البسيط! للحصول على الذكاء الاصطناعي الشامل والرد الصوتي المباشر، يرجى التفعيل لـ VIP."

  else:
    return "⚠️ **السيرفر المحلي محدود:** لا يحتوي على إجابات لهذا السؤال. اشترك في سيرفر **VIP** للحصول على الذكاء الاصطناعي الشامل (برمجة، رياضة، حل واجبات، محادثة صوتية)."


# ==========================================
# 👑 6. سيرفر VIP الشامل والذكاء الاصطناعي
# ==========================================
def ask_vip_server(prompt):
  sys_prompt = "أنت ذكاء اصطناعي متطور وشامل في كافة المجالات (برمجة، رياضة، حل واجبات، وإجابة أي سؤال). أنت تابع لشركة Kivo والمطور التنفيذي هو محمد عادل."
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
# 🔑 8. شاشة الدخول
# ==========================================
if not st.session_state["user_email"]:
  st.title("⚡ منصة Nova AI")
  st.caption("تطوير شركة كيفو (Kivo) - المطور التنفيذي محمد عادل")
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة السر", type="password")
    if st.button("دخول المنصة"):
      if email.strip() and password.strip():
        st.session_state["user_email"] = email.strip().lower()
        st.rerun()
      else:
        st.error("يرجى إدخال البيانات كاملة.")

# ==========================================
# 🚀 9. واجهة التطبيق
# ==========================================
else:
  user_email = st.session_state["user_email"]
  is_executive = user_email == EXECUTIVE_EMAIL.lower()

  st.sidebar.title("☰ القائمة")
  if is_executive:
    st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
  else:
    st.sidebar.info(f"👤 {user_email}")

  st.sidebar.markdown("---")

  # لوحة التحكم الخاصة بالمطور
  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم الأكواد")
    new_code = st.sidebar.text_input("كود VIP جديد:")
    if st.sidebar.button("➕ إضافة الكود"):
      if new_code.strip():
        add_vip_code(new_code.strip())
        st.sidebar.success("تم التجميع والإضافة!")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**الأكواد المتاحة:**")
    all_codes = load_vip_codes()
    for c_key in list(all_codes.keys()):
      c1, c2 = st.sidebar.columns([3, 1])
      c1.caption(f"🔑 `{c_key}`")
      if c2.button("❌", key=f"del_{c_key}"):
        delete_vip_code(c_key)
        st.rerun()

    st.sidebar.markdown("---")

  # اختيار نمط السيرفر
  server_mode = st.sidebar.radio(
      "اختر السيرفر:",
      ["🌐 السيرفر المحلي (بسيط ومحدود)", "👑 سيرفر VIP (الذكاء الشامل والصوتي)"],
      index=1 if st.session_state["vip_activated"] else 0,
  )

  if server_mode == "👑 سيرفر VIP (الذكاء الشامل والصوتي)":
    if not st.session_state["vip_activated"]:
      vip_input = st.sidebar.text_input("أدخل كود VIP:", type="password")
      if st.sidebar.button("تأكيد التفعيل"):
        ok, msg = validate_vip_code(vip_input.strip())
        if ok:
          st.session_state["vip_activated"] = True
          st.session_state["active_code"] = vip_input.strip()
          st.sidebar.success(msg)
          time.sleep(0.5)
          st.rerun()
        else:
          st.sidebar.error(msg)

      st.sidebar.info(f"💸 **للإشتراك:** تحويل أورنج كاش برقم `{ORANGE_CASH_NUMBER}`")

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 خروج"):
    st.session_state.clear()
    st.rerun()

  # الواجهة الرئيسية
  st.title("⚡ Nova AI Studio")

  if server_mode == "👑 سيرفر VIP (الذكاء الشامل والصوتي)":
    if st.session_state["vip_activated"]:
      st.success(
          "👑 **أنشط حالياً:** سيرفر VIP الشامل (برمجة، رياضة، حل واجبات، ومحادثة"
          " صوتية)."
      )
    else:
      st.warning("⚠️ يرجى أدخال كود VIP بالجانب للتفعيل.")

  else:
    st.info("🌐 **أنشط حالياً:** السيرفر المحلي (يحتوي فقط على الساعة، الأهلي، والأساسيات).")

  # نظام الشات التفاعلي والصوتي
  if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! كيف يمكنني مساعدتك؟"}
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
      if server_mode == "🌐 السيرفر المحلي (بسيط ومحدود)":
        answer = ask_local_server(user_prompt)
        audio_fp = None
      else:
        if not st.session_state["vip_activated"]:
          answer = "❌ يرجى تفعيل كود VIP أولاً لاستخدام الذكاء الاصطناعي الشامل والصوتي."
          audio_fp = None
        else:
          with st.spinner("VIP AI يتحدث ويجيب الآن... ⚡"):
            answer = ask_vip_server(user_prompt)
            # محاكاة التحدث والتطابق الصوتي المباشر Face-to-Face
            audio_fp = text_to_audio(answer)

      st.markdown(answer)
      if audio_fp:
        st.audio(audio_fp, format="audio/mp3")

      st.session_state.messages.append({
          "role": "assistant",
          "content": answer,
          "audio": audio_fp,
      })
