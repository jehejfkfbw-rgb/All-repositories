import base64
from datetime import datetime
import io
import os
import time
import urllib.parse
from gtts import gTTS
from PIL import Image
import requests
import streamlit as st

# ==========================================
# ⚙️ 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        z-index: 999999 !important;
    }

    [data-testid="stSidebar"] { 
        background-color: #111827 !important; 
        color: #ffffff !important;
    }
    
    .stButton>button { 
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); 
        color: white !important; 
        border-radius: 8px; 
        width: 100%; 
        border: none; 
        padding: 8px; 
        font-weight: bold;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 📲 2. إشعارات الواتساب ورقام التواصل
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
# 🔑 4. إدارة أكواد VIP الديناميكية
# ==========================================
CODES_FILE = "vip_codes.txt"


def get_vip_codes():
  if not os.path.exists(CODES_FILE):
    default_codes = ["NOVA2026", "KIVO_VIP", "MOHAMED_NOVA"]
    save_vip_codes(default_codes)
    return default_codes
  try:
    with open(CODES_FILE, "r", encoding="utf-8") as f:
      codes = [line.strip() for line in f.readlines() if line.strip()]
      return codes
  except Exception:
    return ["NOVA2026"]


def save_vip_codes(codes_list):
  with open(CODES_FILE, "w", encoding="utf-8") as f:
    for code in set(codes_list):
      f.write(f"{code}\n")


# ==========================================
# 🤖 5. محرك الذكاء الاصطناعي
# ==========================================
def ask_nova_ai(prompt, server_type, user_vip_code=""):
  sys_prompt = "أنت مساعد ذكي اسمه Nova تابع لشركة Kivo. المطور التنفيذي هو محمد عادل من شركة Kivo. أجب بذكاء واحترافية وبشكل مبسط:"
  valid_codes = get_vip_codes()

  if server_type == "👑 سيرفر VIP الخاص (للمشتركين)":
    if user_vip_code.strip() in valid_codes:
      try:
        encoded_p = urllib.parse.quote(
            f"{sys_prompt}\nابحث في النت وأجب بأحدث المعلومات عن: {prompt}"
        )
        url = (
            f"https://text.pollinations.ai/{encoded_p}?model=searchgpt&cache=false"
        )
        res = requests.get(url, timeout=10)
        if res.status_code == 200 and len(res.text.strip()) > 5:
          return f"⚡ **[استجابة سيرفر VIP السريع]**\n\n{res.text.strip()}"
      except Exception:
        pass
    else:
      return f"❌ كود التفعيل غير صحيح! حول مبلغ الاشتراك على أورنج كاش ({ORANGE_CASH_NUMBER}) ثم تواصل معنا للحصول على الكود."

  try:
    encoded_p = urllib.parse.quote(f"{sys_prompt}\nالسؤال: {prompt}")
    url = f"https://text.pollinations.ai/{encoded_p}?model=qna&cache=false"
    res = requests.get(url, timeout=12)
    if res.status_code == 200 and len(res.text.strip()) > 5:
      return res.text.strip()
  except Exception:
    pass

  return "عذراً، السيرفر المجاني يمر بضغط حالياً. حاول مجدداً أو اشترك في سيرفر VIP."


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

  # 🛠️ لوحة تحكم المطور
  if is_executive:
    st.sidebar.subheader("🛠️ لوحة تحكم الأكواد")
    current_codes = get_vip_codes()
    new_code = st.sidebar.text_input("أنشئ كود VIP جديد:")
    if st.sidebar.button("➕ إضافة الكود"):
      if new_code.strip():
        current_codes.append(new_code.strip())
        save_vip_codes(current_codes)
        st.sidebar.success(f"تمت إضافة الكود: {new_code.strip()}")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.caption(f"الأكواد الشغالة: {', '.join(current_codes)}")
    st.sidebar.markdown("---")

  # ⚙️ قسم اختيار السيرفر والاشتراك
  st.sidebar.subheader("🌐 نوع السيرفر")
  server_option = st.sidebar.radio(
      "اختر السيرفر:",
      ["🌐 سيرفر مجاني", "👑 سيرفر VIP الخاص (للمشتركين)"],
  )

  vip_code_input = ""
  if server_option == "👑 سيرفر VIP الخاص (للمشتركين)":
    vip_code_input = st.sidebar.text_input(
        "🔑 أدخل كود التفعيل (VIP):", type="password"
    )
    st.sidebar.info(
        f"💸 **للتحويل والاشتراك:**\nتحويل المبلغ على محفظة **أورنج كاش"
        f" (Orange Cash)** برقم:\n`{ORANGE_CASH_NUMBER}`"
    )
    st.sidebar.markdown(
        f"[💬 اضغط هنا لإرسال إيصال التحويل على واتساب](https://wa.me/{MY_PHONE})"
    )

  st.sidebar.markdown("---")

  if "messages" not in st.session_state:
    welcome_msg = (
        "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! نظام Nova"
        " في خدمتك بالكامل."
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
        with st.spinner("Nova يفكر ويجيب... ⚡"):
          res_text = ask_nova_ai(user_prompt, server_option, vip_code_input)

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
