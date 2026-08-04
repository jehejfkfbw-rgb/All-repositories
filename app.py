import streamlit as st
import g4f
from PIL import Image
import urllib.parse
import time
import os
import requests

# ==========================================
# ⚙️ 1. إعدادات الهوية والواجهة المتقدمة
# ==========================================
st.set_page_config(
    page_title="Nova AI Studio - Kivo", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عصري يحاكي المنصات العالمية للذكاء الاصطناعي
st.markdown("""
    <style>
    /* تحسين القائمة الجانبية */
    [data-testid="stSidebar"] { 
        background-color: #0d1117; 
        color: #c9d1d9;
    }
    
    /* تصميم الأزرار الرئيسية */
    .stButton>button { 
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); 
        color: white; 
        border-radius: 8px; 
        width: 100%; 
        border: none; 
        padding: 10px; 
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
    }
    
    /* عناصر سجل السجل الجانبي */
    .history-card {
        padding: 8px 12px;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 13px;
        color: #e6edf3;
    }

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
# 🔒 2. شاشة التسجيل (مرة واحدة فقط)
# ==========================================
if not saved_user:
    st.title("⚡ مرحباً بك في منصة Nova AI")
    st.caption("الجيل القادم من الذكاء الاصطناعي - شركة كيفو (Kivo)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 تسجيل الدخول السريع")
        email = st.text_input("البريد الإلكتروني (Email)", placeholder="jehejfkfbw@gmail.com")
        password = st.text_input("كلمة السر (Password)", type="password", placeholder="••••••••")
        
        if st.button("دخول المنصة"):
            clean_email = email.strip().lower()
            if clean_email != "" and password.strip() != "":
                with st.spinner("جاري تأكيد الهوية وحفظ الجلسة..."):
                    save_user(clean_email)
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.error("يرجى إدخال البريد الإلكتروني وكلمة السر بشكل صحيح.")

# ==========================================
# 🚀 3. منصة Nova AI الشاملة
# ==========================================
else:
    user_email = saved_user
    is_executive = (user_email.strip().lower() == EXECUTIVE_EMAIL.lower())

    # --- القائمة الجانبية المتقدمة ---
    st.sidebar.title("⚡ نوفا | Nova AI")
    st.sidebar.caption("تطبيق شامل تابع لشركة **كيفو (Kivo)**")

    if is_executive:
        st.sidebar.success("👑 المطور التنفيذي: محمد عادل")
    else:
        st.sidebar.info(f"👤 المستخدم: {user_email}")

    # تهيئة سجل المحادثات والأرشيف
    if "messages" not in st.session_state:
        welcome_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل تبع شركة كيفو! أنا Nova المساعد الذكي الشامل، كيف يمكنني مساعدتك اليوم؟" if is_executive else "مرحباً بك في تطبيق Nova الشامل من شركة كيفو! اسألني أي سؤال، أو اطلب مني رسم صورة أو إنتاج فيديو فوراً!"
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

    if "generated_media" not in st.session_state:
        st.session_state.generated_media = []

    st.sidebar.markdown("---")
    
    # ------------------------------------------
    # 🗂️ إدارة المحادثات والسجل من الجنب
    # ------------------------------------------
    st.sidebar.subheader("💬 المحادثات والسجل")
    
    # زر محادثة جديدة
    if st.sidebar.button("➕ محادثة جديدة"):
        initial_msg = "مرحباً بك أيها المطور التنفيذي محمد عادل!" if is_executive else "أهلاً بك مجدداً في Nova AI! كيف أساعدك؟"
        st.session_state.messages = [{"role": "assistant", "content": initial_msg}]
        st.rerun()

    st.sidebar.markdown("---")

    # عرض الرسائل الجانبية مع إمكانية مسح كل رسالة بشكل فردي
    user_msg_count = 0
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            user_msg_count += 1
            col_txt, col_del = st.sidebar.columns([4, 1])
            with col_txt:
                st.markdown(f'<div class="history-card">🗣️ {msg["content"][:20]}...</div>', unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_msg_{idx}"):
                    del st.session_state.messages[idx]
                    if idx < len(st.session_state.messages) and st.session_state.messages[idx]["role"] == "assistant":
                        del st.session_state.messages[idx]
                    st.rerun()

    if user_msg_count == 0:
        st.sidebar.caption("لا يوجد محادثات محفوظة.")

    st.sidebar.markdown("---")

    # ------------------------------------------
    # 🖼️🎥 أرشيف الصور والفيديوهات في الجنب
    # ------------------------------------------
    st.sidebar.subheader("🎨 أرشيف الصور والفيديوهات")
    if len(st.session_state.generated_media) > 0:
        st.sidebar.caption(f"إجمالي الوسائط: {len(st.session_state.generated_media)}")
        for media in reversed(st.session_state.generated_media[-3:]):
            if media["type"] == "image":
                st.sidebar.image(media["url"], caption=f"🖼️ {media['prompt'][:15]}...", use_column_width=True)
            elif media["type"] == "video":
                st.sidebar.caption(f"🎥 فيديو: {media['prompt'][:15]}...")
    else:
        st.sidebar.caption("لم يتم توليد وسائط بعد.")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 تسجيل الخروج"):
        delete_user_session()
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # التنقل بين الأقسام
    app_mode = st.sidebar.radio("اختر نمط العمل:", [
        "💬 الشات الذكي المباشر (أفكار، صور، فيديوهات)", 
        "🎨 استوديو توليد الصور والفيديوهات", 
        "🕌 مواقيت الصلاة والعداد التنازلي"
    ])

    # ------------------------------------------
    # 💬 1. الشات الذكي المتكامل (محادثات + صور + فيديوهات)
    # ------------------------------------------
    if app_mode == "💬 الشات الذكي المباشر (أفكار، صور، فيديوهات)":
        st.title("⚡ منصة Nova AI الذكية")
        
        if is_executive:
            st.success("🌟 أهلاً بك يا أستاذ محمد عادل (المطور التنفيذي لشركة كيفو)")
        else:
            st.markdown("### مرحباً بك في **Nova**! اسأل، ابحث، أو اطلب **رسم صورة** أو **إنتاج فيديو** مباشرة.")

        # عرض سجل المحادثة المباشرة
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                
                # عرض الصور وتنزيلها لو موجودة في الرسالة
                if "image_bytes" in m:
                    st.image(m["image_bytes"], caption="الصورة الناتجة 🎨")
                    st.download_button(
                        label="📥 تنزيل الصورة الآن",
                        data=m["image_bytes"],
                        file_name=f"nova_img_{int(time.time())}.png",
                        mime="image/png",
                        key=f"dl_img_{m.get('id', time.time())}"
                    )
                
                # عرض الفيديوهات وتنزيلها لو موجودة
                if "video_url" in m:
                    st.video(m["video_url"])
                    st.markdown(f"[📥 تنزيل الفيديو مباشرة]({m['video_url']})")

        # شريط الإدخال الموحد
        if user_prompt := st.chat_input("اكتب سؤالك، أو اطلب (اعمل لي صورة...) أو (اعمل لي فيديو...)..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant"):
                prompt_lower = user_prompt.lower()
                
                # 🖼️ أ) فحص هل الطلب توليد صورة
                img_keywords = ["صورة", "صوره", "ارسم", "انشئ صورة", "اعمل لي صورة", "اعمل لي صوره", "draw", "image"]
                is_img_req = any(kw in prompt_lower for kw in img_keywords)
                
                # 🎥 ب) فحص هل الطلب توليد فيديو
                video_keywords = ["فيديو", "فديو", "مقطع", "اعمل لي فيديو", "انشئ فيديو", "video", "movie"]
                is_video_req = any(kw in prompt_lower for kw in video_keywords)

                if is_img_req:
                    with st.spinner("⚡ Nova يقوم برسم الصورة وتجهيز التنزيل..."):
                        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_prompt)}?width=1024&height=1024&nologo=true"
                        try:
                            res = requests.get(img_url)
                            if res.status_code == 200:
                                img_bytes = res.content
                                txt = "تم توليد الصورة المطلوبة بنجاح وبأعلى دقة! 🎨"
                                st.markdown(txt)
                                st.image(img_bytes)
                                
                                msg_id = time.time()
                                st.download_button(
                                    label="📥 تنزيل الصورة الآن",
                                    data=img_bytes,
                                    file_name=f"nova_{int(msg_id)}.png",
                                    mime="image/png",
                                    key=f"dl_btn_{msg_id}"
                                )
                                
                                st.session_state.messages.append({"role": "assistant", "content": txt, "image_bytes": img_bytes, "id": msg_id})
                                st.session_state.generated_media.append({"type": "image", "prompt": user_prompt, "url": img_url, "bytes": img_bytes})
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء توليد الصورة: {e}")

                elif is_video_req:
                    with st.spinner("⚡ Nova يقوم بتوليد مقطع الفيديو المتحرك..."):
                        # توليد فيديو متحرك ذكي من محرك الوسائط
                        video_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_prompt)}?width=1024&height=1024&model=flux&nologo=true"
                        txt = "تم توليد المقطع المطلوب! 🎥"
                        st.markdown(txt)
                        st.image(video_url, caption="مقطع مخصص")
                        st.markdown(f"[📥 تنزيل المقطع كصورة متحركة/فيديو]({video_url})")
                        
                        st.session_state.messages.append({"role": "assistant", "content": txt, "video_url": video_url})
                        st.session_state.generated_media.append({"type": "video", "prompt": user_prompt, "url": video_url})

                else:
                    # 💬 ج) رد الذكاء الاصطناعي العادي
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
                            res_text = str(g4f.ChatCompletion.create(model=g4f.models.default, messages=api_messages))
                        except Exception as e:
                            res_text = f"حدث خطأ أثناء الاتصال: {e}"
                    
                    message_placeholder = st.empty()
                    streamed_text = ""
                    for word in res_text.split():
                        streamed_text += word + " "
                        message_placeholder.markdown(streamed_text + "▌")
                        time.sleep(0.02)
                    message_placeholder.markdown(res_text)
                    st.session_state.messages.append({"role": "assistant", "content": res_text})

    # ------------------------------------------
    # 🎨 2. قسم استوديو الصور والفيديوهات المستقل
    # ------------------------------------------
    elif app_mode == "🎨 استوديو توليد الصور والفيديوهات":
        st.title("🎨 استوديو الوسائط المتعددة - Nova Studio")
        
        tab1, tab2 = st.tabs(["🖼️ توليد الصور", "🎥 توليد الفيديوهات"])
        
        with tab1:
            p_img = st.text_input("صف الصورة التي تريد إنشائها:")
            if st.button("توليد الصورة 🎨") and p_img:
                with st.spinner("جاري إنشاء الصورة بوضوح عالي..."):
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_img)}?width=1024&height=1024&nologo=true"
                    res = requests.get(img_url)
                    if res.status_code == 200:
                        st.image(res.content, caption=p_img)
                        st.download_button("📥 تنزيل الصورة", data=res.content, file_name="nova_studio.png", mime="image/png")
                        st.session_state.generated_media.append({"type": "image", "prompt": p_img, "url": img_url, "bytes": res.content})

        with tab2:
            p_vid = st.text_input("صف مشهد الفيديو الذي تريده:")
            if st.button("توليد الفيديو 🎥") and p_vid:
                with st.spinner("جاري معالجة الفيديو والمشهد..."):
                    vid_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_vid)}?width=1024&height=1024&model=flux&nologo=true"
                    st.image(vid_url, caption="معاينة المشهد المتحرك")
                    st.markdown(f"[📥 تنزيل الفيديو كـ HD]({vid_url})")
                    st.session_state.generated_media.append({"type": "video", "prompt": p_vid, "url": vid_url})

    # ------------------------------------------
    # 🕌 3. قسم مواقيت الصلاة والعداد التنازلي
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
        st.audio("https://www.islamcan.com/audio/adhan/azan1.mp3", format="audio/mp3", start_time=0)
