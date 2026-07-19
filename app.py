import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz

# إعدادات الصفحة
st.set_page_config(page_title="ميمو الذكي", page_icon="🤖")
st.title("🤖 ميمو الذكي")

# إعداد مفتاح الـ API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ: تأكد من إعداد GOOGLE_API_KEY في صفحة Secrets.")
    st.stop()

# إدارة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أنا ميمو، كيف يمكنني مساعدتك؟"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اسأل ميمو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # معالجة الرد
    with st.chat_message("assistant"):
        cairo_tz = pytz.timezone('Africa/Cairo')
        now = datetime.now(cairo_tz)
        
        # ردود ذكية سريعة
        if "الساعه كام" in prompt or "الساعة كام" in prompt:
            response_text = f"الساعة الآن في مصر هي: {now.strftime('%I:%M %p')}"
        elif "النهارده ايه" in prompt or "التاريخ" in prompt:
            days_ar = {"Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
            day_name = days_ar.get(now.strftime('%A'), now.strftime('%A'))
            response_text = f"النهارده {day_name}، {now.strftime('%Y-%m-%d')}"
        else:
            # استخدام الذكاء الاصطناعي للأسئلة الأخرى
            try:
                response = model.generate_content(prompt)
                response_text = response.text
            except Exception as e:
                response_text = "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي."

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
