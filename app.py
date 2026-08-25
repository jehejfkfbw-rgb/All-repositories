import io
import json
import os
import time
from datetime import datetime, timedelta
import google.generativeai as genai
from gtts import gTTS
from huggingface_hub import InferenceClient
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio 2026", page_icon="⚡", layout="wide"
)

ORANGE_CASH_NUMBER = "01213783090"
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
CODES_FILE = "vip_codes.json"

# مفتاح Google Gemini الخاص بسيرفر VIP
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
  genai.configure(api_key=GEMINI_API_KEY)


# ==========================================
# 🔊 2. محرك تحويل النص إلى صوت (gTTS)
# ==========================================
def text_to_audio_bytes(text):
  """تحويل نص رد الذكاء الاصطناعي إلى صوت ملف MP3 في الذاكرة."""
  try:
    # تنظيف النص من علامات Markdown لتشغيل صوتي نقي
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
# 🔑 3. نظام إدارة الأكواد والاشتراكات
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
    return False, "⏳ انتهت مدة صلاحية اشتراك VIP، تم التحويل للسيرفر المجاني."

  return True, "🎉 اشتراك VIP يعمل بنجاح."


# ==========================================
# 🌐 4. السيرفر المجاني (مكتبة الذكاء الاصطناعي)
# ==========================================
def ask_local_server(prompt):
  try:
    client = InferenceClient("Qwen/Qwen2.5-Coder-32B-Instruct")
    messages = [
        {
            "role": "system",
            "content": (
                "أنت المساعد الذكي المجاني لمنصة نوفا (Nova AI Studio). أجب"
                " على سؤال المستخدم بذكاء ووضوح."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    response = client.chat_completion(
        messages=messages, max_tokens=600, temperature=0.7
    )
    return response.choices[0].message.content
  except Exception:
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
      return f"📅 اليوم: {days_ar[now.weekday()]}\n📆 التاريخ: {now.strftime('%Y-%m-%d')}\n⏰ الوقت: {now.strftime('%I:%M:%S %p')}"
    return "🤖 **السيرفر المجاني:** تعذر الاتصال بالمحرك المجاني موقتاً، يرجى إعادة المحاولة."


# ==========================================
# 👑 5. سيرفر VIP (Google Gemini API)
# ==========================================
def ask_vip_server(prompt):
  if not GEMINI_API_KEY:
    return "⚠️ **تنبيه VIP:** لم يتم إضافة API Key الخاص بـ Google Gemini بعد. يرجى إضافته في إعدادات المنصة لتفعيل السيرفر المدفوع."

  sys_p = "أنت مساعد VIP ذكي وفائق القدرات لمنصة Nova AI Studio. المطور هو محمد عادل لشركة Kivo."
  try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=sys_p
    )
    response = model.generate_content(prompt)
    if response and response.text:
      return response.text
  except Exception as e:
    return f"⚡ **خطأ VIP:** تعذر الاتصال بسيرفر جوجل Gemini ({e})."


# ==========================================
# 🚀 6. تطبيق الواجهة والتحكم
# ==========================================
if "user_email" not in st.session_state:
  st.session_state["user_email"] = None
if "vip_activated" not in st.session_state:
  st.session_state["vip_activated"] = False
if "active_code" not in st.session_state:
  st.session_state["active_code"] = ""

if not st.session_state["user_email"]:
  st.title("⚡ منصة Nova AI Studio 2026")
  email = st.text_input("البريد الإلكتروني:")
  passw = st.text_input("كلمة السر:", type="password")
  if st.button("تسجيل الدخول"):
    if email and passw:
      st.session_state["user_email"] = email.strip().lower()
      st.rerun()
else:
  user = st.session_state["user_email"]
  is_exec = user == EXECUTIVE_EMAIL.lower()

  # التحقق من صلاحية الكود المفعل
  if st.session_state["vip_activated"]:
    ok, msg = validate_and_check_expiry(st.session_state["active_code"])
    if not ok:
      st.session_state["vip_activated"] = False
      st.session_state["active_code"] = ""
      st.error(f"⚠️ {msg}")

  st.sidebar.title("☰ لوحة التحكم")

  # ==========================================
  # 🛠️ لوحة التحكم الخاصة بالمطور فقط
  # ==========================================
  if is_exec:
    st.sidebar.success("👑 مرحباً بك يا مطور المنصة")
    st.sidebar.subheader("🛠️ إدارة الاشتراكات للأكواد")
    c_name = st.sidebar.text_input("كود VIP جديد:")
    c_days = st.sidebar.number_input(
        "مدة الصلاحية (بالأيام):", min_value=1, value=30
    )
    if st.sidebar.button("➕ إنشاء الكود"):
      if c_name:
        add_vip_code(c_name, c_days)
        st.sidebar.success(f"تم إنشاء الكود `{c_name}` لمدة {c_days} يوم!")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("**الأكواد المسجلة:**")
    all_c = load_vip_codes()
    for k, v in list(all_c.items()):
      c1, c2 = st.sidebar.columns([3, 1])
      c1.caption(f"🔑 `{k}` | ⏳ {v['expiry'][:10]}")
      if c2.button("❌", key=f"del_{k}"):
        delete_vip_code(k)
        st.rerun()

    # --- قسم الكتب والمناهج الأزهري (حصري للمطور) ---
    st.sidebar.divider()
    st.sidebar.subheader("📚 مكتبة منهج 1 إعدادي أزهر")
    azhar_choice = st.sidebar.selectbox(
        "اختر الكتاب المطلوب:",
        [
            "اللغة العربية - المطالعة والنصوص وفنون الكتابة",
            "اللغة العربية - القواعد النحوية والصرفية",
            "بوابة المناهج المركزية (PDF)",
        ],
    )

    if azhar_choice == "اللغة العربية - المطالعة والنصوص وفنون الكتابة":
      st.sidebar.markdown(
          "[📥 فتح وتحميل كتاب المطالعة والنصوص"
          " (PDF)](https://azhar.gov.eg/Materials/prep.htm)"
      )
    elif azhar_choice == "اللغة العربية - القواعد النحوية والصرفية":
      st.sidebar.markdown(
          "[📥 فتح وتحميل كتاب النحو والصرف"
          " (PDF)](https://azhar.gov.eg/Materials/prep.htm)"
      )
    else:
      st.sidebar.markdown(
          "[🌐 رابط المكتبة المركزية الرسمية"
          " للأزهر](https://mtrl.azhar.gov.eg/t/index.htm)"
      )

  # ==========================================
  # 💳 تفعيل حسابات المستخدمين
  # ==========================================
  st.sidebar.divider()
  st.sidebar.subheader("💳 تفعيل حساب VIP")
  if not st.session_state["vip_activated"]:
    st.sidebar.info(f"للاشتراك، قم بالتحويل إلى: `{ORANGE_CASH_NUMBER}`")
    v_code = st.sidebar.text_input("أدخل كود VIP الخاص بك:", type="password")
    if st.sidebar.button("⚡ تفعيل VIP"):
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

  # ==========================================
  # 💬 الواجهة الرئيسية للمحادثة والصوت
  # ==========================================
  st.title("⚡ Nova AI Studio 2026")

  if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "أهلاً بك في منصة Nova AI Studio! اكتب سؤالك هنا وسأجيبك فوراً."
            ),
        }
    ]

  # عرض المحادثات السابقة مع مشغل الصوت الخاص بالرد
  for idx, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
      st.markdown(m["content"])
      if m["role"] == "assistant":
        if f"audio_{idx}" in st.session_state:
          st.audio(st.session_state[f"audio_{idx}"], format="audio/mp3")

  if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("جاري التفكير والتوليد الصوتي..."):
        if st.session_state["vip_activated"]:
          ans = ask_vip_server(prompt)
        else:
          ans = ask_local_server(prompt)

        # تحويل رد الذكاء الاصطناعي إلى صوت عبر gTTS
        audio_fp = text_to_audio_bytes(ans)
        curr_idx = len(st.session_state.messages)

      st.markdown(ans)
      if audio_fp:
        audio_bytes = audio_fp.read()
        st.audio(audio_bytes, format="audio/mp3")
        st.session_state[f"audio_{curr_idx}"] = audio_bytes

      st.session_state.messages.append({"role": "assistant", "content": ans})
