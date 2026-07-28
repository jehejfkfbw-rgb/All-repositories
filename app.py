import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
import os

st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

MY_WHATSAPP_NUMBER = "201213783090"

VALID_CODES = {
    "1111": "active", "2222": "active", "3333": "active", "4444": "active",
    "5555": "active", "6666": "active", "7777": "active", "8888": "active",
    "9999": "active", "1234": "active", "5678": "active", "4321": "active",
    "8765": "active", "2468": "active", "1357": "active"
}

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f4f4f4; }
    h1, h2, h3 { color: #C8102E; }
    .stButton>button { background-color: #C8102E; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

SESSION_FILE = "permanent_user_session.txt"

if "logged_in" not in st.session_state:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            st.session_state.logged_in = bool(f.read().strip())
    else:
        st.session_state.logged_in = False

if "step" not in st.session_state:
    st.session_state.step = "phone_step"
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1>🤖 تفعيل تطبيق ميمو</h1>", unsafe_allow_html=True)
        
        if st.session_state.step == "phone_step":
            phone_input = st.text_input("أدخل رقم هاتفك:", placeholder="مثال: 010xxxxxxxx")
            if st.button("حفظ الرقم والمتابعة", use_container_width=True):
                if phone_input:
                    st.session_state.user_phone = phone_input.strip()
                    st.session_state.step = "code_step"
                    st.rerun()
                else:
                    st.error("الرجاء إدخال رقم الهاتف أولاً.")

        elif st.session_state.step == "code_step":
            st.success(f"رقمك المسجل: **{st.session_state.user_phone}**")
            
            st.info(f"للحصول على كود التفعيل، راسلني مباشرة على رقم الواتساب التالي:\n\n📱 **{MY_WHATSAPP_NUMBER}**\n\nواكتب لي: (أريد تفعيل رقمي: {st.session_state.user_phone})")
            
            st.markdown("---")
            entered_code = st.text_input("أدخل كود التفعيل المكون من 4 أرقام:", max_chars=4, type="password")
            
            if st.button("فتح التطبيق وثبته دائماً", use_container_width=True):
                if entered_code in VALID_CODES:
                    st.session_state.logged_in = True
                    with open(SESSION_FILE, "w", encoding="utf-8") as f:
                        f.write(st.session_state.user_phone)
                    st.success("تم التفعيل بنجاح!")
                    st.rerun()
                else:
                    st.error("كود التفعيل غير صحيح.")
            
            if st.button("الرجوع لتغيير رقم الهاتف"):
                st.session_state.step = "phone_step"
                st.rerun()
    st.stop()

st.sidebar.title("🤖 ميمو AI")
st.sidebar.success("التطبيق مفعل ✅")
if st.sidebar.button("تسجيل الخروج"):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    st.session_state.logged_in = False
    st.session_state.step = "phone_step"
    st.rerun()

app_mode = st.sidebar.radio("اختر القسم:", ["💬 الشات الذكي", "🎨 توليد الصور"])

if app_mode == "💬 الشات الذكي":
    st.title("💬 ميمو - الشات الذكي")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "أهلاً يا فنان! اكتب سؤالك."}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
        with st.chat_message("assistant"):
            try:
                res = str(g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": user_prompt}]))
            except Exception as e:
                res = f"خطأ: {e}"
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

elif app_mode == "🎨 توليد الصور":
    st.title("🎨 استوديو توليد الصور")
    p = st.text_input("صف الصورة:")
    if st.button("توليد") and p:
        st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true")
