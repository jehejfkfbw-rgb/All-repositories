import streamlit as st
import g4f
from PIL import Image
import urllib.parse
import time
import os

# --- إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="Nova AI Studio - Kivo", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تنسيق التصميم (CSS) لإخفاء أدوات التحميل المزعجة وجعل الواجهة مثل التطبيقات ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f4f4f4; }
    h1, h2, h3 { color: #1E88E5; }
    .stButton>button { background-color: #1E88E5; color: white; border-radius: 5px; width: 100%; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #1565C0; }
    .history-item { padding: 10px; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 5px; font-size: 14px; }
    
    /* إخفاء مؤشر التحميل التقليدي ليظهر بشكل أوتوماتيكي أنيق */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- البريد المخصص للمطور التنفيذي ---
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"

# --- إدارة حالة تسجيل الدخول (تسجيل المرة الواحدة) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_executive" not in st.session_state:
    st.session_state.is_executive = False

# ==========================================
# 🔒 1. شاشة التسجيل (تظهر مرة واحدة فقط)
# ==========================================
if not st.session_state.logged_in:
    st.title("⚡ مرحباً بك في Nova AI")
    st.caption("إحدى تطويرات شركة كيفو (Kivo)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 تسجيل الدخول")
        email = st.text_input("البريد الإلكتروني (Email)", placeholder="jehejfkfbw@gmail.com")
        password = st.text_input("كلمة السر (Password)", type="password", placeholder="••••••••")
        
        if st.button("دخول"):
            clean_email = email.strip().lower()
            if clean_email != "" and password.strip() != "":
                with st.spinner("جاري التحقق وتسجيل الدخول..."):
                    time.sleep(0.5)
                    st.session_state.logged_in = True
                    st.session_state.user_email = clean_email
                    
                    if clean_email == EXECUTIVE_EMAIL.lower():
                        st.session_state.is_executive = True
                    else:
                        st.session_state.is_executive = False
                        
                    st.rerun()
            else:
                st.error("يرجى إدخال البريد الإلكتروني وكلمة السر بشكل صحيح.")

# ==========================================
# 🚀 2. التطبيق الرئيسي (بعد التسجيل)
# ==========================================
else:
    st.sidebar.title("⚡ نوفا | Nova AI")
    st.sidebar.caption("تطبيق تابع لشركة **كيفو (Kivo)**")

    # ترحيب القائمة الجانبية
    if st.session_state.is_executive:
        st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
    else:
        st.sidebar.info(f"👤 العميل: {st.session_state.user_email}")

    # --- إدارة سجل المحادثات والرسالة الترحيبية الأولى ---
    if "messages" not in st.session_state:
        if st.session_state.is_executive:
            welcome_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! نظام Nova في خدمتك بالكامل."
        else:
            welcome_msg = "مرحباً بك في تطبيق Nova من شركة كيفو! أنا مساعدك الذكي، كيف يمكنني مساعدتك اليوم؟"
            
        st.session_state.messages = [
            {"role": "assistant", "content": welcome_msg}
        ]

    st.sidebar.markdown("---")
    st.sidebar.subheader("🗂️ سجل المحادثة")

    has_history = False
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            has_history = True
            st.sidebar.markdown(f'<div class="history-item">🗣️ {msg["content"][:30]}...</div>', unsafe_allow_html=True)

    if not has_history:
        st.sidebar.write("لا يوجد سجل حالياً.")

    if st.sidebar.button("🗑️ مسح السجل بالكامل"):
        initial_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو!" if st.session_state.is_executive else "مرحباً بك في تطبيق Nova من شركة كيفو!"
        st.session_state.messages = [{"role": "assistant", "content": initial_msg}]
        st.rerun()

    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.is_executive = False
        st.rerun()

    st.sidebar.markdown("---")

    app_mode = st.sidebar.radio("اختر القسم:", ["💬 الشات الذكي (Nova)", "🕌 مواقيت الصلاة والعداد التنازلي", "🎨 توليد الصور"])

    # ------------------------------------------
    # 💬 قسم الشات الذكي (Nova AI)
    # ------------------------------------------
    if app_mode == "💬 الشات الذكي (Nova)":
        st.title("⚡ الذكاء الاصطناعي Nova")
        
        if st.session_state.is_executive:
            st.success("🌟 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي لشركة كيفو)")
        else:
            st.markdown("### مرحباً بك في **Nova** من شركة **كيفو (Kivo)**، اسأله أي سؤال وسيجيبك فوراً.")
            
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                
        if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant"):
                # تعليمات الذكاء الاصطناعي حول المطور والشركة
                system_instruction = (
                    "أنت مساعد ذكي اسمك Nova (نوفا) تابع لشركة كيفو (Kivo). "
                    "إذا سألك أي شخص من المطور أو من صنعك أو من طورك، يجب أن تجيب دائماً بوضوح وبصيغة احترافية: "
                    "'المطور التنفيذي هو محمد عادل من شركة كيفو (Kivo)'."
                )
                
                api_messages = [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ]

                # شاشة التحميل الأوتوماتيكية عند معالجة الرد
                with st.spinner("Nova يفكر الآن... ⚡"):
                    try:
                        res = str(g4f.ChatCompletion.create(model=g4f.models.default, messages=api_messages))
                    except Exception as e:
                        res = f"حدث خطأ أثناء الاتصال: {e}"
                
                # كتابة الكلام تدريجياً كلمة بكلمة تلقائياً
                message_placeholder = st.empty()
                streamed_text = ""
                for word in res.split():
                    streamed_text += word + " "
                    message_placeholder.markdown(streamed_text + "▌")
                    time.sleep(0.02)
                message_placeholder.markdown(res)
                    
            st.session_state.messages.append({"role": "assistant", "content": res})

    # ------------------------------------------
    # 🕌 قسم مواقيت الصلاة
    # ------------------------------------------
    elif app_mode == "🕌 مواقيت الصلاة والعداد التنازلي":
        st.title("🕌 مواقيت الصلاة والعداد التنازلي اللحظي")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("الفجر", "03:15 ص")
        col1.metric("الظهر", "11:58 ص")
        col2.metric("العصر", "03:32 م")
        col2.metric("المغرب", "06:51 م")
        col3.metric("العشاء", "08:14 م")
        
        st.markdown("---")
        st.subheader("⏳ العداد التنازلي (ينزل ثانية بثانية):")
        
        countdown_placeholder = st.empty()
        for seconds_left in range(300, 0, -1):
            mins, secs = divmod(seconds_left, 60)
            countdown_placeholder.markdown(f"🚨 **باقي على الصلاة القادمة: {mins} دقيقة و {secs} ثانية**")
            time.sleep(1)
        
        st.markdown("### 🔊 مشغل صوت الآذان")
        adhan_audio_url = "https://www.islamcan.com/audio/adhan/azan1.mp3"
        st.audio(adhan_audio_url, format="audio/mp3", start_time=0)

    # ------------------------------------------
    # 🎨 قسم توليد الصور
    # ------------------------------------------
    elif app_mode == "🎨 توليد الصور":
        st.title("🎨 استوديو توليد الصور - Nova")
        p = st.text_input("صف الصورة التي تريدها:")
        if st.button("توليد") and p:
            with st.spinner("جاري رسم الصورة بأعلى دقة... 🎨"):
                st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true")
