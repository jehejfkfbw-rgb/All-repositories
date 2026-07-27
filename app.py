import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import urllib.request
import json
import urllib.parse
import io

# ==========================================
# 1. إعدادات وتصميم التطبيق
# ==========================================
st.set_page_config(page_title="Memo AI Studio", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f9f9f9;
    }
    h1, h2, h3 {
        color: #C8102E; /* اللون الأحمر الخاص بالأهلي */
    }
    .stButton>button {
        background-color: #C8102E;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #A00D24;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.title("🤖 ميمو الشامل")
st.sidebar.write("مساعدك الذكي المتكامل (بحث شامل، توليد، تحرير)")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("اختر الوظيفة:", [
    "🌐 البحث الذكي (شامل + تخصيص الأهلي)", 
    "🎨 توليد الصور بالذكاء الاصطناعي", 
    "✏️ محرر الصور والفلاتر"
])

st.sidebar.markdown("---")
st.sidebar.info("التطبيق جاهز ويعمل بكافة مكتباته بانتظام.")

# ==========================================
# 3. منطق البحث الذكي (يبحث في أي شيء، ولو 'الأهلي' يوجهه للمصري)
# ==========================================
if app_mode == "🌐 البحث الذكي (شامل + تخصيص الأهلي)":
    st.title("🌐 ميمو - محرك البحث الذكي")
    st.write("اسأل عن أي سؤال في العالم، وإذا كتبت 'الأهلي' وحدها فسأبحث لك عن **النادي الأهلي المصري** حصرياً!")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    def get_wikipedia_summary(query):
        try:
            search_term = query
            
            # الذكاء هنا: لو المستخدم كتب كلمة "الأهلي" فقط بدون تحديد، نوجهه للمصري تلقائياً
            # أما لو سأل عن أي شيء آخر (تاريخ، عواصم، علوم...) فسيترك البحث طبيعياً ليبحث عما طلبته
            if query.strip() == "الأهلي" or query.strip() == "النادي الأهلي":
                search_term = "النادي الأهلي المصري"
            elif "الأهلي" in query and "المصري" not in query and "السعودي" not in query and "الأردني" not in query:
                search_term = "النادي الأهلي المصري"

            encoded_query = urllib.parse.quote(search_term)
            url = f"https://ar.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                search_results = data.get('query', {}).get('search', [])
                
                if search_results:
                    best_match = search_results[0]
                    title = best_match.get('title', '')
                    snippet = best_match.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                    return f"### 📌 نتيجة البحث: {title}\n\n{snippet}...\n\n*(المعلومات مقدمة من موسوعة ويكيبيديا)*"
                else:
                    return "عذراً، لم أجد معلومات دقيقة حول هذا الموضوع."
        except Exception as e:
            return f"حدث خطأ في الاتصال: {e}"

    if prompt := st.chat_input("اكتب سؤالك هنا (مثلاً: الأهلي، أو عاصمة فرنسا، أو تاريخ الفراعنة)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري البحث..."):
                response = get_wikipedia_summary(prompt)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# 4. منطق توليد الصور بالذكاء الاصطناعي
# ==========================================
elif app_mode == "🎨 توليد الصور بالذكاء الاصطناعي":
    st.title("🎨 ميمو - استوديو توليد الصور")
    st.write("اكتب وصفاً دقيقاً للصورة التي تتخيلها، وسيقوم ميمو برسمها لك!")
    st.markdown("---")

    ai_prompt = st.text_input("اكتب وصف الصورة هنا (بالعربية أو الإنجليزية):", placeholder="مثال: نسر الأهلي يحلق فوق ملعب القاهرة")

    if st.button("🎨 ابدأ التوليد"):
        if ai_prompt:
            with st.spinner("جاري توليد الصورة بالذكاء الاصطناعي... قد يستغرق الأمر لحظات..."):
                try:
                    encoded_prompt = urllib.parse.quote(ai_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                    
                    with urllib.request.urlopen(image_url) as response:
                        image_data = response.read()
                        img = Image.open(io.BytesIO(image_data))
                        
                        st.success("تم توليد الصورة بنجاح!")
                        st.image(img, caption=f"الصورة المولدة: {ai_prompt}", use_column_width=True)
                        
                        st.markdown(f'<a href="{image_url}" download="memo_generated_image.jpg" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; padding: 10px 20px; border:none; border-radius:5px; cursor:pointer;">📥 تحميل الصورة</button></a>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء توليد الصورة: {e}")
        else:
            st.warning("الرجاء كتابة وصف للصورة أولاً.")

# ==========================================
# 5. منطق محرر الصور والفلاتر
# ==========================================
elif app_mode == "✏️ محرر الصور والفلاتر":
    st.title("✏️ ميمو - محرر الصور المتقدم")
    st.write("ارفع صورتك الخاصة، وقم بتعديل الإضاءة، التباين، وإضافة الفلاتر.")
    st.markdown("---")

    uploaded_file = st.file_uploader("اختر صورة من جهازك...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            original_img = Image.open(uploaded_file)
            
            with st.expander("عرض الصورة الأصلية", expanded=False):
                st.image(original_img, caption="الصورة الأصلية", use_column_width=True)

            st.sidebar.markdown("### 🎛️ أدوات التحرير")
            
            brightness = st.sidebar.slider("درجة الإضاءة (Brightness)", 0.0, 3.0, 1.0, 0.1)
            contrast = st.sidebar.slider("التباين (Contrast)", 0.0, 3.0, 1.0, 0.1)
            sharpness = st.sidebar.slider("حدة الصورة (Sharpness)", 0.0, 3.0, 1.0, 0.1)
            
            apply_blur = st.sidebar.checkbox("تطبيق تأثير ضبابي (Blur)")
            apply_bw = st.sidebar.checkbox("تحويل إلى أبيض وأسود (Grayscale)")

            enhancer_bright = ImageEnhance.Brightness(original_img)
            img_edited = enhancer_bright.enhance(brightness)
            
            enhancer_contrast = ImageEnhance.Contrast(img_edited)
            img_edited = enhancer_contrast.enhance(contrast)
            
            enhancer_sharp = ImageEnhance.Sharpness(img_edited)
            img_edited = enhancer_sharp.enhance(sharpness)

            if apply_blur:
                img_edited = img_edited.filter(ImageFilter.BLUR)
            
            if apply_bw:
                img_edited = img_edited.convert("L")

            st.subheader("✨ الصورة بعد التعديل:")
            st.image(img_edited, caption="صورتك المعدلة بواسطة ميمو", use_column_width=True)

            buf = io.BytesIO()
            img_edited.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="💾 تحميل الصورة النهائية المعدلة",
                data=byte_im,
                file_name="memo_edited_image.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الصورة: {e}")
    else:
        st.info("الرجاء رفع صورة للبدء في التحرير.")

# ==========================================
# 6. التذييل (Footer)
# ==========================================
st.markdown("---")
st.caption("تطبيق ميمو الشامل (Memo AI Studio) - جميع الحقوق محفوظة © 2024")
