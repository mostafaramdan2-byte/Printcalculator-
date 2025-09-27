import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="حاسبة تكلفة الطباعة", layout="wide")
st.title("🖨️ حاسبة تكلفة الطباعة A-Z")
st.markdown("برنامج شامل لحساب الورق، مقاس الفرخ، مقاس القص، وطريقة القص.")

# --------------------------
# بيانات أساسية
# --------------------------
with st.expander("📌 بيانات المطبوع"):
    job_type = st.selectbox("نوع المطبوع", ["نوت بوك", "منيو", "كتالوج", "فلاير", "بروشور", "مجلة", "فولدر", "أخرى"])
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("العرض (سم)", min_value=1.0, step=0.5)
    with col2:
        height = st.number_input("الطول (سم)", min_value=1.0, step=0.5)
    quantity = st.number_input("عدد النسخ المطلوبة", min_value=1, step=1)

# --------------------------
# الورق
# --------------------------
with st.expander("📄 تفاصيل الورق"):
    paper_type = st.selectbox("نوع الورق", ["كوشيه", "بريستول كوشيه", "ورق طبع"])
    paper_gram = st.selectbox("جرام الورق", list(range(90, 351, 10)))

# --------------------------
# الطباعة
# --------------------------
with st.expander("🎨 الطباعة"):
    colors = st.radio("ألوان الطباعة", ["أبيض وأسود", "ألوان"])

# --------------------------
# التشطيب
# --------------------------
with st.expander("✨ خدمات ما بعد الطباعة"):
    lamination = st.checkbox("سلوفان")
    binding = st.checkbox("تجليد/سلك")
    die_cut = st.checkbox("تكسير/قص خاص")

# --------------------------
# اقتراح مقاس الفرخ المناسب
# --------------------------
sheet_options = [(70, 100), (88, 44)]
best_fit_options = []

for sw, sh in sheet_options:
    fit_x = sw // width
    fit_y = sh // height
    total_fit = fit_x * fit_y
    if total_fit > 0:
        best_fit_options.append((sw, sh, total_fit))

if best_fit_options:
    st.success("✅ مقاسات الفرخ المناسبة:")
    for sw, sh, total_fit in best_fit_options:
        st.write(f"- {sw} × {sh} سم → عدد النسخ في الفرخ: {total_fit}")
    # نختار أول خيار كاقتراح رئيسي
    sw, sh, total_fit = best_fit_options[0]
else:
    st.error("❌ المقاس المطلوب لا يناسب مقاسات الأفرخ القياسية")
    total_fit = 0

# --------------------------
# مقاس القص النهائي وطريقة القص
# --------------------------
if total_fit > 0:
    cut_size = f"{width} × {height} سم"
    if total_fit <= 2:
        cut_method = "نص فرخ"
    elif total_fit <= 4:
        cut_method = "ربع فرخ"
    elif total_fit <= 8:
        cut_method = "تمن فرخ"
    else:
        cut_method = "مخصص"
else:
    cut_size = "غير متاح"
    cut_method = "غير متاح"

# --------------------------
# عرض النتائج
# --------------------------
if total_fit > 0:
    st.markdown("### 📊 النتيجة النهائية")
    result_data = {
        "النوع": job_type,
        "المقاس النسخة (سم)": cut_size,
        "الكمية": quantity,
        "نوع الورق": paper_type,
        "جرام الورق": paper_gram,
        "ألوان الطباعة": colors,
        "التشطيب": ", ".join(
            [opt for opt, chk in [("سلوفان", lamination), ("تجليد/سلك", binding), ("تكسير", die_cut)] if chk]
        ) or "بدون",
        "مقاس الفرخ": f"{sw} × {sh} سم",
        "عدد النسخ في الفرخ": total_fit,
        "طريقة القص": cut_method
    }
    df = pd.DataFrame([result_data])
    st.table(df)

    # --------------------------
    # زر تنزيل Excel بدون ظهور رموز
    # --------------------------
    output = io.BytesIO()
    df.to_excel(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    st.download_button(
        label="⬇️ تحميل النتيجة Excel",
        data=output,
        file_name="print_job.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
