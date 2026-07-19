import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz

# إعدادات الصفحة
st.set_page_config(page_title="ميمو الذكي", page_icon="🤖")

st.title("🤖 ميمو الذكي")

# قراءة المفتاح من الـ Secrets بأمان
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام نموذج gemini-1.5-flash الأحدث والأسرع
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("تأكد من كتابة المفتاح بشكل صحيح في الـ Secrets باسم GOOGLE_API_KEY")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    # رسالة ترحيبية أولية مخزنة بشكل صحيح
    st.session_state.messages = [{"role": "assistant", "content": "أنا ميمو، كيف يمكنني مساعدتك؟"}]

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة المستخدم
if prompt := st.chat_input("اسأل ميمو أي شيء..."):
    # عرض رسالة المستخدم وحفظها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # إذا سأل عن الوقت أو التاريخ، نجيبه مباشرة بدقة مصر
        cairo_tz = pytz.timezone('Africa/Cairo')
        now = datetime.now(cairo_tz)
        
        if "الساعه كام" in prompt or "الساعة كام" in prompt or "الوقت" in prompt:
            full_response = f"الساعة الآن في مصر هي: {now.strftime('%I:%M %p')}"
            message_placeholder.markdown(full_response)
        elif "النهارده ايه" in prompt or "تاريخ كام" in prompt or "التاريخ" in prompt:
            days_ar = {"Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
            day_name = days_ar.get(now.strftime('%A'), now.strftime('%A'))
            full_response = f"النهارده هو يوم {day_name}، وتاريخ اليوم هو: {now.strftime('%Y-%m-%d')}"
            message_placeholder.markdown(full_response)
        else:
            # إذا كان سؤالاً عاماً، نرسله لـ Gemini
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = "عذراً، واجهت مشكلة في الاتصال بالذكاء الاصطناعي. تأكد من صلاحية مفتاح الـ API الخاص بك."
                message_placeholder.markdown(full_response)
                st.small(f"تفاصيل الخطأ لتبحث عنها: {e}")

    # حفظ رد ميمو في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": full_response})
