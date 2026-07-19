import streamlit as st
from datetime import date

# 1. إعدادات الصفحة
st.set_page_config(page_title="ميمو", page_icon="🤖")

# 2. إخفاء العلامات
hide_style = "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🤖 أهلاً بك في ميمو")

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال رسالة جديدة
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. رد ميمو الذكي
    response = "أنا ميمو، كيف يمكنني مساعدتك؟"
    
    if "النهارده" in prompt or "التاريخ" in prompt:
        response = f"النهارده {date.today().strftime('%A %Y/%m/%d')} يا محمد!"
    elif "اسمك" in prompt:
        response = "اسمي ميمو، وأنا هنا عشان أساعدك في تعلم البرمجة."
    elif "حالك" in prompt:
        response = "أنا بخير جداً، خصوصاً لما بشوفك بتطور الكود بنفسك!"

    # إضافة رد ميمو للذاكرة
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
