import streamlit as st
import g4f
from PIL import Image, ImageEnhance
import urllib.parse

# ==========================================
# 1. إعدادات تطبيق ميمو الذكي
# ==========================================
st.set_page_config(page_title="Memo AI Studio 2026", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f4f4f4;
    }
    h1, h2, h3 {
        color: #C8102E;
    }
    .stButton>button {
        background-color: #C8102E;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.title("🤖 ميمو AI - بدون مفاتيح")
st.sidebar.write("شات ذكي حر + توليد صور + محرر")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("اختر القسم:", [
    "💬 الشات الذكي الحر", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "✏️ محرر الصور والفلاتر"
])

# ==========================================
# 3. قسم الشات الذكي (يعمل بدون مفتاح API تماماً)
# ==========================================
if app_mode == "💬 الشات الذكي الحر":
    st.title("💬 ميمو - الشات الذكي المباشر")
    st.write("اسأل عن أي شيء، برمجة، رياضة، تاريخ... بدون مفاتيح وبدون حدود!")
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري توليد الإجابة..."):
                try:
                    # استخدام نموذج مجاني مدمج بدون الحاجة لمفتاح
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": user_prompt}],
                    )
                    bot_reply = str(response)
                    
                    st.markdown(bot_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"حدث خطأ بسيط، جرب مرة أخرى: {e}")

# ==========================================
# 4. قسم توليد الصور بالذكاء الاصطناعي
# ==========================================
elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    st.write("اكتب وصف أي صورة تخطر ببالك وسيتم رسمها فوراً!")
    st.markdown("---")

    image_prompt = st.text_input("صف الصورة:", placeholder="مثال: سيارة مستقبلية تطير في الفضاء")

    if st.button("توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري رسم الصورة..."):
                try:
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.success("تم توليد الصورة بنجاح!")
                    st.image(image_url, caption=image_prompt, use_column_width=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")
        else:
            st.warning("الرجاء كتابة وصف للصورة أولاً.")

# ==========================================
# 5. قسم محرر الصور والفلاتر
# ==========================================
elif app_mode == "✏️ محرر الصور والفلاتر":
    st.title("✏️ ميمو - محرر الصور")
    st.write("ارفع صورتك وعدل إضاءتها وتباينها بلمسة زر.")
    st.markdown("---")

    file = st.file_uploader("اختر صورة...", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="الصورة الأصلية", use_column_width=True)

        st.sidebar.markdown("### أدوات التعديل")
        brightness = st.sidebar.slider("الإضاءة", 0.1, 3.0, 1.0)
        contrast = st.sidebar.slider("التباين", 0.1, 3.0, 1.0)

        edited = ImageEnhance.Brightness(img).enhance(brightness)
        edited = ImageEnhance.Contrast(edited).enhance(contrast)

        st.subheader("الصورة النهائية:")
        st.image(edited, caption="بعد التعديل", use_column_width=True)
