import streamlit as st
from datetime import datetime

# إعداد الواجهة
st.set_page_config(page_title="سيستم ميمو", layout="wide")

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
            # تحويل النص لـ lowercase عشان ميمو يفهم الأوامر بسهولة
            text = prompt.lower()
            
            if "الساعة" in text or "الوقت" in text:
                now = datetime.now().strftime("%I:%M %p")
                response = f"يا محمد، الوقت الآن هو {now} بتوقيت مصر."
            elif "كورة" in text or "ماتش" in text:
                response = "أنا جاهز يا بطل! أي فريق تحب نتابع أخبار أو مواعيد مبارياته؟"
            elif "يومك" in text or "كيف حالك" in text:
                response = "أنا بخير يا محمد، السيستم يعمل بكفاءة وأنا جاهز لتنظيم يومك ومذاكرتك!"
            else:
                response = "أهلاً يا محمد، أنا السيستم الخاص بك، كيف يمكنني مساعدتك في يومك اليوم؟"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- تبويب المهام ---
with tab2:
    st.subheader("قائمة المهام")
    st.write("السيستم الخاص بك جاهز لإضافة مهامك اليومية.")

# --- تبويب الأكواد ---
with tab3:
    st.subheader("مكتبة الأكواد")
    st.write("مساحة مخصصة لحفظ أكوادك البرمجية.")
