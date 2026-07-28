import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
import os

# ==========================================
# 1. إعدادات التطبيق الأساسية
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

# رقم واتساب الخاص بك (لاستقبال الرسائل)
MY_WHATSAPP_NUMBER = "201213783090"

# الأكواد المكونة من 4 أرقام لتفعيل التطبيق
VALID_CODES = {
    "1111": "active",
    "2222": "active",
    "3333": "active",
    "4444": "active",
    "5555": "active",
    "6666": "active",
    "7777": "active",
    "8888": "active",
    "9999": "active",
    "1234": "active",
    "5678": "active",
    "4321": "active",
    "8765": "active",
    "2468": "active",
    "1357": "active"
}

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f4f4f4;
    }
    h1, h2, h3 {
        color: #C8102E;
    }
    .stButton>button {
        background-color: #C8102E;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

SESSION_FILE = "permanent_user_session.txt"

if "logged_in" not in st.session_state:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            if f.read().strip():
                st.session_state.logged_in = True
            else:
                st.session_state.logged_in = False
    else:
        st.session_state.logged_in = False

if "step" not in st.session_state:
    st.session_state.step = "phone_step"
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""

# ==========================================
# 2. شاشة التفعيل وطلب الكود عبر الواتساب
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1>🤖 تفعيل تطبيق ميمو</h1>
                <p style="color: gray;">اكتب رقمك ثم اضغط على زر الواتساب بالأسفل لمراسلتي</p>
            </div>
        """, unsafe_allow_html=True)
        
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
            
            # تجهيز رسالة الواتساب الرابط الرسمي
            wa_message = f"مرحباً يا فنان، أريد تفعيل تطبيق ميمو ليبقى مفتوحاً دائماً.\nرقم هاتفي هو: {st.session_state.user_phone}"
            encoded_message = urllib.parse.quote(wa_message)
            wa_link = f"https://wa.me/{MY_WHATSAPP_NUMBER}?text={encoded_message}"
            
            # استخدام زر اللينك الرسمي في ستريمليت لفتح الواتساب بدون أي حظر وبكل أمان
            st.link_button("💚 اضغط هنا للتواصل عبر الواتساب وإرسال الرقم", wa_link, use_container_width=True)
            
            st.markdown("---")
            entered_code = st.text_input("أدخل كود التفعيل المكون من 4 أرقام:", max_chars=4, type="password")
            
            if st.button("فتح التطبيق وثبته دائماً", use_container_width=True):
                if entered_code in VALID_CODES:
                    st.session_state.logged_in = True
                    with open(SESSION_FILE, "w", encoding="utf-8") as f:
                        f.write(st.session_state.user_phone)
                    st.success("تم التفعيل بنجاح! سيبقى التطبيق مفتوحاً معك دائماً...")
                    st.rerun()
                else:
                    st.error("كود التفعيل غير صحيح.")
            
            if st.button("الرجوع لتغيير رقم الهاتف"):
                st.session_state.step = "phone_step"
                st.rerun()
                
    st.stop()

# ==========================================
# 3. واجهة التطبيق الرئيسية (مفتوحة وثابتة دائماً)
# ==========================================
st.sidebar.title("🤖 ميمو AI - InnovaSoft")
st.sidebar.success("التطبيق مفعل ومفتوح دائماً ✅")

if st.sidebar.button("إلغاء التفعيل (تسجيل الخروج)"):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    st.session_state.logged_in = False
    st.session_state.step = "phone_step"
    st.rerun()

st.sidebar.markdown("---")
menu_options = [
    "💬 الشات الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي"
]
app_mode = st.sidebar.radio("اختر القسم:", menu_options)

if app_mode == "💬 الشات الذكي":
    st.title("💬 ميمو - الشات الذكي السريع")
    st.write("أهلاً بك، اسأل عن أي شيء وسأرد عليك فوراً!")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "أهلاً يا فنان! أنا جاهز، اكتب سؤالك وهيجيلك الرد في ثانية."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك أو بحثك هنا..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("ميمو بيكتب الرد..."):
                try:
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    bot_reply = str(response)
                except Exception as e:
                    bot_reply = f"عذراً حدث خطأ: {e}"
                
                st.markdown(bot_reply)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    image_prompt = st.text_input("صف الصورة التي تريد توليدها:")
    if st.button("توليد الصورة"):
        if image_prompt:
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(image_prompt)}?width=1024&height=1024&nologo=true", caption=image_prompt)
