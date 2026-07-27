import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="تطبيق ميمو للذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide"
)

# 2. تهيئة سجل البحث في الـ Session State
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# --- تنسيق الواجهة لتكون القائمة الجانبية على اليمين ودعم اللغة العربية ---
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    [data-testid="stSidebar"] {
        right: 0;
        left: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- القائمة الجانبية (على اليمين) ----------------
with st.sidebar:
    st.header("🔍 البحث والسجل")
    
    # مربع ادخال البحث
    search_query = st.text_input("ابحث عن خدمة أو كلمة:")
    
    if st.button("بحث"):
        if search_query.strip() != "":
            st.session_state.search_history.insert(0, search_query.strip())
            st.success(f"تم البحث عن: {search_query}")

    st.write("---")
    st.subheader("📜 سجل البحث:")
    
    if st.session_state.search_history:
        for item in st.session_state.search_history:
            st.markdown(f"• **{item}**")
            
        if st.button("تفريغ السجل 🗑️"):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.write("لا يوجد بحث سابق حتى الآن.")

# ---------------- محتوى الصفحة الرئيسي ----------------
st.title("🤖 مرحباً بك! أنا الذكاء الاصطناعي ميمو (Memo)")
st.subheader("مساعدك الذكي ودليلك لأفضل أدوات الذكاء الاصطناعي")

st.markdown("""
أهلاً بك في موقعنا! أنا **ميمو**، المساعد الذكي الخاص بالموقع. يمكنك استخدام الخانة بالأسفل لسؤالي عن أي شيء أو الاستفسار عن المطور، أو تصفح أفضل خدمات الذكاء الاصطناعي المجمعة لك بالأسفل.
""")

st.write("---")

# ---------------- قسم اسأل ميمو ----------------
st.subheader("💬 اسأل ميمو")
user_question = st.text_input("اكتب سؤالك هنا (مثال: مين صاحبك؟ / Who created you?):")

if user_question:
    q_lower = user_question.lower()
    # الكلمات المفتاحية للتعرف على السؤال عن صاحب التطبيق أو الشركة
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

# نتائج البحث
if search_query:
    st.info(f"🔎 نتائج البحث عن: **{search_query}**")

# تبويبات الخدمات باللغة العربية
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 أدوات النصوص والمحاثة", 
    "🎨 إنشاء الصور والفنون", 
    "💻 البرمجة والتطوير", 
    "🎙️ الصوت والموسيقى"
])

with tab1:
    st.header("توليد النصوص والمساعدات الذكية")
    st.write("أفضل أدوات الذكاء الاصطناعي للكتابة، البحث، وتوليد الأفكار.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("شات جي بي تي (ChatGPT)")
        st.markdown("الأداة الأشهر عالمياً للمحادثة، كتابة المقالات، وتلخيص النصوص.")
        st.link_button("زيارة ChatGPT", "https://chatgpt.com")
    with col2:
        st.subheader("جوجل جيميناي (Gemini)")
        st.markdown("ذكاء جوجل المتطور المرتبط بالبحث المباشر ومعالجة البيانات.")
        st.link_button("زيارة Gemini", "https://gemini.google.com")

with tab2:
    st.header("إنشاء الصور وتوليد الفنون")
    st.write("حول أفكارك وتخيلاتك إلى صور وفنون فائقة الدقة.")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("ميدجيرني (Midjourney)")
        st.markdown("أفضل أداة لتوليد صور سينمائية وفنية عالية الجودة.")
        st.link_button("زيارة Midjourney", "https://www.midjourney.com")
    with col4:
        st.subheader("دالي 3 (DALL-E 3)")
        st.markdown("نموذج شركة OpenAI الذكي لفهم الوصف الدقيق وإنشاء الصور.")
        st.link_button("زيارة DALL-E 3", "https://openai.com/dall-e-3")

with tab3:
    st.header("البرمجة وتطوير البرمجيات")
    st.write("أدوات مساعدة للمبرمجين لكتابة الكود وتصحيح الأخطاء بسرعة.")
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("جيت هاب كوبايلوت (GitHub Copilot)")
        st.markdown("مساعد المبرمجين الذكي الذي يكمل الأكواد داخل محرر الأكواد.")
        st.link_button("زيارة GitHub Copilot", "https://github.com/features/copilot")
    with col6:
        st.subheader("كلود (Claude)")
        st.markdown("نموذج متقدم يمتاز بدقة عالية في فهم البرمجيات المنطقية والأكواد الطويلة.")
        st.link_button("زيارة Claude", "https://claude.ai")

with tab4:
    st.header("توليد الصوت والموسيقى")
    st.write("تحويل النصوص إلى أصوات بشرية واضحة وإنشاء مقاطع موسيقية.")
    col7, col8 = st.columns(2)
    with col7:
        st.subheader("إليفين لابس (ElevenLabs)")
        st.markdown("أفضل أداة لتوليد التعليق الصوتي والتعرف على الأصوات بدقة متناهية.")
        st.link_button("زيارة ElevenLabs", "https://elevenlabs.io")
    with col8:
        st.subheader("سونو (Suno AI)")
        st.markdown("إنشاء أغاني كاملة مع الموسيقى والكلمات والألحان من الوصف النصي.")
        st.link_button("زيارة Suno", "https://suno.com")

st.write("---")
st.caption("🤖 تطبيق ميمو الذكي © 2026 - تم التطوير بواسطة محمد عادل محمد علي")
