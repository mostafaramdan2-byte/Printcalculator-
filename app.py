import streamlit as st
import math

st.title("🖨️ برنامج حساب الطباعة A-Z")

# اختيار نوع المطبوع
product_type = st.selectbox("اختر نوع المطبوع", ["نوت بوك", "كتالوج/مجلة", "منيو", "فلاير/بروشور"])

# اختيار مقاس الورق الأساس
paper_size = st.selectbox("اختر مقاس الورق الأساس", ["70x100", "88x44"])
if paper_size == "70x100":
    sheet_width, sheet_height = 70, 100
else:
    sheet_width, sheet_height = 88, 44

# ------------------------------
# 📒 النوت بوك
# ------------------------------
if product_type == "نوت بوك":
    num_notebooks = st.number_input("عدد النسخ", min_value=1, value=100)
    pages_per_notebook = st.number_input("عدد الأوراق الداخلية لكل نسخة", min_value=1, value=50)
    width = st.number_input("عرض النوت (سم)", min_value=1, value=14)
    height = st.number_input("ارتفاع النوت (سم)", min_value=1, value=20)

    # الورق الداخلي
    total_pages = num_notebooks * pages_per_notebook
    fit_per_sheet = (sheet_width // width) * (sheet_height // height)
    fit_per_sheet = max(fit_per_sheet, 1)
    total_sheets = math.ceil(total_pages / fit_per_sheet)

    paper_cost = st.number_input("سعر الفرخ للورق الداخلي (جنيه)", min_value=0.0, value=2.0)
    total_paper_cost = total_sheets * paper_cost

    # الغلاف
    cover_paper_cost = st.number_input("سعر فرخ الغلاف (جنيه)", min_value=0.0, value=5.0)
    cover_fit = (sheet_width // width) * (sheet_height // height)
    cover_fit = max(cover_fit, 1)
    cover_sheets = math.ceil(num_notebooks / cover_fit)
    cover_total_cost = cover_sheets * cover_paper_cost

    # السلوفان
    lamination = st.selectbox("هل يوجد سلوفان على الغلاف؟", ["لا", "لامع", "مطفي"])
    lamination_cost = 0
    if lamination != "لا":
        lamination_cost_per_cover = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=1.0)
        lamination_cost = lamination_cost_per_cover * num_notebooks

    # الطباعة
    inside_print_cost = st.number_input("تكلفة طباعة الورق الداخلي للفرخ (جنيه)", min_value=0.0, value=1.0)
    total_inside_print_cost = inside_print_cost * total_sheets

    cover_print_cost = st.number_input("تكلفة طباعة الغلاف للفرخ (جنيه)", min_value=0.0, value=3.0)
    total_cover_print_cost = cover_print_cost * cover_sheets

    # السلك الحلزوني
    spirals_needed = num_notebooks
    spiral_cost_per_piece = st.number_input("تكلفة عقلة السلك (جنيه)", min_value=0.0, value=2.0)
    total_spiral_cost = spirals_needed * spiral_cost_per_piece

    # الإجمالي
    grand_total = (
        total_paper_cost +
        cover_total_cost +
        lamination_cost +
        total_inside_print_cost +
        total_cover_print_cost +
        total_spiral_cost
    )
    cost_per_notebook = grand_total / num_notebooks

    st.subheader("📊 النتائج")
    st.write(f"📄 عدد الأفرخ الداخلي: {total_sheets}")
    st.write(f"📘 عدد أفرخ الغلاف: {cover_sheets}")
    st.write(f"🌀 عدد عقل السلك: {spirals_needed}")
    st.write(f"💰 التكلفة الكلية: {grand_total:.2f} جنيه")
    st.write(f"💵 تكلفة النسخة الواحدة: {cost_per_notebook:.2f} جنيه")

# ------------------------------
# 📖 الكتالوج/المجلة
# ------------------------------
elif product_type == "كتالوج/مجلة":
    num_catalogs = st.number_input("عدد النسخ", min_value=1, value=500)
    pages_per_catalog = st.number_input("عدد الصفحات الداخلية", min_value=4, value=40)
    width = st.number_input("عرض الكتالوج (سم)", min_value=1, value=21)
    height = st.number_input("ارتفاع الكتالوج (سم)", min_value=1, value=29)

    total_pages = num_catalogs * pages_per_catalog
    fit_per_sheet = (sheet_width // width) * (sheet_height // height) * 2  # وجهين
    fit_per_sheet = max(fit_per_sheet, 1)
    total_sheets = math.ceil(total_pages / fit_per_sheet)

    inside_paper_cost = st.number_input("سعر الفرخ للورق الداخلي (جنيه)", min_value=0.0, value=2.0)
    total_inside_paper_cost = total_sheets * inside_paper_cost

    # الغلاف
    cover_paper_cost = st.number_input("سعر فرخ الغلاف (جنيه)", min_value=0.0, value=5.0)
    cover_fit = (sheet_width // width) * (sheet_height // height)
    cover_fit = max(cover_fit, 1)
    cover_sheets = math.ceil(num_catalogs / cover_fit)
    total_cover_paper_cost = cover_sheets * cover_paper_cost

    # الطباعة
    inside_print_cost = st.number_input("تكلفة طباعة الورق الداخلي للفرخ (جنيه)", min_value=0.0, value=1.0)
    total_inside_print_cost = inside_print_cost * total_sheets

    cover_print_cost = st.number_input("تكلفة طباعة الغلاف للفرخ (جنيه)", min_value=0.0, value=3.0)
    total_cover_print_cost = cover_print_cost * cover_sheets

    # السلوفان للغلاف
    lamination = st.selectbox("هل يوجد سلوفان للغلاف؟", ["لا", "لامع", "مطفي"])
    lamination_cost = 0
    if lamination != "لا":
        lamination_cost_per_copy = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=1.0)
        lamination_cost = lamination_cost_per_copy * num_catalogs

    # التجليد
    binding_type = st.selectbox("طريقة التجليد", ["دبوس", "كعب حراري", "سلك لولبي"])
    binding_cost_per_copy = 0
    if binding_type == "دبوس":
        binding_cost_per_copy = st.number_input("تكلفة تدبيس النسخة (جنيه)", min_value=0.0, value=0.5)
    elif binding_type == "كعب حراري":
        binding_cost_per_copy = st.number_input("تكلفة الكعب الحراري للنسخة (جنيه)", min_value=0.0, value=1.5)
    elif binding_type == "سلك لولبي":
        binding_cost_per_copy = st.number_input("تكلفة السلك لكل نسخة (جنيه)", min_value=0.0, value=2.0)
    total_binding_cost = binding_cost_per_copy * num_catalogs

    # الإجمالي
    grand_total = (
        total_inside_paper_cost +
        total_cover_paper_cost +
        total_inside_print_cost +
        total_cover_print_cost +
        lamination_cost +
        total_binding_cost
    )
    cost_per_catalog = grand_total / num_catalogs

    st.subheader("📊 النتائج")
    st.write(f"📄 عدد الأفرخ الداخلي: {total_sheets}")
    st.write(f"📘 عدد أفرخ الغلاف: {cover_sheets}")
    st.write(f"📌 تكلفة التجليد: {total_binding_cost:.2f} جنيه")
    st.write(f"💰 التكلفة الكلية: {grand_total:.2f} جنيه")
    st.write(f"💵 تكلفة النسخة الواحدة: {cost_per_catalog:.2f} جنيه")

# ------------------------------
# 🍽️ المنيو
# ------------------------------
elif product_type == "منيو":
    num_menus = st.number_input("عدد النسخ", min_value=1, value
