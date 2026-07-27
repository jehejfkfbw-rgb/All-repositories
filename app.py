import streamlit as st
import datetime
import requests
import time
from datetime import datetime as dt, timedelta

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="تطبيق ميمو - مواقيت الصلاة والأذان",
    page_icon="🕌",
    layout="wide"
)

# 2. تهيئة سجل البحث
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# --- تنسيق CSS للواجهة والعداد التنازلي ---
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .countdown-box {
        background: linear-gradient(135deg, #1e2130, #2a2e42);
        color: #00ffcc;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border: 1px solid #00ffcc;
        box-shadow: 0 4px 10px rgba(0, 255, 204, 0.2);
        margin-bottom: 15px;
    }
    .prayer-card {
        background-color: #1e2130;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #313549;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# دالة لجلب مواقيت الصلاة
@st.cache_data(ttl=3600)
def get_prayer_times(country="Egypt"):
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity?city=Cairo&country={country}&method=5"
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

# حساب الصلاة القادمة والوقت المتبقي لها
def get_next_prayer(prayer_times):
    now = dt.now()
    today_str = now.strftime("%Y-%m-%d")
    
    prayers = {
        "الفجر": prayer_times.get('Fajr'),
        "الظهر": prayer_times.get('Dhuhr'),
        "العصر": prayer_times.get('Asr'),
        "المغرب": prayer_times.get('Maghrib'),
        "العشاء": prayer_times.get('Isha')
    }
    
    for name, p_time in prayers.items():
        prayer_dt = dt.strptime(f"{today_str} {p_time}", "%Y-%m-%d %H:%M")
        if prayer_dt > now:
            return name, prayer_dt
            
    # إذا انتهت صلوات اليوم، فالصلاة القادمة هي فجر الغد
    tomorrow_str = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    fajr_tomorrow = dt.strptime(f"{tomorrow_str} {prayer_times.get('Fajr')}", "%Y-%m-%d %H:%M")
    return "الفجر", fajr_tomorrow


# ---------------- تقسيم الواجهة (يمين وشمال) ----------------
col_main, col_left = st.columns([2.5, 1.2])

# ==========================================
# العمود الأيسر (أعلى الشمال: الأذان والعداد + السجل)
# ==========================================
with col_left:
    st.markdown("### 🕌 مواقيت الصلاة والأذان")
    
    # اختيار الدولة
    country = st.selectbox("اختر الدولة لمعرفة الوقت:", ["مصر", "السعودية", "الإمارات"], index=0)
    country_code = "Egypt" if country == "مصر" else ("Saudi Arabia" if country == "السعودية" else "UAE")
    
    prayer_times = get_prayer_times(country_code)
    next_prayer_name, next_prayer_dt = get_next_prayer(prayer_times)
    
    # حساب المتبقي للصلاة القادمة
    now = dt.now()
    time_diff = next_prayer_dt - now
    total_seconds = int(time_diff.total_seconds())
    
    # عرض العداد التنازلي الرقمي (النزول حتى يصل 00:00:00)
    if total_seconds > 0:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        st.markdown(f"""
        <div class="countdown-box">
            ⏳ متبقي على أذان <b>{next_prayer_name}</b><br>
            <span style="font-size: 32px;">{timer_text}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # عند الوصول إلى 00:00:00 يشتغل الأذان فوراً
        st.markdown(f"""
        <div class="countdown-box" style="color: #ff4b4b; border-color: #ff4b4b;">
            🔔 حان الآن موعد أذان {next_prayer_name}! 00:00:00
        </div>
        """, unsafe_allow_html=True)
        st.audio("https://www.islamcan.com/audio/adhan/azan1.mp3", autoplay=True)

    # جدول مواقيت الصلاة
    st.markdown(f"""
    <div class="prayer-card">
        <b>⏰ الوقت الحالي:</b> {now.strftime("%I:%M:%S %p")}<br><hr style='margin:8px 0;'>
        <b>🌅 الفجر:</b> {prayer_times.get('Fajr')}<br>
        <b>☀️ الظهر:</b> {prayer_times.get('Dhuhr')}<br>
        <b>🌤️ العصر:</b> {prayer_times.get('Asr')}<br>
        <b>🌆 المغرب:</b> {prayer_times.get('Maghrib')}<br>
        <b>🌌 العشاء:</b> {prayer_times.get('Isha')}
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # 📜 قسم سجل البحث (أسفل الأذان)
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
# العمود الأيمن (المحتوى الرئيسي ووحدة الكتابة)
# ==========================================
with col_main:
    st.title("🤖 إنتاج - AI ميمو InnovaSoft")
    st.write("شات ذكي صوتي + توليد صور + محرر")
    
    st.subheader("🔎 البحث في التطبيق")
    search_query = st.text_input("ادخل كلمة للبحث:", key="main_search")
    if st.button("بحث 🔍"):
        if search_query.strip() != "":
            st.session_state.search_history.insert(0, search_query.strip())
            st.success(f"تم تسجيل البحث: {search_query}")
            st.rerun()

    st.write("---")

    # جهة الكتابة واسأل ميمو
    st.subheader("💬 اسأل ميمو")
    user_question = st.text_input("اكتب سؤالك هنا (مثال: مين صاحب الشركة؟):", key="ask_memo")

    if user_question:
        q_lower = user_question.lower()
        owner_keywords = ["مين صاحبك", "من صاحبك", "صاحب الشركة", "مين المطور", "who created", "who is the owner"]
        
        if any(keyword in q_lower for keyword in owner_keywords):
            st.success("🤖 **Memo:** This application was created and developed by Mohamed Adel Mohamed Ali.")
        else:
            st.info("🤖 **Memo:** أهلاً بك! أنا ميمو، يمكنك سؤالي عن مطور التطبيق أو مواقيت الصلاة.")

    st.write("---")

    # أقسام الخدمة
    st.subheader(":اختر القسم")
    section = st.radio("", ["الشات الصوتي الذكي 💬", "توليد الصور بالذكاء الاصطناعي 🎨", "محرر الصور والفلاتر ✏️"])


# إعادة تحديث الصفحة كل ثانية ليعمل العداد التنازلي بشكل حي ومباشر
time.sleep(1)
st.rerun()
