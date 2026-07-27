import random
import smtplib
from email.message import EmailMessage
import streamlit as st

# بيانات البريد المرسل وتطبيق جوجل (كلمة المرور الـ 16 حرف بتاعتك)
SENDER_EMAIL = "ajakdjrjej@gmail.com"  # الإيميل بتاعك اللي انشأت عليه الكلمة
SENDER_PASSWORD = "eelaangubuzhdwmj"

# دالة إرسال رمز التحقق
def send_otp_email(receiver_email, otp_code):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'رمز التحقق الخاص بك لتطبيق ميمو (Memo)'
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg.set_content(f"أهلاً بك يا فنان!\n\nرمز التحقق الخاص بك هو: {otp_code}\n\nلا تشارك هذا الرمز مع أي شخص.")

        # الاتصال بسيرفر جيمايل وإرسال البريد
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return str(e)

# واجهة تطبيق Streamlit
st.title("تطبيق ميمو - Memo AI 🤖")
st.write("أهلاً بك في نظام تسجيل الدخول الآمن.")

# حالة الجلسة لتخزين الرمز
if "otp" not in st.session_state:
    st.session_state.otp = None
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

user_email = st.text_input("أدخل بريدك الإلكتروني:")

if st.button("إرسال رمز التحقق"):
    if user_email:
        # توليد رمز عشوائي من 4 أرقام
        st.session_state.otp = str(random.randint(1000, 9999))
        
        # محاولة إرسال الإيميل
        result = send_otp_email(user_email, st.session_state.otp)
        
        if result == True:
            st.session_state.email_sent = True
            st.success("تم إرسال رمز التحقق إلى بريدك الإلكتروني بنجاح! تفقد صندوق الوارد.")
        else:
            st.error(f"حدث خطأ أثناء الإرسال: {result}")
    else:
        st.warning("الرجاء إدخال البريد الإلكتروني أولاً.")

# تحقق من الرمز المدخل
if st.session_state.email_sent:
    entered_otp = st.text_input("أدخل رمز التحقق المكون من 4 أرقام:")
    
    if st.button("تأكيد الرمز"):
        if entered_otp == st.session_state.otp:
            st.success("تم تسجيل الدخول بنجاح يا فنان! أهلاً بك في تطبيق ميمو.")
        else:
            st.error("رمز التحقق غير صحيح، حاول مرة أخرى.")
