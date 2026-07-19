import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="ميمو", page_icon="🤖")

# 2. كود إخفاء العلامة المائية والـ Menu
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# 3. محتوى لوحة التحكم الجانبية
with st.sidebar:
    st.title("🤖 لوحة تحكم ميمو")
    st.write("أهلاً بك في ميمو المطور.")
    option = st.selectbox("اختار المهمة:", ["دردشة", "إعدادات"])

# 4. محتوى الصفحة الرئيسي
st.title("أهلاً بك في ميمو")

if option == "دردشة":
    st.write("أنا ميمو، كيف يمكنني مساعدتك اليوم؟")
    user_input = st.text_input("اكتب رسالتك هنا:")
    if user_input:
        st.write(f"ميمو يرد: لقد استلمت رسالتك: {user_input}")

elif option == "إعدادات":
    st.write("هنا يمكنك تغيير إعدادات ميمو لاحقاً.")
