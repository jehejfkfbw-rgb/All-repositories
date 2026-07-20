import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ميمو - النسخة الذكية", page_icon="🤖", layout="centered")

# --- واجهة المستخدم ---
st.title("🤖 ميمو الذكي")
st.markdown("---")
# تعديل النص ليشمل التاريخ المحدد
st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>قيد التطوير من المطور محمد عادل</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>الحدث المرتقب: 20 أغسطس 2026</p>", unsafe_allow_html=True)
st.markdown("---")

# --- إدارة الحالة (سجل المحادثة) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً يا محمد! أنا ميمو معك، كيف يمكنني مساعدتك اليوم؟"}
    ]

# --- عرض تاريخ المحادثة ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وظيفة الردود الذكية ---
def get_memo_response(user_text):
    text = user_text.lower()
    if any(word in text for word in ["ازيك", "عامل ايه", "أهلاً", "مرحبا"]):
        return "الحمد لله يا محمد! أنا ميمو، ومستعد معك لكل جديد في يوم 20 أغسطس."
    elif "اسمك" in text:
        return "أنا ميمو، مساعدك الشخصي، نجهز لكل ما هو قادم في 20/08/2026."
    else:
        return f"يا هلا يا محمد! أنا هنا وجاهز، ننتظر سوياً يوم 20 أغسطس 2026."

# --- معالجة الرسائل ---
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = get_memo_response(prompt)
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("أقسام ميمو")
    st.success("✅ الدردشة الذكية (مفعل)")
    st.divider()
    st.write("🛠️ تحليل البيانات (قيد التطوير)")
    st.write("🛠️ المساعد البرمجي (قيد التطوير)")
    st.divider()
    st.info("تطوير: محمد عادل - 20/08/2026")
    
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
