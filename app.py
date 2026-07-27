import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from gtts import gTTS
import os
from datetime import datetime
import pytz

# ==========================================
# 1. إعدادات تطبيق ميمو الذكي
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

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

# دالة تحويل النص إلى صوت
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        audio_file = "memo_voice.mp3"
        tts.save(audio_file)
        return audio_file
    except:
        return None

# ==========================================
# 2. القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.title("🤖 ميمو AI - إنتاج InnovaSoft")
st.sidebar.write("شات ذكي صوتي + توليد صور + محرر")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("اختر القسم:", [
    "💬 الشات الصوتي الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "✏️ محرر الصور والفلاتر"
])

# ==========================================
# 3. قسم الشات الصوتي الذكي
# ==========================================
if app_mode == "💬 الشات الصوتي الذكي":
    st.title("💬 ميمو - الشات الصوتي")
    st.write("اسأل عن الوقت في أي دولة عربية أو أمريكا، أو اسألني عن اسمي وصاحب الشركة!")
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for idx, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "audio" in message:
                st.audio(message["audio"], format="audio/mp3")

    if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
        lower_prompt = user_prompt.lower()
        
        # الرد على الوقت والساعة حسب الدول المطلوبة
        if "الساعة" in user_prompt or "الوقت" in user_prompt or "كام الساعه" in lower_prompt or "كام الساعة" in lower_prompt:
            # خريطة توقيت الدول العربية وأمريكا
            timezones = {
                'مصر': 'Africa/Cairo',
                'السعودية': 'Asia/Riyadh',
                'الامارات': 'Asia/Dubai',
                'الإمارات': 'Asia/Dubai',
                'الكويت': 'Asia/Kuwait',
                'قطر': 'Asia/Qatar',
                'البحرين': 'Asia/Bahrain',
                'عمان': 'Asia/Muscat',
                'الأردن': 'Asia/Amman',
                'فلسطين': 'Asia/Gaza',
                'لبنان': 'Asia/Beirut',
                'سوريا': 'Asia/Damascus',
                'العراق': 'Asia/Baghdad',
                'اليمن': 'Asia/Aden',
                'السودان': 'Africa/Khartoum',
                'ليبيا': 'Africa/Tripoli',
                'تونس': 'Africa/Tunis',
                'الجزائر': 'Africa/Algiers',
                'المغرب': 'Africa/Casablanca',
                'موريتانيا': 'Africa/Nouakchott',
                'الصومال': 'Africa/Mogadishu',
                'جيبوتي': 'Africa/Djibouti',
                'جزر القمر': 'Africa/Indian/Comoro',
                'امريكا': 'America/New_York',
                'أمريكا': 'America/New_York',
                'الولايات المتحدة': 'America/New_York'
            }
            
            # معرفة الدولة المطلوبة من نص المستخدم
            found_country = None
            for country, tz_name in timezones.items():
                if country in user_prompt:
                    found_country = country
                    target_tz = pytz.timezone(tz_name)
                    break
            
            # لو مفيش دولة محددة، نخليه يرجع توقيت مصر افتراضياً
            if not found_country:
                target_tz = pytz.timezone('Africa/Cairo')
                found_country = 'مصر'
            
            current_time = datetime.now(target_tz)
            time_str = current_time.strftime('%I:%M %p')
            time_str = time_str.replace('AM', 'صباحاً').replace('PM', 'مساءً')
            bot_reply = f"الساعة الآن في {found_country} هي {time_str}"
            
        # الرد على صاحب الشركة
        elif "صاحب الشركة" in user_prompt or "مين صاحبك" in user_prompt or "مؤسس" in user_prompt or "صاحب شركه" in user_prompt:
            bot_reply = "صاحب ومؤسس شركة InnovaSoft هو المبرمج محمد!"
            
        # الرد على الهوية والصانع
        elif "اسمك" in user_prompt or "اسمك ايه" in user_prompt or "من أنت" in user_prompt or "انت مين" in user_prompt or "صنعك" in user_prompt or "شركتك" in user_prompt or "مين عملك" in user_prompt:
            bot_reply = "أنا اسمي ميمو، وتم تطويري وبرمجتي بواسطة شركة **InnovaSoft**!"
            
        # باقي الأسئلة للشات الحر
        else:
            with st.spinner("جاري التفكير وتوليد الصوت..."):
                try:
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": user_prompt}],
                    )
                    bot_reply = str(response)
                except Exception as e:
                    bot_reply = f"عذراً حدث خطأ بسيط: {e}"

        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            audio_path = text_to_speech(bot_reply)
            if audio_path:
                st.audio(audio_path, format="audio/mp3")
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply, "audio": audio_path})
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# ==========================================
# 4. قسم توليد الصور بالذكاء الاصطناعي
# ==========================================
elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    st.write("صف أي صورة تتخيلها وسيتم رسمها فوراً!")
    st.markdown("---")

    image_prompt = st.text_input("صف الصورة:", placeholder="مثال: مدينة مستقبلية مضيئة")

    if st.button("توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري رسم الصورة..."):
                try:
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.success("تم توليد الصورة بنجاح!")
                    st.image(image_url, caption=image_prompt, use_column_width=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")
        else:
            st.warning("الرجاء كتابة وصف للصورة أولاً.")

# ==========================================
# 5. قسم محرر الصور والفلاتر
# ==========================================
elif app_mode == "✏️ محرر الصور والفلاتر":
    st.title("✏️ ميمو - محرر الصور")
    st.write("ارفع صورتك وعدل إضاءتها وتباينها بلمسة زر.")
    st.markdown("---")

    file = st.file_uploader("اختر صورة...", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="الصورة الأصلية", use_column_width=True)

        st.sidebar.markdown("### أدوات التعديل")
        brightness = st.sidebar.slider("الإضاءة", 0.1, 3.0, 1.0)
        contrast = st.sidebar.slider("التباين", 0.1, 3.0, 1.0)

        edited = ImageEnhance.Brightness(img).enhance(brightness)
        edited = ImageEnhance.Contrast(edited).enhance(contrast)

        st.subheader("الصورة النهائية:")
        st.image(edited, caption="بعد التعديل", use_column_width=True)
