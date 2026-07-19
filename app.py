import streamlit as st
import google.generativeai as genai
import sqlite3

# --- 1. إعدادات قاعدة البيانات ---
conn = sqlite3.connect('mimo_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat_history
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_message TEXT, 
              mimo_response TEXT)''')
conn.commit()

def save_to_db(user_input, response):
    c.execute("INSERT INTO chat_history (user_message, mimo_response) VALUES (?, ?)", (user_input, response))
    conn.commit()

# --- 2. إعدادات واجهة التطبيق ---
st.set_page_config(page_title="ميمو - النسخة الكاملة", page_icon="🤖")
st.title("🤖 ميمو: المساعد الذكي مع الذاكرة")

# القائمة الجانبية للمفتاح
with st.sidebar:
    api_key = st.text_input("أدخل مفتاح الـ API هنا:", type="password")
    st.info("قم بإنشاء المفتاح من Google AI Studio.")

# تهيئة الذكاء الاصطناعي
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# --- 3. إدارة المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة من الذاكرة (Session State)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة المستخدم
if prompt := st.chat_input("تحدث مع ميمو..."):
    if not api_key:
        st.error("من فضلك أدخل مفتاح الـ API في القائمة الجانبية!")
        st.stop()

    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد ميمو
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            reply = response.text
            st.markdown(reply)
            
            # حفظ المحادثة في قاعدة البيانات
            save_to_db(prompt, reply)
            
            # حفظ في ذاكرة الجلسة
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {e}")
