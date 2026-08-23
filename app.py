import streamlit as st
import g4f
from PIL import Image
import urllib.parse
import time
import os
import requests
from gtts import gTTS
import base64
import io

# ==========================================
# ⚙️ 1. إعدادات الصفحة (شريط جانبي مفتوح وثابت)
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded" # إجبار الشريط الجانبي على الظهور دائماً
)

# كود CSS لتثبيت زر الـ 3 شرط والشريط الجانبي على الموبايل
st.markdown("""
    <style>
    /* إظهار زر الثلاث شرط بوضوح على الموبايل */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        z-index: 999999 !important;
    }

    /* تنسيق الشريط الجانبي */
    [data-testid="stSidebar"] { 
        background-color: #111827 !important; 
        color: #ffffff !important;
    }
    
    /* الأزرار */
    .stButton>button { 
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); 
        color: white !important; 
        border-radius: 8px; 
        width: 100%; 
        border: none; 
        padding: 8px; 
        font-weight: bold;
    }

    /* بطاقات السجل في الشريط الجانبي */
    .history-card {
        padding: 8px;
        background-color: #1f2937;
        border-right: 3px solid #1E88E5;
        border-radius: 4px;
        margin-bottom: 5px;
        font-size: 12px;
        color: #ffffff;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- دالة تحويل النص إلى صوت (Audio Generator) ---
def text_to_audio(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        return None

# --- إدارة التسجيل ---
EXECUTIVE_EMAIL = "jehejfkfbw@gmail.com"
SESSION_FILE = "user_session.txt"

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
# 🔒 2. شاشة التسجيل
# ==========================================
if not saved_user:
    st.title("⚡ مرحباً بك في منصة Nova AI")
    st.caption("إحدى تطويرات شركة كيفو (Kivo)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 تسجيل الدخول السريع")
        email = st.text_input("البريد الإلكتروني (Email)", placeholder="jehejfkfbw@gmail.com")
        password = st.text_input("كلمة السر (Password)", type="password", placeholder="••••••••")
        
        if st.button("دخول المنصة"):
            clean_email = email.strip().lower()
            if clean_email != "" and password.strip() != "":
                with st.spinner("جاري تأكيد الهوية..."):
                    save_user(clean_email)
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.error("يرجى إدخال البريد الإلكتروني وكلمة السر بشكل صحيح.")

# ==========================================
# 🚀 3. التطبيق الرئيسي
# ==========================================
else:
    user_email = saved_user
    is_executive = (user_email.strip().lower() == EXECUTIVE_EMAIL.lower())

    # ------------------------------------------
    # ☰ الشريط الجانبي (Sidebar)
    # ------------------------------------------
    st.sidebar.title("☰ القائمة الرئيسية")
    st.sidebar.caption("تطبيق تابع لشركة **كيفو (Kivo)**")

    if is_executive:
        st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
    else:
        st.sidebar.info(f"👤 المستخدم: {user_email}")

    # تهيئة المحادثات
    if "messages" not in st.session_state:
        welcome_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! نظام Nova في خدمتك بالكامل." if is_executive else "مرحباً بك في تطبيق Nova من شركة كيفو!"
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

    if "generated_media" not in st.session_state:
        st.session_state.generated_media = []

    st.sidebar.markdown("---")
    
    # خيارات التحكم والمحادثات في السايدبار
    if st.sidebar.button("➕ محادثة جديدة"):
        initial_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل!" if is_executive else "أهلاً بك مجدداً في Nova AI!"
        st.session_state.messages = [{"role": "assistant", "content": initial_msg}]
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🗂️ السجل (حذف فردي)")

    user_msg_count = 0
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            user_msg_count += 1
            col_txt, col_del = st.sidebar.columns([4, 1])
            with col_txt:
                st.markdown(f'<div class="history-card">💬 {msg["content"][:18]}...</div>', unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_msg_side_{idx}"):
                    del st.session_state.messages[idx]
                    if idx < len(st.session_state.messages) and st.session_state.messages[idx]["role"] == "assistant":
                        del st.session_state.messages[idx]
                    st.rerun()

    if user_msg_count == 0:
        st.sidebar.caption("لا يوجد سجل محادثات.")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 تسجيل الخروج"):
        delete_user_session()
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # اختيار الأقسام من الشريط الجانبي
    app_mode = st.sidebar.radio("📌 التنقل بين الأقسام:", [
        "💬 الشات الذكي (محادثات صوتیة + صور + فيديوهات)", 
        "🎨 استوديو توليد الصور والفيديوهات", 
        "🕌 مواقيت الصلاة والعداد التنازلي"
    ])

    # ------------------------------------------
    # 🚀 الشاشة الرئيسية
    # ------------------------------------------
    st.title("⚡ نوفا | Nova AI Studio")
    
    if is_executive:
        st.success("👑 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي)")

    st.markdown("---")

    # ------------------------------------------
    # 💬 1. الشات الرئيسي مع ميزة الصوت
    # ------------------------------------------
    if app_mode == "💬 الشات الذكي (محادثات صوتیة + صور + فيديوهات)":
        
        # عرض جميع الرسائل مع مشغل الصوت للردود
        for idx, m in enumerate(st.session_state.messages):
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                
                # إذا كانت الرسالة من المساعد الذكي، نضع خيار تشغيل الصوت
                if m["role"] == "assistant":
                    if "audio_bytes" in m:
                        st.audio(m["audio_bytes"], format="audio/mp3")
                    else:
                        if st.button("🔊 استماع للرد", key=f"tts_btn_{idx}"):
                            audio_data = text_to_audio(m["content"])
                            if audio_data:
                                m["audio_bytes"] = audio_data
                                st.audio(audio_data, format="audio/mp3")

                if "image_bytes" in m:
                    st.image(m["image_bytes"], caption="الصورة المتولدة 🎨")
                    st.download_button(
                        label="📥 تنزيل الصورة",
                        data=m["image_bytes"],
                        file_name=f"nova_{int(time.time())}.png",
                        mime="image/png",
                        key=f"dl_chat_{m.get('id', time.time())}"
                    )
                
                if "video_url" in m:
                    st.image(m["video_url"], caption="المقطع المتحرك 🎥")
                    st.markdown(f"[📥 تنزيل الفيديو]({m['video_url']})")

        # إدخال السؤال
        if user_prompt := st.chat_input("اكتب سؤالك، أو اطلب (اعمل لي صورة...) أو (اعمل لي فيديو...)..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant"):
                prompt_lower = user_prompt.lower()
                
                img_keywords = ["صورة", "صوره", "ارسم", "انشئ صورة", "اعمل لي صورة", "draw", "image"]
                is_img_req = any(kw in prompt_lower for kw in img_keywords)
                
                video_keywords = ["فيديو", "فديو", "مقطع", "اعمل لي فيديو", "video", "movie"]
                is_video_req = any(kw in prompt_lower for kw in video_keywords)

                if is_img_req:
                    with st.spinner("⚡ Nova يقوم برسم الصورة..."):
                        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_prompt)}?width=1024&height=1024&nologo=true"
                        try:
                            res = requests.get(img_url)
                            if res.status_code == 200:
                                img_bytes = res.content
                                txt = "تم توليد الصورة المطلوبة بنجاح! 🎨"
                                st.markdown(txt)
                                st.image(img_bytes)
                                
                                msg_id = time.time()
                                st.download_button(
                                    label="📥 تنزيل الصورة",
                                    data=img_bytes,
                                    file_name=f"nova_{int(msg_id)}.png",
                                    mime="image/png",
                                    key=f"dl_btn_{msg_id}"
                                )
                                
                                st.session_state.messages.append({"role": "assistant", "content": txt, "image_bytes": img_bytes, "id": msg_id})
                                st.session_state.generated_media.append({"type": "image", "prompt": user_prompt, "url": img_url, "bytes": img_bytes})
                        except Exception as e:
                            st.error(f"خطأ أثناء التوليد: {e}")

                elif is_video_req:
                    with st.spinner("⚡ Nova يقوم بتوليد الفيديو..."):
                        video_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_prompt)}?width=1024&height=1024&model=flux&nologo=true"
                        txt = "تم توليد المقطع المتحرك بنجاح! 🎥"
                        st.markdown(txt)
                        st.image(video_url, caption="معاينة الفيديو")
                        st.markdown(f"[📥 تنزيل الفيديو]({video_url})")
                        
                        st.session_state.messages.append({"role": "assistant", "content": txt, "video_url": video_url})
                        st.session_state.generated_media.append({"type": "video", "prompt": user_prompt, "url": video_url})

                else:
                    system_instruction = (
                        "أنت مساعد ذكي اسمك Nova تابع لشركة كيفو (Kivo). "
                        "إذا سألك أي شخص عن المطور أو من صنعك، أجب بدقة واحترافية: "
                        "'المطور التنفيذي هو محمد عادل من شركة كيفو (Kivo)'."
                    )
                    api_messages = [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ]

                    with st.spinner("Nova يفكر الآن... ⚡"):
                        try:
                            res_text = str(g4f.ChatCompletion.create(model=g4f.models.default, messages=api_messages))
                        except Exception as e:
                            res_text = f"حدث خطأ أثناء الاتصال: {e}"
                    
                    st.markdown(res_text)
                    
                    # تحويل النص المستلم إلى صوت وتوليد مشغل صوت تلقائياً
                    audio_fp = text_to_audio(res_text)
                    if audio_fp:
                        st.audio(audio_fp, format="audio/mp3")
                        st.session_state.messages.append({"role": "assistant", "content": res_text, "audio_bytes": audio_fp})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": res_text})

    # ------------------------------------------
    # 🎨 2. قسم استوديو الوسائط
    # ------------------------------------------
    elif app_mode == "🎨 استوديو توليد الصور والفيديوهات":
        st.title("🎨 استوديو الوسائط - Nova Studio")
        
        tab1, tab2 = st.tabs(["🖼️ توليد الصور", "🎥 توليد الفيديوهات"])
        
        with tab1:
            p_img = st.text_input("صف الصورة التي تريدها:")
            if st.button("توليد الصورة 🎨") and p_img:
                with st.spinner("جاري الرسم..."):
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true"
                    res = requests.get(img_url)
                    if res.status_code == 200:
                        st.image(res.content, caption=p_img)
                        st.download_button("📥 تنزيل الصورة", data=res.content, file_name="nova_img.png", mime="image/png")
                        st.session_state.generated_media.append({"type": "image", "prompt": p_img, "url": img_url, "bytes": res.content})

        with tab2:
            p_vid = st.text_input("صف الفيديو الذي تريده:")
            if st.button("توليد الفيديو 🎥") and p_vid:
                with st.spinner("جاري التوليد..."):
                    vid_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_vid)}?width=1024&height=1024&model=flux&nologo=true"
                    st.image(vid_url, caption="المعاينة")
                    st.markdown(f"[📥 تنزيل الفيديو]({vid_url})")
                    st.session_state.generated_media.append({"type": "video", "prompt": p_vid, "url": vid_url})

    # ------------------------------------------
    # 🕌 3. مواقيت الصلاة
    # ------------------------------------------
    elif app_mode == "🕌 مواقيت الصلاة والعداد التنازلي":
        st.title("🕌 مواقيت الصلاة والعداد التنازلي")
        col1, col2, col3 = st.columns(3)
        col1.metric("الفجر", "03:15 ص")
        col1.metric("الظهر", "11:58 ص")
        col2.metric("العصر", "03:32 م")
        col2.metric("المغرب", "06:51 م")
        col3.metric("العشاء", "08:14 م")
        st.markdown("---")
        countdown_placeholder = st.empty()
        for seconds_left in range(300, 0, -1):
            mins, secs = divmod(seconds_left, 60)
            countdown_placeholder.markdown(f"🚨 **باقي على الصلاة القادمة: {mins} دقيقة و {secs} ثانية**")
            time.sleep(1)
        st.audio("https://www.islamcan.com/audio/adhan/azan1.mp3", format="audio/mp3", start_time=0)
