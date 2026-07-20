import streamlit as st
from datetime import datetime

# إعداد الواجهة
st.set_page_config(page_title="سيستم ميمو الخاص", layout="wide")

st.title("🤖 ميمو: السيستم الخاص بمحمد عادل")

# التبويبات
tab1, tab2, tab3 = st.tabs(["💬 ميمو الذكي", "✅ المهام", "💻 مكتبة الأكواد"])

# --- تبويب ميمو الذكي ---
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
            # منطق السيستم الخاص
            if "الساعة" in prompt or "الوقت" in prompt:
                now = datetime.now().strftime("%I:%M %p")
                response = f"يا محمد، الوقت الآن هو {now} بتوقيت مصر."
            elif "كورة" in prompt or "ماتش" in prompt:
                response = "أنا جاهز! أي فريق تحب نتابع نتائجه اليوم؟"
            else:
                response = "أهلاً يا محمد، أنا السيستم الخاص بك، كيف يمكنني تنظيم يومك اليوم؟"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- تبويب المهام والأكواد ---
with tab2:
    st.subheader("قائمة المهام")
    st.write("السيستم الخاص بك يعمل الآن!")

with tab3:
    st.subheader("مكتبة الأكواد")
    st.write("مساحة مخصصة لك فقط.")
