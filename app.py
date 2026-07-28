import streamlit as st
import g4f
from PIL import Image
import urllib.parse
import time
from gtts import gTTS
import os

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
    .history-item { padding: 10px; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 5px; font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🤖 ميمو AI")
st.sidebar.success("التطبيق يعمل بكفاءة ✅")

# --- بداية إضافة سجل المحادثات في الجنب ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً يا فنان! أنا ميمو، اسألني أي سؤال وسأجيبك فوراً."}]

st.sidebar.markdown("---")
st.sidebar.subheader("🗂️ سجل المحادثة")

# عرض الأسئلة السابقة في القائمة الجانبية
has_history = False
for msg in st.session_state.messages:
    if msg["role"] == "user":
        has_history = True
        # عرض أول 30 حرف من السؤال عشان ماياخدش مساحة كبيرة
        st.sidebar.markdown(f'<div class="history-item">🗣️ {msg["content"][:30]}...</div>', unsafe_allow_html=True)

if not has_history:
    st.sidebar.write("لا يوجد سجل حالياً.")

# زرار مسح السجل
if st.sidebar.button("🗑️ مسح السجل بالكامل"):
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً يا فنان! أنا ميمو، اسألني أي سؤال وسأجيبك فوراً."}]
    st.rerun() # لإعادة تحميل الصفحة وتحديث السجل
st.sidebar.markdown("---")
# --- نهاية إضافة سجل المحادثات ---

app_mode = st.sidebar.radio("اختر القسم:", ["💬 الشات الذكي (ميمو)", "🕌 مواقيت الصلاة والعداد التنازلي", "🎨 توليد الصور"])

if app_mode == "💬 الشات الذكي (ميمو)":
    st.title("🤖 الذكاء الاصطناعي ميمو")
    st.markdown("### مرحباً بك في الذكاء الاصطناعي ميمو، اسأله أي سؤال يجاوبك عليه فوراً.")
        
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
                res = f"حدث خطأ يا فنان: {e}"
            
            # كتابة الكلام تدريجياً كلمة بكلمة
            message_placeholder = st.empty()
            streamed_text = ""
            for word in res.split():
                streamed_text += word + " "
                message_placeholder.markdown(streamed_text + "▌")
                time.sleep(0.03)
            message_placeholder.markdown(res)
            
            # تحويل النص إلى صوت ونطقه
            try:
                tts = gTTS(text=res, lang='ar')
                tts.save("response.mp3")
                st.audio("response.mp3", format="audio/mp3")
            except:
                st.warning("عفواً، لم أتمكن من توليد الصوت لهذه الرسالة.")
                
        st.session_state.messages.append({"role": "assistant", "content": res})

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

elif app_mode == "🎨 توليد الصور":
    st.title("🎨 استوديو توليد الصور")
    p = st.text_input("صف الصورة التي تريدها:")
    if st.button("توليد") and p:
        st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true")
