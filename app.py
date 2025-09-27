import streamlit as st
import pandas as pd

st.set_page_config(page_title="حاسبة تكلفة الطباعة", layout="wide")

st.title("🖨️ حاسبة تكلفة الطباعة A-Z")
st.markdown("برنامج شامل لحساب الورق والتكلفة، مقاس القص، وطريقة القص.")

# --------------------------
# بيانات أساسية
# --------------------------
job_type = st.selectbox("📌 اختر نوع المطبوع", ["نوت بوك", "منيو", "كتالوج", "فلاير", "بروشور", "مجلة", "فولدر", "أخرى"])

col1, col2 = st.columns(2)
with col1:
    width = st.number_input("العرض (سم)", min_value=1.0, step=0.5)
with col2:
    height = st.number_input("الطول (سم)", min_value=1.0, step=0.5)

quantity = st.number_input("عدد النسخ المطلوبة", min_value=1, step=1)

# --------------------------
# الورق
# --------------------------
paper_type = st.selectbox("📄 نوع الورق", ["كوشيه", "بريستول كوشيه", "ورق طبع"])
paper_gram = st.selectbox("📏 جرام الورق", list(range(90, 351, 10)))

# --------------------------
# الطباعة
# --------------------------
colors = st.radio("🎨 الطباعة", ["أبيض وأسود", "ألوان"])

# --------------------------
# التشطيب
# --------------------------
st.markdown("### ✂️ خدمات ما بعد الطباعة")
lamination = st.checkbox("سلوفان")
binding = st.checkbox("تجليد/سلك")
die_cut = st.checkbox("تكسير/قص خاص")

# --------------------------
# اقتراح مقاس الفرخ المناسب
# --------------------------
sheet_options = [(70, 100), (88, 44)]
best_fit = None
for sw, sh in sheet_options:
    fit_x = sw // width
    fit_y = sh // height
    total_fit = fit_x * fit_y
    if total_fit > 0:
        best_fit = (sw, sh, total_fit)
        break

if best_fit:
    sw, sh, total_fit = best_fit
    st.success(f"✅ أنسب مقاس الفرخ: {sw} × {sh} سم (عدد {total_fit} نسخة في الفرخ)")
else:
    total_fit = 0
    st.error("❌ المقاس المطلوب لا يناسب مقاسات الأفرخ القياسية")

# --------------------------
# حساب مقاس القص النهائي وطريقة القص
# --------------------------
if total_fit > 0:
    cut_width = sw // (sw // width)
    cut_height = sh // (sh // height)
    cut_size = f"{cut_width} × {cut_height} سم"

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
        "المقاس النسخة (سم)": f"{width} × {height}",
        "الكمية": quantity,
        "نوع الورق": paper_type,
        "جرام الورق": paper_gram,
        "ألوان الطباعة": colors,
        "التشطيب": ", ".join(
            [opt for opt, chk in [("سلوفان", lamination), ("تجليد/سلك", binding), ("تكسير", die_cut)] if chk]
        ) or "بدون",
        "مقاس الفرخ المناسب": f"{sw} × {sh} سم",
        "عدد النسخ في الفرخ": total_fit,
        "مقاس القص النهائي": cut_size,
        "طريقة القص": cut_method
    }
    df = pd.DataFrame([result_data])
    st.table(df)

    # زر تنزيل Excel
    output = "print_job.xlsx"
    df.to_excel(output, index=False)
    with open(output, "rb") as file:
        st.download_button("⬇️ تحميل النتيجة Excel", file, file_name="print_job.xlsx")
