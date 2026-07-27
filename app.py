import smtplib
import streamlit as st

# واجهة تطبيق Streamlit
st.title("تطبيق ميمو - Memo AI 🤖")
st.write("أهلاً بك، سجل دخولك ببريدك الإلكتروني وكلمة المرور.")

user_email = st.text_input("أدخل بريدك الإلكتروني:")
user_password = st.text_input("أدخل كلمة المرور:", type="password")

if st.button("تسجيل الدخول"):
    if user_email and user_password:
        try:
            # الاتصال بسيرفر جيمايل والتحقق من صحة البيانات مباشرة
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(user_email, user_password)
            
            # لو البيانات صحيحة بيدخل فوري
            st.success("تم تسجيل الدخول بنجاح يا فنان! أهلاً بك في تطبيق ميمو.")
            
        except Exception as e:
            st.error("فشل تسجيل الدخول: تأكد من صحة البريد الإلكتروني وكلمة المرور.")
    else:
        st.warning("الرجاء إدخال البريد الإلكتروني وكلمة المرور أولاً.")
