import streamlit as st
import g4f
from PIL import Image
import urllib.parse
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Memo AI Studio 2026", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f4f4f4; }
    h1, h2, h3 { color: #C8102E; }
    .stButton>button { background-color: #C8102E; color: white; border-radius: 5px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🤖 ميمو AI")
st.sidebar.success("التطبيق جاهز ومتوافق مع الموبايل ✅")

# القائمة الجانبية للتنقل بين الأقسام
app_mode = st.sidebar.radio("اختر القسم:", ["🕌 مواقيت الصلاة والعداد", "💬 الشات الذكي", "🎨 توليد الصور"])

if app_mode == "🕌 مواقيت الصلاة والعداد":
    st.title("🕌 مواقيت الصلاة والعداد التنازلي")
    st.write("أهلاً بك يا فنان! هذا القسم يظهر في وجهة التطبيق مباشرة لمتابعة أوقات الصلاة.")
    
    # عرض مواقيت الصلاة
    col1, col2, col3 = st.columns(3)
    col1.metric("الفجر", "03:15 ص")
    col1.metric("الظهر", "11:58 ص")
    col2.metric("العصر", "03:32 م")
    col2.metric("المغرب", "06:51 م")
    col3.metric("العشاء", "08:14 م")
    
    st.markdown("---")
    st.subheader("⏳ العداد التنازلي للصلاة القادمة (الفجر / الظهر)")
    
    # محاكاة عداد تنازلي نشط يظهر في الواجهة
    st.warning("🚨 باقي على موعد الصلاة القادمة: **ساعة و 12 دقيقة و 45 ثانية**")
    
    # مشغل صوت الآذان
    st.markdown("### 🔊 مشغل صوت الآذان")
    st.write("اضغط تشغيل لاستماع الآذان فور دخولك التطبيق:")
    adhan_audio_url = "https://www.islamcan.com/audio/adhan/azan1.mp3"
    st.audio(adhan_audio_url, format="audio/mp3", start_time=0)

elif app_mode == "💬 الشات الذكي":
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
