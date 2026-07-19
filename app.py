import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="ميمو", page_icon="🤖")

# إخفاء العلامة المائية والـ Menu
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}, footer {visibility: hidden;}, header {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# لوحة التحكم الجانبية
with st.sidebar:
    st.title("🤖 لوحة تحكم ميمو")
    option = st.selectbox("اختار المهمة:", ["دردشة", "إعدادات"])

# محتوى الصفحة الرئيسي
st.title("أهلاً بك في ميمو")

if option == "دردشة":
    st.write("أنا ميمو، كيف يمكنني مساعدتك اليوم؟")
    
    # استخدام session_state عشان الذاكرة متتمسحش
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل القديمة
    for message in st.session_state.messages:
        with st.chat_message("user"):
            st.markdown(message)

    # استقبال رسالة جديدة
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        st.session_state.messages.append(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # رد ميمو (هنا تقدر تغير الردود براحتك)
        response = f"أهلاً يا محمد، لقد قلت لي: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)

elif option == "إعدادات":
    st.write("إعدادات ميمو قيد التطوير.")
