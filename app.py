import streamlit as st
import time

# 1. إعدادات الصفحة وشكلها
st.set_page_config(page_title="Memo AI", page_icon="🤖", layout="centered")

# 2. تصميم الخلفية المخصصة (أزرق غامق) وتعديل الألوان
st.markdown("""
    <style>
    /* تغيير خلفية الصفحة بالكامل */
    .stApp {
        background-color: #0B192C;
        color: #F5F7F8;
    }
    /* تعديل شكل صندوق الكتابة */
    .stTextInput input {
        background-color: #1E3E62;
        color: white;
        border-radius: 10px;
        border: 1px solid #008DDA;
    }
    /* تعديل العناوين */
    h1, h3 {
        color: #008DDA !important;
        text-align: center;
    }
    /* شكل رسايل الشات */
    .user-msg {
        background-color: #1E3E62;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-msg {
        background-color: #008DDA;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: white;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.title("🤖 ميمو - Memo AI")
st.subheader("مرحباً بك يا محمد! أنا ميمو، مساعدك الذكي.")

# 3. إعداد ذاكرة الشات لتخزين المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة إذا وجدت
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>أنت:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><b>ميمو:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# 4. استقبال سؤال المستخدم
user_input = st.chat_input("اكتب سؤالك هنا يا محمد...")

if user_input:
    # عرض رسالة المستخدم فوراً
    st.markdown(f'<div class="user-msg"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # ردود ذكية وتلقائية من ميمو للاختبار
    lowered_input = user_input.lower()
    if "أهلاً" in lowered_input or "اهلا" in lowered_input or "سلام" in lowered_input:
        bot_response = "أهلاً بك يا محمد! منور الشات. أنا ميمو وجاهز لمساعدتك في أي وقت! 🚀"
    elif "اسمك" in lowered_input:
        bot_response = "اسمي ميمو (Memo AI)! البوت الخاص بك اللي أنت برمجته بنفسك وبايثون المرة دي شغال تمام! 😎"
    elif "كورة" in lowered_input or "ماتش" in lowered_input:
        bot_response = "الماتشات دايماً حماسية يا محمد! تفتكر مين اللي هيكسب؟ ⚽"
    elif "python" in lowered_input or "بايثون" in lowered_input:
        bot_response = "بايثون هي لغتي الأم! لغة قوية وسهلة، وأنت كودتني بيها بنجاح اليوم. 🐍"
    else:
        bot_response = f"أنا سمعتك كويس يا محمد! سؤالك هو: '{user_input}'. أنا لسه بوت تجريبي وبطور من نفسي، قولي حابب نبرمج إيه جديد مع بعض؟"
    
    # تأثير الكتابة (الذكاء الاصطناعي)
    with st.spinner("ميمو يفكر..."):
        time.sleep(1)
        
    # عرض رد ميمو وحفظه
    st.markdown(f'<div class="bot-msg"><b>ميمو:</b> {bot_response}</div>', unsafe_allow_html=True)
   
