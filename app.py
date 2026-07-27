import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse
from gtts import gTTS
import os
from datetime import datetime
import pytz
import requests

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

# دالة جلب مواقيت الصلاة الحقيقية من API
def get_prayer_times(country):
    # خريطة لربط اسم الدولة بالمدينة المطلوبة للـ API
    cities = {
        'مصر': 'Cairo', 'السعودية': 'Riyadh', 'الإمارات': 'Dubai',
        'الكويت': 'Kuwait', 'قطر': 'Doha', 'البحرين': 'Manama',
        'عمان': 'Muscat', 'الأردن': 'Amman', 'فلسطين': 'Jerusalem',
        'لبنان': 'Beirut', 'سوريا': 'Damascus', 'العراق': 'Baghdad',
        'اليمن': 'Sana a', 'السودان': 'Khartoum', 'ليبيا': 'Tripoli',
        'تونس': 'Tunis', 'الجزائر': 'Algiers', 'المغرب': 'Rabat',
        'موريتانيا': 'Nouakchott', 'أمريكا': 'New York'
    }
    city = cities.get(country, 'Cairo')
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=5"
        response = requests.get(url)
        data = response.json()
        if data['code'] == 200:
            return data['data']['timings']
    except:
        pass
    return None

# ==========================================
# 2. القائمة الجانبية (Sidebar - التوقيت والأذان التلقائي)
# ==========================================
st.sidebar.title("🤖 ميمو AI - إنتاج InnovaSoft")
st.sidebar.write("شات ذكي صوتي + توليد صور + محرر")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("اختر القسم:", [
    "💬 الشات الصوتي الذكي", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "✏️ محرر الصور والفلاتر"
])

# قسم مواقيت الصلاة والأذان التلقائي
st.sidebar.markdown("---")
st.sidebar.subheader("🕌 مواقيت الصلاة والأذان التلقائي")
selected_country_sidebar = st.sidebar.selectbox("اختر الدولة:", [
    'مصر', 'السعودية', 'الإمارات', 'الكويت', 'قطر', 'البحرين', 'عمان', 
    'الأردن', 'فلسطين', 'لبنان', 'سوريا', 'العراق', 'اليمن', 'السودان', 
    'ليبيا', 'تونس', 'الجزائر', 'المغرب', 'موريتانيا', 'أمريكا'
])

# جلب المواقيت اليومية
timings = get_prayer_times(selected_country_sidebar)
if timings:
    st.sidebar.write(f"🌅 **الفجر:** {timings.get('Fajr')}")
    st.sidebar.write(f"☀️ **الشروق:** {timings.get('Sunrise')}")
    st.sidebar.write(f"عب **الظهر:** {timings.get('Dhuhr')}")
    st.sidebar.write(f"🌤️ **العصر:** {timings.get('Asr')}")
    st.sidebar.write(f"🌇 **المغرب:** {timings.get('Maghrib')}")
    st.sidebar.write(f"🌙 **العشاء:** {timings.get('Isha')}")

# تشغيل صوت الأذان (الله أكبر) يدوياً أو تلقائياً عند الحاجة
st.sidebar.markdown("---")
st.sidebar.markdown("🔊 **تشغيل صوت الأذان:**")
adhan_audio_url = "https://www.islamcan.com/audio/adhan/azan01.mp3"
st.sidebar.audio(adhan_audio_url, format="audio/mp3")

# ==========================================
# 3. قسم الشات الصوتي الذكي (مع حفظ الذاكرة)
# ==========================================
if app_mode == "💬 الشات الصوتي الذكي":
    st.title("💬 ميمو - الشات الصوتي")
    st.write("اسأل عن مواقيت الصلاة، الوقت، أو اسألني عن صاحب الشركة، وسأحفظ محادثتنا بالكامل!")
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("🗑️ مسح الذاكرة وبدء محادثة جديدة"):
        st.session_state.chat_history = []
        st.rerun()

    for idx, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "audio" in message:
                st.audio(message["audio"], format="audio/mp3")

    if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
        lower_prompt = user_prompt.lower()
        
        # الرد على مواقيت الصلاة بدقة
        if "صلاة" in user_prompt or "أذان" in user_prompt or "مواقيت" in user_prompt:
            found_country = 'مصر'
            timezones_dict = {
                'مصر': 'Africa/Cairo', 'السعودية': 'Asia/Riyadh', 'الإمارات': 'Asia/Dubai',
                'الكويت': 'Asia/Kuwait', 'قطر': 'Asia/Qatar', 'البحرين': 'Asia/Bahrain',
                'عمان': 'Asia/Muscat', 'الأردن': 'Asia/Amman', 'فلسطين': 'Asia/Gaza',
                'لبنان': 'Asia/Beirut', 'سوريا': 'Asia/Damascus', 'العراق': 'Asia/Baghdad',
                'اليمن': 'Asia/Aden', 'السودان': 'Africa/Khartoum', 'ليبيا': 'Africa/Tripoli',
                'تونس': 'Africa/Tunis', 'الجزائر': 'Africa/Algiers', 'المغرب': 'Africa/Casablanca',
                'موريتانيا': 'Africa/Nouakchott', 'أمريكا': 'America/New_York'
            }
            for country in timezones_dict.keys():
                if country in user_prompt:
                    found_country = country
                    break
            
            p_times = get_prayer_times(found_country)
            if p_times:
                bot_reply = f"مواقيت الصلاة اليوم في {found_country}:\n- الفجر: {p_times.get('Fajr')}\n- الظهر: {p_times.get('Dhuhr')}\n- العصر: {p_times.get('Asr')}\n- المغرب: {p_times.get('Maghrib')}\n- العشاء: {p_times.get('Isha')}"
            else:
                bot_reply = "عذراً، لم أستطيع جلب مواقيت الصلاة الآن."

        elif "الساعة" in user_prompt or "الوقت" in user_prompt or "كام الساعه" in lower_prompt:
            bot_reply = "راجع الشريط الجانبي (Sidebar) لمعرفة الوقت الدقيق ومواقيت الصلاة لكل الدول مباشرة!"
            
        elif "صاحب الشركة" in user_prompt or "مين صاحبك" in user_prompt or "مؤسس" in user_prompt or "صاحب شركه" in user_prompt:
            bot_reply = "صاحب ومؤسس شركة InnovaSoft هو المبرمج محمد!"
            
        elif "اسمك" in user_prompt or "اسمك ايه" in user_prompt or "من أنت" in user_prompt or "انت مين" in user_prompt or "صنعك" in user_prompt or "شركتك" in user_prompt:
            bot_reply = "أنا اسمي ميمو، وتم تطويري وبرمجتي بواسطة شركة **InnovaSoft**!"
            
        else:
            with st.spinner("جاري التفكير وتوليد الصوت..."):
                try:
                    messages_list = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                    messages_list.append({"role": "user", "content": user_prompt})
                    
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        messages=messages_list,
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
