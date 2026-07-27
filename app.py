import requests
import streamlit as st

# إعدادات صفحة Streamlit وتصميم الواجهة
st.set_page_config(
    page_title="تطبيق ميمو - Memo AI",
    page_icon="🤖",
    layout="centered"
)

# بيانات بوت التليجرام الخاص بك لاستقبال الإشعارات والرسائل
TELEGRAM_BOT_TOKEN = "حط_التوكن_بتاع_البوت_هنا"  # استبدل هذه الكلمة بتوكن البوت الخاص بك
TELEGRAM_CHAT_ID = "8672781771"  # الـ Chat ID الخاص بك على تليجرام

# دالة إرسال التنبيهات والرسائل إلى تليجرام
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        pass

# إرسال تنبيه فور فتح التطبيق لأول مرة في الجلسة
if "app_opened_alert" not in st.session_state:
    send_telegram_alert("🚨 *تنبيه جديد:* قام شخص ما بفتح تطبيق ميمو (Memo AI) حالا!")
    st.session_state.app_opened_alert = True

# عنوان التطبيق والمميزات البصرية
st.title("تطبيق ميمو - Memo AI 🤖")
st.markdown("---")
st.write("أهلاً بك يا فنان! أنا مساعدك الذكي المطور. اكتب رسالتك وسأقوم بالرد عليك وإرسال نسخة من النشاط مباشرة إلى تليجرام.")

# الشريط الجانبي (Sidebar) للمميزات الإضافية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    st.write("خصائص تطبيق ميمو الذكي:")
    st.info("• شات تفاعلي مباشر.\n• إشعارات فورية على تليجرام.\n• حفظ محادثات الجلسة تلقائياً.")
    
    if st.button("🗑️ مسح محادثة الشات"):
        st.session_state.messages = []
        st.rerun()

# تهيئة حافظة رسائل الشات في الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً يا فنان! أنا ميمو معاك، قول لي أقدر أساعدك بايه النهاردة؟"}
    ]

# عرض رسائل الشات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق ادخال رسائل المستخدم (Chat Input)
if user_input := st.chat_input("اكتب رسالتك هنا يا فنان..."):
    # إضافة رسالة المستخدم وعرضها
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # إرسال رسالة المستخدم تلقائياً إلى تليجرام لكي تتابع كل كبيرة وصغيرة
    send_telegram_alert(f"💬 *رسالة جديدة من المستخدم:*\n{user_input}")

    # محاكاة رد الذكاء الاصطناعي (Memo AI)
    bot_response = f"يا أهلاً بيك يا فنان! لقد استقبلت رسالتك بنجاح وعال عالٍ: '{user_input}'. هل تحتاج لأي مساعدة أخرى في الكود أو البرمجة؟"

    # إضافة رد المساعد وعرضه
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
