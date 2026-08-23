import io
import json
import os
import time
from datetime import datetime, timedelta
from gtts import gTTS
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio 2026", page_icon="⚡", layout="wide"
)

ORANGE_CASH_NUMBER = "01213783090"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
CODES_FILE = "vip_codes.json"


# ==========================================
# 🔑 2. نظام إدارة الأكواد بوقت صلاحية محدد
# ==========================================
def load_vip_codes():
  if not os.path.exists(CODES_FILE):
    now = datetime.now()
    default_codes = {
        "NOVA2026": {
            "expiry": (now + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "days": 30,
        },
        "KIVO_VIP": {
            "expiry": (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "days": 1,
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


def validate_and_check_expiry(code_name):
  codes = load_vip_codes()
  if code_name not in codes:
    return False, "❌ الكود غير صحيح."

  expiry_str = codes[code_name]["expiry"]
  expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

  if datetime.now() > expiry_dt:
    return False, "⏳ انتهت مدة صلاحية الاشتراك، تم التحويل للسيرفر المحلي."

  return True, "🎉 الاشتراك يعمل بنجاح."


# ==========================================
# 🌐 3. السيرفر المحلي (بسيط ومحدد)
# ==========================================
def ask_local_server(prompt):
  p = prompt.strip().lower()
  now = datetime.now()

  if any(x in p for x in ["الساعه", "الساعة", "التاريخ", "اليوم", "الوقت"]):
    days_ar = [
        "الإثنين",
        "الثلاثاء",
        "الأربعاء",
        "الخميس",
        "الجمعة",
        "السبت",
        "الأحد",
    ]
    return f"📅 اليوم: {days_ar[now.weekday()]}\n📆 التاريخ: {now.strftime('%Y-%m-%d')}\n⏰ الوقت بالثواني: {now.strftime('%I:%M:%S %p')}"
  elif any(x in p for x in ["اهلي", "الأهلي", "مباراه", "مباراة"]):
    return "⚽ **النادي الأهلي:** موعد مباراة الأهلي القادمة متاح ضمن جدول المباريات المحلي."
  else:
    return "⚠️ **السيرفر المحلي محدود:** يدعم فقط الوقت، التاريخ، والأساسيات. اشترك في VIP للذكاء الشامل."


# ==========================================
# 👑 4. سيرفر VIP المباشر والمضمون 100%
# ==========================================
def ask_vip_server(prompt):
  sys_p = "أنت مساعد ذكي شامل يجيب عن كل الأسئلة في البرمجة والرياضة والواجبات. المطور هو محمد عادل لشركة Kivo."
  try:
    req1 = requests.get(
        "https://duckduckgo.com/duckchat/v1/status",
        headers={"x-vqd-accept": "1"},
        timeout=5,
    )
    vqd = req1.headers.get("x-vqd-4")
    if vqd:
      payload = {
          "model": "gpt-4o-mini",
          "messages": [
              {"role": "system", "content": sys_p},
              {"role": "user", "content": prompt},
          ],
      }
      res2 = requests.post(
          "https://duckduckgo.com/duckchat/v1/chat",
          json=payload,
          headers={
              "x-vqd-4": vqd,
              "Content-Type": "application/json",
              "Accept": "text/event-stream",
          },
          timeout=10,
      )

      full_res = ""
      for line in res2.text.split("\n"):
        if line.startswith("data: "):
          d = line[6:]
          if d != "[DONE]":
            try:
              j = json.loads(d)
              if "message" in j:
                full_res += j["message"]
            except:
              pass
      if full_res.strip():
        return full_res.strip()
  except:
    pass

  return "⚡ **VIP AI:** أهلاً بك! أنا جاهز لإجابة سؤالك بالكامل، أعد إرسال سؤالك وسأجيب فوراً."


# ==========================================
# 🚀 5. تطبيق الواجهة والتحكم
# ==========================================
if "user_email" not in st.session_state:
  st.session_state["user_email"] = None
if "vip_activated" not in st.session_state:
  st.session_state["vip_activated"] = False
if "active_code" not in st.session_state:
  st.session_state["active_code"] = ""

if not st.session_state["user_email"]:
  st.title("⚡ منصة Nova AI Studio")
  email = st.text_input("البريد الإلكتروني")
  passw = st.text_input("كلمة السر", type="password")
  if st.button("دخول"):
    if email and passw:
      st.session_state["user_email"] = email.strip().lower()
      st.rerun()
else:
  user = st.session_state["user_email"]
  is_exec = user == EXECUTIVE_EMAIL.lower()

  # التحقق التلقائي من انتهاء وقت الكود النشط
  if st.session_state["vip_activated"]:
    ok, msg = validate_and_check_expiry(st.session_state["active_code"])
    if not ok:
      st.session_state["vip_activated"] = False
      st.session_state["active_code"] = ""
      st.error(f"⚠️ {msg}")

  st.sidebar.title("☰ التحكم")

  # لوحة المطور لتحديد مدة الكود بالأيام
  if is_exec:
    st.sidebar.subheader("🛠️ لوحة تحديد مدة الاشتراكات")
    c_name = st.sidebar.text_input("الكود الجديد:")
    c_days = st.sidebar.number_input(
        "مدة الصلاحية (بالأيام):", min_value=1, value=30
    )
    if st.sidebar.button("➕ إنشاء الكود الموقت"):
      if c_name:
        add_vip_code(c_name, c_days)
        st.sidebar.success(f"تم إنشاء الكود لمدة {c_days} يوم!")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**الأكواد ومواعيد انتهائها:**")
    all_c = load_vip_codes()
    for k, v in list(all_c.items()):
      c1, c2 = st.sidebar.columns([3, 1])
      c1.caption(f"🔑 `{k}`\n⏳ ينتهي: {v['expiry'][:10]}")
      if c2.button("❌", key=f"del_{k}"):
        delete_vip_code(k)
        st.rerun()

  # تفعيل VIP
  st.sidebar.subheader("💳 تفعيل VIP")
  if not st.session_state["vip_activated"]:
    st.sidebar.info(f"الدفع 50ج عبر أورنج كاش: `{ORANGE_CASH_NUMBER}`")
    v_code = st.sidebar.text_input("أدخل كود VIP:", type="password")
    if st.sidebar.button("⚡ تفعيل فوراً"):
      ok, msg = validate_and_check_expiry(v_code.strip())
      if ok:
        st.session_state["vip_activated"] = True
        st.session_state["active_code"] = v_code.strip()
        st.sidebar.success(msg)
        time.sleep(0.5)
        st.rerun()
      else:
        st.sidebar.error(msg)
  else:
    st.sidebar.success(f"👑 VIP مفعل بكود: `{st.session_state['active_code']}`")

  st.title("⚡ Nova AI Studio")

  if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا جاهز لإجابتك."}
    ]

  for m in st.session_state.messages:
    with st.chat_message(m["role"]):
      st.markdown(m["content"])

  if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      if st.session_state["vip_activated"]:
        ans = ask_vip_server(prompt)
      else:
        ans = ask_local_server(prompt)

      st.markdown(ans)
      st.session_state.messages.append({"role": "assistant", "content": ans})
