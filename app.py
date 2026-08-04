import streamlit as st
import g4f
from PIL import Image
import urllib.parse
import time
import os
import requests

# --- إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="Nova AI Studio - Kivo", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تنسيق التصميم (CSS) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f4f4f4; }
    h1, h2, h3 { color: #1E88E5; }
    .stButton>button { background-color: #1E88E5; color: white; border-radius: 5px; width: 100%; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #1565C0; }
    .history-item { padding: 8px; background-color: #e0e0e0; border-radius: 5px; font-size: 13px; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- البريد المخصص للمطور التنفيذي ---
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
SESSION_FILE = "user_session.txt"

# --- إدارة جلسة التسجيل الدائم ---
def get_saved_user():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_user(email):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(email)

def delete_user_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

saved_user = get_saved_user()

# ==========================================
# 🔒 1. شاشة التسجيل (مرة واحدة فقط)
# ==========================================
if not saved_user:
    st.title("⚡ مرحباً بك في Nova AI")
    st.caption("إحدى تطويرات شركة كيفو (Kivo)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 تسجيل الدخول")
        email = st.text_input("البريد الإلكتروني (Email)", placeholder="jehejfkfbw@gmail.com")
        password = st.text_input("كلمة السر (Password)", type="password", placeholder="••••••••")
        
        if st.button("دخول"):
            clean_email = email.strip().lower()
            if clean_email != "" and password.strip() != "":
                with st.spinner("جاري حفظ بيانات الدخول..."):
                    save_user(clean_email)
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.error("يرجى إدخال البريد الإلكتروني وكلمة السر بشكل صحيح.")

# ==========================================
# 🚀 2. التطبيق الرئيسي
# ==========================================
else:
    user_email = saved_user
    is_executive = (user_email.strip().lower() == EXECUTIVE_EMAIL.lower())

    st.sidebar.title("⚡ نوفا | Nova AI")
    st.sidebar.caption("تطبيق تابع لشركة **كيفو (Kivo)**")

    if is_executive:
        st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
    else:
        st.sidebar.info(f"👤 العميل: {user_email}")

    if "messages" not in st.session_state:
        if is_executive:
            welcome_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! نظام Nova في خدمتك بالكامل."
        else:
            welcome_msg = "مرحباً بك في تطبيق Nova من شركة كيفو! أنا مساعدك الذكي، كيف يمكنني مساعدتك اليوم؟ (يمكنك طلب رسم أي صورة هنا فوراً)"
            
        st.session_state.messages = [
            {"role": "assistant", "content": welcome_msg}
        ]

    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []

    st.sidebar.markdown("---")
    
    # ------------------------------------------
    # 🗂️ 1. إدارة ومسح المحادثات فردياً
    # ------------------------------------------
    st.sidebar.subheader("🗂️ سجل المحادثات")
    
    user_msg_count = 0
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            user_msg_count += 1
            col_txt, col_del = st.sidebar.columns([4, 1])
            with col_txt:
                st.markdown(f'<div class="history-item">💬 {msg["content"][:22]}...</div>', unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_{idx}"):
                    del st.session_state.messages[idx]
                    if idx < len(st.session_state.messages) and st.session_state.messages[idx]["role"] == "assistant":
                        del st.session_state.messages[idx]
                    st.rerun()

    if user_msg_count == 0:
        st.sidebar.write("لا يوجد محادثات حالياً.")

    if st.sidebar.button("🗑️ مسح السجل بالكامل"):
        initial_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو!" if is_executive else "مرحباً بك في تطبيق Nova من شركة كيفو!"
        st.session_state.messages = [{"role": "assistant", "content": initial_msg}]
        st.rerun()

    st.sidebar.markdown("---")

    # ------------------------------------------
    # 🖼️ 2. قسم مكتبة/معرض الصور المتولدة في الجنب
    # ------------------------------------------
    st.sidebar.subheader("🖼️ معرض الصور المتولدة")
    if len(st.session_state.generated_images) > 0:
        st.sidebar.caption(f"عدد الصور: {len(st.session_state.generated_images)}")
        for img_item in reversed(st.session_state.generated_images[-3:]):
            st.sidebar.image(img_item["url"], caption=f"📌 {img_item['prompt'][:20]}...", use_column_width=True)
    else:
        st.sidebar.write("لم يتم توليد أي صور بعد.")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 تسجيل الخروج"):
        delete_user_session()
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    app_mode = st.sidebar.radio("اختر القسم:", ["💬 الشات الذكي (Nova)", "🕌 مواقيت الصلاة والعداد التنازلي", "🎨 توليد الصور"])

    # ------------------------------------------
    # 💬 قسم الشات الذكي (Nova AI) - مع توليد وتنزيل الصور المباشر
    # ------------------------------------------
    if app_mode == "💬 الشات الذكي (Nova)":
        st.title("⚡ الذكاء الاصطناعي Nova")
        
        if is_executive:
            st.success("🌟 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي لشركة كيفو)")
        else:
            st.markdown("### مرحباً بك في **Nova** من شركة **كيفو (Kivo)**، يمكنك التحدث معي أو طلب رسم وصناعة أي صورة تريدها!")
            
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                # إذا كانت الرسالة تحتوي على صورة وتنزيل
                if "image_bytes" in m:
                    st.image(m["image_bytes"], caption="الصورة المتولدة 🎨")
                    st.download_button(
                        label="📥 تنزيل الصورة الآن",
                        data=m["image_bytes"],
                        file_name=f"nova_chat_img_{int(time.time())}.png",
                        mime="image/png",
                        key=f"dl_chat_{m.get('img_id', time.time())}"
                    )
                
        if user_prompt := st.chat_input("اكتب سؤالك أو اطلب صورة (مثال: اعمل لي صورة فندق فاخر)..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant"):
                # التحقق إذا كان العميل يطلب صراحة رسم/توليد صورة
                image_keywords = ["صورة", "صوره", "ارسم", "انشئ صورة", "اعمل لي صورة", "اعمل لي صوره", "generate image", "draw"]
                is_image_request = any(kw in user_prompt.lower() for kw in image_keywords)
                
                if is_image_request:
                    with st.spinner("⚡ Nova يقوم برسم وتوليد الصورة بأعلى سرعة..."):
                        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_prompt)}?width=1024&height=1024&nologo=true"
                        try:
                            response = requests.get(img_url)
                            if response.status_code == 200:
                                img_bytes = response.content
                                reply_txt = f"تم توليد الصورة المطلوبة بأعلى سرعة ودقة! يمكنك تنزيلها فوراً عبر الزر أدناه 🎨"
                                st.markdown(reply_txt)
                                st.image(img_bytes, caption=user_prompt)
                                
                                img_id = int(time.time())
                                st.download_button(
                                    label="📥 تنزيل الصورة الآن",
                                    data=img_bytes,
                                    file_name=f"nova_{img_id}.png",
                                    mime="image/png",
                                    key=f"btn_dl_{img_id}"
                                )
                                
                                # حفظ المحادثة والمعرض
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": reply_txt, 
                                    "image_bytes": img_bytes,
                                    "img_id": img_id
                                })
                                st.session_state.generated_images.append({"prompt": user_prompt, "url": img_url, "bytes": img_bytes})
                            else:
                                st.error("تعذر جلب الصورة، حاول مرة أخرى.")
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء الاتصال بالسيرفر: {e}")
                else:
                    system_instruction = (
                        "أنت مساعد ذكي اسمك Nova (نوفا) تابع لشركة كيفو (Kivo). "
                        "إذا سألك أي شخص من المطور أو من صنعك أو من طورك، يجب أن تجيب دائماً بوضوح وبصيغة احترافية: "
                        "'المطور التنفيذي هو محمد عادل من شركة كيفو (Kivo)'."
                    )
                    
                    api_messages = [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ]

                    with st.spinner("Nova يفكر الآن... ⚡"):
                        try:
                            res = str(g4f.ChatCompletion.create(model=g4f.models.default, messages=api_messages))
                        except Exception as e:
                            res = f"حدث خطأ أثناء الاتصال: {e}"
                    
                    message_placeholder = st.empty()
                    streamed_text = ""
                    for word in res.split():
                        streamed_text += word + " "
                        message_placeholder.markdown(streamed_text + "▌")
                        time.sleep(0.02)
                    message_placeholder.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})

    # ------------------------------------------
    # 🕌 قسم مواقيت الصلاة
    # ------------------------------------------
    elif app_mode == "🕌 مواقيت الصلاة والعداد التنازلي":
        st.title("🕌 مواقيت الصلاة والعداد التنازلي اللحظي")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("الفجر", "03:15 ص")
        col1.metric("الظهر", "11:58 ص")
        col2.metric("العصر", "03:32 م")
        col2.metric("المغرب", "06:51 م")
        col3.metric("العشاء", "08:14 م")
        
        st.markdown("---")
        st.subheader("⏳ العداد التنازلي (ينزل ثانية بثانية):")
        
        countdown_placeholder = st.empty()
        for seconds_left in range(300, 0, -1):
            mins, secs = divmod(seconds_left, 60)
            countdown_placeholder.markdown(f"🚨 **باقي على الصلاة القادمة: {mins} دقيقة و {secs} ثانية**")
            time.sleep(1)
        
        st.markdown("### 🔊 مشغل صوت الآذان")
        adhan_audio_url = "https://www.islamcan.com/audio/adhan/azan1.mp3"
        st.audio(adhan_audio_url, format="audio/mp3", start_time=0)

    # ------------------------------------------
    # 🎨 قسم توليد الصور المستقل
    # ------------------------------------------
    elif app_mode == "🎨 توليد الصور":
        st.title("🎨 استوديو توليد الصور - Nova")
        p = st.text_input("صف الصورة التي تريدها (مثال: فندق فاخر على الشاطئ بحديقة واسعة):")
        
        if st.button("توليد الصورة 🎨") and p:
            with st.spinner("جاري رسم الصورة بأعلى سرعة وإعداد رابط التنزيل المباشر... ⚡"):
                img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true"
                
                try:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img_bytes = response.content
                        st.image(img_bytes, caption=f"الوصف: {p}")
                        
                        # زر تنزيل الصورة
                        st.download_button(
                            label="📥 تنزيل الصورة إلى جهازك الآن",
                            data=img_bytes,
                            file_name=f"nova_{int(time.time())}.png",
                            mime="image/png"
                        )
                        
                        st.session_state.generated_images.append({"prompt": p, "url": img_url, "bytes": img_bytes})
                    else:
                        st.error("تعذر توليد الصورة، يرجى المحاولة لاحقاً.")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تنزيل الصورة: {e}")

        if len(st.session_state.generated_images) > 0:
            st.markdown("---")
            st.subheader("📚 أرشيف الصور المطلوبة سابقاً:")
            cols = st.columns(2)
            for idx, img_item in enumerate(reversed(st.session_state.generated_images)):
                with cols[idx % 2]:
                    st.image(img_item["url"], caption=f"الوصف: {img_item['prompt']}")
                    if "bytes" in img_item:
                        st.download_button(
                            label=f"📥 تنزيل الصورة",
                            data=img_item["bytes"],
                            file_name=f"nova_img_{idx}.png",
                            mime="image/png",
                            key=f"dl_tab_{idx}"
                        )
