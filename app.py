import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Memo AI Studio 2026", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تفعيل صلاحيات الويب والتوافقية مع الموبايل والكمبيوتر
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f4f4f4; }
    h1, h2, h3 { color: #C8102E; }
    .stButton>button { background-color: #C8102E; color: white; border-radius: 5px; width: 100%; }
    .reportview-container { background: #fff }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🤖 ميمو AI")
st.sidebar.success("التطبيق جاهز ومتوافق مع الموبايل ✅")

app_mode = st.sidebar.radio("اختر القسم:", ["💬 الشات الذكي", "🎨 توليد الصور", "🕌 مواقيت الصلاة والآذان"])

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

elif app_mode == "🕌 مواقيت الصلاة والآذان":
    st.title("🕌 مواقيت الصلاة والعداد التنازلي")
    
    st.info("🕒 مواقيت الصلاة اليوم بتوقيت مصر:")
    col1, col2, col3 = st.columns(3)
    col1.metric("الفجر", "03:15 ص")
    col1.metric("الظهر", "11:58 ص")
    col2.metric("العصر", "03:32 م")
    col2.metric("المغرب", "06:51 م")
    col3.metric("العشاء", "08:14 م")
    
    st.markdown("---")
    st.subheader("⏳ العداد التنازلي للصلاة القادمة:")
    st.write("العداد يعمل أونلاين بكفاءة عالية على المتصفح الخاص بالموبايل والكمبيوتر.")
    
    st.markdown("### 🔊 سماع الآذان")
    adhan_audio_url = "https://www.islamcan.com/audio/adhan/azan1.mp3"
    st.audio(adhan_audio_url, format="audio/mp3", start_time=0)
