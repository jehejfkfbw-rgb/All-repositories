import streamlit as st
from datetime import datetime

# إعداد الواجهة
st.set_page_config(page_title="ميمو سيستم", layout="wide")

st.title("🤖 ميمو: السيستم الذكي")

# إنشاء التبويبات
tab1, tab2, tab3 = st.tabs(["💬 ميمو الذكي", "✅ المهام", "💻 مكتبة الأكواد"])

# --- تبويب ميمو الذكي (الرئيسي) ---
with tab1:
    st.subheader("مساعدك الشخصي")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("تحدث مع ميمو..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            text = prompt.lower()
            if "الساعة" in text or "الوقت" in text:
                now = datetime.now().strftime("%I:%M %p")
                response = f"الوقت الآن هو {now} بتوقيت مصر."
            else:
                response = "أهلاً بك! أنا ميمو، كيف يمكنني مساعدتك اليوم؟"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- تبويب المهام (قيد التطوير) ---
with tab2:
    st.subheader("قائمة المهام")
    st.info("⚠️ هذا القسم قيد التطوير حالياً، انتظر التحديثات القادمة!")

# --- تبويب الأكواد (قيد التطوير) ---
with tab3:
    st.subheader("مكتبة الأكواد")
    st.warning("🚧 هذا القسم قيد التطوير حالياً، ترقبوا الإضافات قريباً!")
