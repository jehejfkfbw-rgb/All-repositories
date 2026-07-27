import streamlit as st
import datetime
import requests
from datetime import datetime as dt

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="تطبيق ميمو للذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide"
)

# 2. تهيئة سجل البحث في Session State
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# --- تنسيق الواجهة ودعم اتجاه النص ---
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .prayer-card {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #313549;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# دالة لجلب مواقيت الصلاة من API
@st.cache_data(ttl=3600)
def get_prayer_times():
    try:
        url = "https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5"
        res = requests.get(url).json()
        return res["data"]["timings"]
    except:
        return {
            "Fajr": "04:30",
            "Dhuhr": "12:00",
            "Asr": "15:30",
            "Maghrib": "18:45",
            "Isha": "20:15"
        }

prayer_times = get_prayer_times()

# ---------------- تقسيم الواجهة إلى عمودين (يمين وشمال) ----------------
col_main, col_left = st.columns([2.5, 1.2])

# ==========================================
# العمود الأيسر (أعلى الشمال: الأذان والمواقيت + أسفله: سجل البحث)
# ==========================================
with col_left:
    # 🕋 قسم مواقيت الصلاة والأذان
    st.markdown("### 🕌 مواقيت الصلاة والأذان")
    
    with st.container():
        now = dt.now().strftime("%H:%M")
        
        # عرض مواقيت الصلاة
        st.markdown(f"""
        <div class="prayer-card">
            <b>⏱️ الوقت الحالي:</b> {now}<br><hr style='margin:8px 0;'>
            <b>🌅 الفجر:</b> {prayer_times.get('Fajr')}<br>
            <b>☀️ الظهر:</b> {prayer_times.get('Dhuhr')}<br>
            <b>🌤️ العصر:</b> {prayer_times.get('Asr')}<br>
            <b>🌆 المغرب:</b> {prayer_times.get('Maghrib')}<br>
            <b>🌌 العشاء:</b> {prayer_times.get('Isha')}
        </div>
        """, unsafe_allow_html=True)

        # التحقق من ميعاد الأذان وتشغيل الصوت عند المطابقة
        current_time_short = dt.now().strftime("%H:%M")
        prayers_list = {
            "الفجر": prayer_times.get('Fajr'),
            "الظهر": prayer_times.get('Dhuhr'),
            "العصر": prayer_times.get('Asr'),
            "المغرب": prayer_times.get('Maghrib'),
            "العشاء": prayer_times.get('Isha')
        }

        azan_triggered = False
        for name, p_time in prayers_list.items():
            if current_time_short == p_time:
                st.success(f"🔔 حان الآن موعد أذان صلاة {name}!")
                # صوت الأذان (الله أكبر)
                st.audio("https://www.islamcan.com/audio/adhan/azan1.mp3", autoplay=True)
                azan_triggered = True
                break
        
        if not azan_triggered:
            st.info("⌛ الأذان يعمل تلقائياً فور دخول وقت الصلاة.")

    st.write("---")

    # 📜 قسم سجل البحث (تحت قسم الأذان مباشرة في الشمال)
    st.subheader("📜 سجل البحث")
    
    if st.session_state.search_history:
        for idx, item in enumerate(st.session_state.search_history):
            st.markdown(f"{idx+1}. **{item}**")
            
        if st.button("تفريغ السجل 🗑️"):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.caption("لا يوجد بحث سابق حتى الآن.")


# ==========================================
# العمود الأيمن (المحتوى الرئيسي ووحدة الكتابة والأسئلة)
# ==========================================
with col_main:
    st.title("🤖 تطبيق ميمو للذكاء الاصطناعي")
    st.write("مساعدك الذكي للتصفح والاستفسار والأدوات البرمجية.")
    
    # 🔍 مربع البحث الرئيسي
    st.subheader("🔎 مربع البحث")
    search_query = st.text_input("ابحث عن خدمة أو كلمة داخل التطبيق:", key="main_search")
    if st.button("بحث 🔍"):
        if search_query.strip() != "":
            st.session_state.search_history.insert(0, search_query.strip())
            st.success(f"تمت إضافة '{search_query}' إلى السجل!")
            st.rerun()

    st.write("---")

    # 💬 جهة الكتابة واسأل ميمو
    st.subheader("✍️ جهة الكتابة واسأل ميمو")
    user_question = st.text_input("اكتب سؤالك هنا (مثال: مين صاحبك؟ / Who created you?):", key="ask_memo")

    if user_question:
        q_lower = user_question.lower()
        owner_keywords = [
            "مين صاحبك", "من صاحبك", "مين صاحب الشركة", "صاحب الشركة", 
            "مين عاملك", "من عملك", "مين المطور", "من المطور", "صاحبك", "مين المالك",
            "who created", "who made", "who is the owner", "creator", "developer", "owner"
        ]
        
        if any(keyword in q_lower for keyword in owner_keywords):
            st.success("🤖 **Memo:** This application was created and developed by Mohamed Adel Mohamed Ali.")
        else:
            st.info("🤖 **Memo:** أهلاً بك! أنا ميمو، يمكنك سؤالي عن مطور التطبيق أو البحث عن الأدوات بالأسفل.")

    st.write("---")

    # 📑 تبويبات الخدمات
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 أدوات النصوص", 
        "🎨 إنشاء الصور", 
        "💻 البرمجة والتطوير", 
        "🎙️ الصوت والموسيقى"
    ])

    with tab1:
        st.markdown("#### أفضل أدوات الذكاء الاصطناعي للكتابة والمحادثة")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**ChatGPT**")
            st.link_button("زيارة ChatGPT", "https://chatgpt.com")
        with col2:
            st.markdown("**Google Gemini**")
            st.link_button("زيارة Gemini", "https://gemini.google.com")

    with tab2:
        st.markdown("#### أدوات توليد الصور والتصاميم")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**Midjourney**")
            st.link_button("زيارة Midjourney", "https://www.midjourney.com")
        with col4:
            st.markdown("**DALL-E 3**")
            st.link_button("زيارة DALL-E 3", "https://openai.com/dall-e-3")

    with tab3:
        st.markdown("#### أدوات البرمجة وتطوير المواقع")
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("**GitHub Copilot**")
            st.link_button("زيارة Copilot", "https://github.com/features/copilot")
        with col6:
            st.markdown("**Claude AI**")
            st.link_button("زيارة Claude", "https://claude.ai")

    with tab4:
        st.markdown("#### أدوات توليد الصوت والأغاني")
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("**ElevenLabs**")
            st.link_button("زيارة ElevenLabs", "https://elevenlabs.io")
        with col8:
            st.markdown("**Suno AI**")
            st.link_button("زيارة Suno", "https://suno.com")

    st.write("---")
    st.caption("🤖 تطبيق ميمو الذكي © 2026 - تم التطوير بواسطة محمد عادل محمد علي")
