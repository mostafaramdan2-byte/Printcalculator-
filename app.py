import streamlit as st
import math
import pandas as pd
import io
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, NamedStyle
from openpyxl.utils import get_column_letter

st.set_page_config(page_title="🖨️ برنامج حساب الطباعة A-Z", layout="wide")
st.title("🖨️ برنامج حساب الطباعة A-Z")

# -------------------------
# إعدادات أسعار الورق الافتراضية
# -------------------------
paper_types = {
    "كوشيه": 3.0,
    "دوبلكس": 2.8,
    "أبيض": 2.2,
    "جريدا": 1.6
}

# اختيار نوع المطبوع وورق والأساس
product_type = st.selectbox("اختر نوع المطبوع", ["نوت بوك", "كتالوج/مجلة", "منيو", "فلاير/بروشور"])
paper_size = st.selectbox("اختر مقاس الورق الأساس", ["70x100", "88x44"])
if paper_size == "70x100":
    sheet_width, sheet_height = 70, 100
else:
    sheet_width, sheet_height = 88, 44

paper_choice = st.selectbox("اختر نوع الورق", list(paper_types.keys()))
paper_cost_default = paper_types[paper_choice]
paper_cost = st.number_input("سعر الفرخ (جنيه) — يمكنك تغييره", min_value=0.0, value=float(paper_cost_default))

st.markdown("---")

# بيانات الإدخال المتغيرة بحسب النوع
results = {}
inputs = {}

# --------- نوت بوك ----------
if product_type == "نوت بوك":
    st.header("📒 إعدادات النوت بوك")
    num_notebooks = st.number_input("عدد النسخ", min_value=1, value=100)
    pages_per_notebook = st.number_input("عدد الأوراق الداخلية لكل نسخة", min_value=1, value=50)
    width = st.number_input("عرض النوت (سم)", min_value=1, value=14)
    height = st.number_input("ارتفاع النوت (سم)", min_value=1, value=20)

    # خيارات إضافية
    cover_paper_cost = st.number_input("سعر فرخ الغلاف (جنيه)", min_value=0.0, value=5.0)
    lamination = st.selectbox("هل يوجد سلوفان على الغلاف؟", ["لا", "لامع", "مطفي"])
    lamination_cost_per_cover = 0.0
    if lamination != "لا":
        lamination_cost_per_cover = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=1.0)
    inside_print_cost = st.number_input("تكلفة طباعة الورق الداخلي للفرخ (جنيه)", min_value=0.0, value=1.0)
    cover_print_cost = st.number_input("تكلفة طباعة الغلاف للفرخ (جنيه)", min_value=0.0, value=3.0)
    spiral_cost_per_piece = st.number_input("تكلفة عقلة السلك (جنيه)", min_value=0.0, value=2.0)

    # حسابات
    total_pages = num_notebooks * pages_per_notebook
    fit_per_sheet = max((sheet_width // width) * (sheet_height // height), 1)
    total_sheets = math.ceil(total_pages / fit_per_sheet)
    total_paper_cost = total_sheets * paper_cost

    cover_fit = max((sheet_width // width) * (sheet_height // height), 1)
    cover_sheets = math.ceil(num_notebooks / cover_fit)
    cover_total_cost = cover_sheets * cover_paper_cost

    lamination_cost = lamination_cost_per_cover * num_notebooks if lamination != "لا" else 0.0
    total_inside_print_cost = inside_print_cost * total_sheets
    total_cover_print_cost = cover_print_cost * cover_sheets
    total_spiral_cost = num_notebooks * spiral_cost_per_piece

    grand_total = total_paper_cost + cover_total_cost + lamination_cost + total_inside_print_cost + total_cover_print_cost + total_spiral_cost
    cost_per_notebook = grand_total / num_notebooks

    # حفظ النتائج
    inputs = {
        "نوع المطبوع": product_type,
        "عدد النسخ": num_notebooks,
        "عدد أوراق كل نسخة": pages_per_notebook,
        "مقاس (سم)": f"{width}x{height}",
        "نوع الورق": paper_choice,
        "سعر الفرخ": paper_cost
    }
    results = {
        "عدد الأفرخ الداخلي (فرخ)": total_sheets,
        "عدد أفرخ الغلاف (فرخ)": cover_sheets,
        "تكلفة ورق داخلي (جنيه)": total_paper_cost,
        "تكلفة ورق غلاف (جنيه)": cover_total_cost,
        "تكلفة السلوفان (جنيه)": lamination_cost,
        "تكلفة طباعة داخلي (جنيه)": total_inside_print_cost,
        "تكلفة طباعة غلاف (جنيه)": total_cover_print_cost,
        "تكلفة السلك (جنيه)": total_spiral_cost,
        "التكلفة الكلية (جنيه)": grand_total,
        "تكلفة النسخة الواحدة (جنيه)": cost_per_notebook
    }

# --------- كتالوج / مجلة ----------
elif product_type == "كتالوج/مجلة":
    st.header("📖 إعدادات الكتالوج / المجلة")
    num_catalogs = st.number_input("عدد النسخ", min_value=1, value=500)
    pages_per_catalog = st.number_input("عدد الصفحات الداخلية", min_value=4, value=40)
    width = st.number_input("عرض الكتالوج (سم)", min_value=1, value=21)
    height = st.number_input("ارتفاع الكتالوج (سم)", min_value=1, value=29)

    cover_paper_cost = st.number_input("سعر فرخ الغلاف (جنيه)", min_value=0.0, value=6.0)
    lamination = st.selectbox("هل يوجد سلوفان على الغلاف؟", ["لا", "لامع", "مطفي"])
    lamination_cost_per_cover = 0.0
    if lamination != "لا":
        lamination_cost_per_cover = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=1.5)

    inside_print_cost = st.number_input("تكلفة طباعة الصفحات الداخلية (جنيه للفرخ)", min_value=0.0, value=1.0)
    cover_print_cost = st.number_input("تكلفة طباعة الغلاف للفرخ (جنيه)", min_value=0.0, value=4.0)

    binding_type = st.selectbox("طريقة التجليد", ["دبوس", "كعب حراري", "سلك لولبي"])
    binding_cost_per_copy = 0.0
    if binding_type == "دبوس":
        binding_cost_per_copy = st.number_input("تكلفة تدبيس النسخة (جنيه)", min_value=0.0, value=0.5)
    elif binding_type == "كعب حراري":
        binding_cost_per_copy = st.number_input("تكلفة الكعب الحراري للنسخة (جنيه)", min_value=0.0, value=1.5)
    else:
        binding_cost_per_copy = st.number_input("تكلفة السلك لكل نسخة (جنيه)", min_value=0.0, value=2.0)

    # حسابات
    total_pages = num_catalogs * pages_per_catalog
    fit_per_sheet = max((sheet_width // width) * (sheet_height // height) * 2, 1)  # نحتسب وجهين
    total_sheets = math.ceil(total_pages / fit_per_sheet)
    total_paper_cost = total_sheets * paper_cost

    cover_fit = max((sheet_width // width) * (sheet_height // height), 1)
    cover_sheets = math.ceil(num_catalogs / cover_fit)
    cover_total_cost = cover_sheets * cover_paper_cost

    lamination_cost = lamination_cost_per_cover * num_catalogs if lamination != "لا" else 0.0
    total_inside_print_cost = inside_print_cost * total_sheets
    total_cover_print_cost = cover_print_cost * cover_sheets
    total_binding_cost = binding_cost_per_copy * num_catalogs

    grand_total = total_paper_cost + cover_total_cost + lamination_cost + total_inside_print_cost + total_cover_print_cost + total_binding_cost
    cost_per_catalog = grand_total / num_catalogs

    inputs = {
        "نوع المطبوع": product_type,
        "عدد النسخ": num_catalogs,
        "عدد الصفحات": pages_per_catalog,
        "مقاس (سم)": f"{width}x{height}",
        "نوع الورق": paper_choice,
        "سعر الفرخ": paper_cost
    }
    results = {
        "عدد الأفرخ الداخلي (فرخ)": total_sheets,
        "عدد أفرخ الغلاف (فرخ)": cover_sheets,
        "تكلفة ورق داخلي (جنيه)": total_paper_cost,
        "تكلفة ورق غلاف (جنيه)": cover_total_cost,
        "تكلفة السلوفان (جنيه)": lamination_cost,
        "تكلفة طباعة داخلي (جنيه)": total_inside_print_cost,
        "تكلفة طباعة غلاف (جنيه)": total_cover_print_cost,
        "تكلفة التجليد (جنيه)": total_binding_cost,
        "التكلفة الكلية (جنيه)": grand_total,
        "تكلفة النسخة الواحدة (جنيه)": cost_per_catalog
    }

# --------- منيو ----------
elif product_type == "منيو":
    st.header("🍽️ إعدادات المنيو")
    num_menus = st.number_input("عدد النسخ", min_value=1, value=500)
    pages_per_menu = st.number_input("عدد الصفحات", min_value=1, value=2)
    width = st.number_input("عرض المنيو (سم)", min_value=1, value=21)
    height = st.number_input("ارتفاع المنيو (سم)", min_value=1, value=29)

    has_cover = st.selectbox("هل يوجد غلاف منفصل؟", ["لا", "نعم"])
    cover_paper_cost = 0.0
    cover_sheets = 0
    if has_cover == "نعم":
        cover_paper_cost = st.number_input("سعر فرخ الغلاف (جنيه)", min_value=0.0, value=5.0)

    lamination = st.selectbox("هل يوجد سلوفان؟", ["لا", "لامع", "مطفي"])
    lamination_cost_per_copy = 0.0
    if lamination != "لا":
        lamination_cost_per_copy = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=0.5)

    inside_print_cost = st.number_input("تكلفة طباعة الفرخ (جنيه)", min_value=0.0, value=1.5)

    # حسابات
    total_pages = num_menus * pages_per_menu
    fit_per_sheet = max((sheet_width // width) * (sheet_height // height), 1)
    total_sheets = math.ceil(total_pages / fit_per_sheet)
    total_paper_cost = total_sheets * paper_cost

    if has_cover == "نعم":
        cover_fit = max((sheet_width // width) * (sheet_height // height), 1)
        cover_sheets = math.ceil(num_menus / cover_fit)
        cover_total_cost = cover_sheets * cover_paper_cost
    else:
        cover_total_cost = 0.0

    lamination_cost = lamination_cost_per_copy * num_menus if lamination != "لا" else 0.0
    total_print_cost = inside_print_cost * total_sheets

    grand_total = total_paper_cost + cover_total_cost + lamination_cost + total_print_cost
    cost_per_menu = grand_total / num_menus

    inputs = {
        "نوع المطبوع": product_type,
        "عدد النسخ": num_menus,
        "صفحات كل نسخة": pages_per_menu,
        "مقاس (سم)": f"{width}x{height}",
        "نوع الورق": paper_choice,
        "سعر الفرخ": paper_cost
    }
    results = {
        "عدد الأفرخ المطلوب (فرخ)": total_sheets,
        "عدد أفرخ الغلاف (فرخ)": cover_sheets,
        "تكلفة ورق (جنيه)": total_paper_cost,
        "تكلفة غلاف (جنيه)": cover_total_cost,
        "تكلفة السلوفان (جنيه)": lamination_cost,
        "تكلفة الطباعة (جنيه)": total_print_cost,
        "التكلفة الكلية (جنيه)": grand_total,
        "تكلفة النسخة الواحدة (جنيه)": cost_per_menu
    }

# --------- فلاير / بروشور ----------
elif product_type == "فلاير/بروشور":
    st.header("📄 إعدادات الفلاير / البروشور")
    num_flyers = st.number_input("عدد النسخ", min_value=1, value=1000)
    width = st.number_input("عرض الفلاير (سم)", min_value=1, value=10)
    height = st.number_input("ارتفاع الفلاير (سم)", min_value=1, value=20)

    finishing = st.multiselect("اختر التشطيب المطلوب", ["قص", "سلوفان لامع", "سلوفان مطفي"])
    cut_cost = 0.0
    lam_cost_each = 0.0
    if "قص" in finishing:
        cut_cost = st.number_input("تكلفة القص لكل نسخة (جنيه)", min_value=0.0, value=0.1)
    if "سلوفان لامع" in finishing or "سلوفان مطفي" in finishing:
        lam_cost_each = st.number_input("تكلفة السلوفان لكل نسخة (جنيه)", min_value=0.0, value=0.5)

    inside_print_cost = st.number_input("تكلفة طباعة الفرخ (جنيه)", min_value=0.0, value=1.0)

    # حسابات
    fit_per_sheet = max((sheet_width // width) * (sheet_height // height), 1)
    total_sheets = math.ceil(num_flyers / fit_per_sheet)
    total_paper_cost = total_sheets * paper_cost
    total_print_cost = inside_print_cost * total_sheets
    finishing_cost = (cut_cost + lam_cost_each) * num_flyers

    grand_total = total_paper_cost + total_print_cost + finishing_cost
    cost_per_flyer = grand_total / num_flyers

    inputs = {
        "نوع المطبوع": product_type,
        "عدد النسخ": num_flyers,
        "مقاس (سم)": f"{width}x{height}",
        "نوع الورق": paper_choice,
        "سعر الفرخ": paper_cost
    }
    results = {
        "عدد الأفرخ المطلوب (فرخ)": total_sheets,
        "تكلفة ورق (جنيه)": total_paper_cost,
        "تكلفة الطباعة (جنيه)": total_print_cost,
        "تكلفة التشطيب (جنيه)": finishing_cost,
        "التكلفة الكلية (جنيه)": grand_total,
        "تكلفة النسخة الواحدة (جنيه)": cost_per_flyer
    }

# -------------------------
# عرض النتائج في الواجهة
# -------------------------
st.subheader("📊 النتائج السريعة")
if results:
    left, right = st.columns([1, 1])
    with left:
        st.markdown("**تفاصيل الإدخال**")
        for k, v in inputs.items():
            st.write(f"- **{k}**: {v}")
    with right:
        st.markdown("**مخرجات الحساب**")
        for k, v in results.items():
            if isinstance(v, float):
                st.write(f"- **{k}**: {v:,.2f} جنيه")
            else:
                st.write(f"- **{k}**: {v}")

st.markdown("---")

# ----------------------------------
# تصدير إلى Excel منسق احترافياً
# ----------------------------------
def generate_excel(inputs: dict, results: dict, project_name: str = "Print Report"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # DataFrames to write
    df_inputs = pd.DataFrame(list(inputs.items()), columns=["حقل", "قيمة"])
    df_results = pd.DataFrame(list(results.items()), columns=["معلومة", "قيمة"])

    # استخدم بايت بافر
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # نكتب جداول
        df_inputs.to_excel(writer, sheet_name="تقرير", index=False, startrow=6)
        df_results.to_excel(writer, sheet_name="تقرير", index=False, startrow=6, startcol=3)

        # معلومات الرأس
        wb = writer.book
        ws = wb["تقرير"]
        ws["A1"] = "تقرير تكلفة الطباعة"
        ws["A2"] = f"المشروع: {project_name}"
        ws["A3"] = f"التاريخ: {timestamp}"

        # تنسيقات جاهزة
        header_font = Font(size=14, bold=True)
        ws["A1"].font = header_font
        ws["A1"].alignment = Alignment(horizontal="center")
        # جعل العنوان يمتد عبر أعمدة
        ws.merge_cells("A1:F1")

        # هيدر جدول
        header_fill = PatternFill("solid", fgColor="4F4F4F")  # رمادي غامق
        header_font_white = Font(color="FFFFFF", bold=True)

        thin = Side(border_style="thin", color="000000")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        # Find header rows (pandas wrote headers في row 7 و col A and D)
        # Apply style to headers of both tables
        for col in range(1, 3):  # A,B
            cell = ws.cell(row=7, column=col)
            cell.fill = header_fill
            cell.font = header_font_white
            cell.alignment = Alignment(horizontal="center")
            cell.border = border
        for col in range(4, 6):  # D,E
            cell = ws.cell(row=7, column=col)
            cell.fill = header_fill
            cell.font = header_font_white
            cell.alignment = Alignment(horizontal="center")
            cell.border = border

        # Apply border and number format to value cells
        # inputs values
        for r in range(8, 8 + len(df_inputs)):
            # حقل (A) ، قيمة (B)
            cell_key = ws.cell(row=r, column=1)
            cell_val = ws.cell(row=r, column=2)
            cell_key.border = border
            cell_val.border = border
            cell_key.alignment = Alignment(horizontal="right")
            cell_val.alignment = Alignment(horizontal="left")
        # results values (D,E)
        for r in range(8, 8 + len(df_results)):
            cell_key = ws.cell(row=r, column=4)
            cell_val = ws.cell(row=r, column=5)
            cell_key.border = border
            cell_val.border = border
            cell_key.alignment = Alignment(horizontal="right")
            cell_val.alignment = Alignment(horizontal="left")
            # لو القيمة رقمية - نضبط تنسيق العملة
            try:
                val = float(cell_val.value)
                cell_val.number_format = '#,##0.00 "جنيه"'
            except Exception:
                pass

        # تعديل عرض الأعمدة
        for i, width in enumerate([30, 20, 3, 30, 20], start=1):
            ws.column_dimensions[get_column_letter(i)].width = width

        # حفظ وارجاع البايت
        wb.save(output)

    output.seek(0)
    return output

if results:
    project_name_input = st.text_input("اسم المشروع للتقرير (سيضاف داخل ملف Excel)", value=f"{product_type} - printing-calculator")
    if st.button("⬇️ تصدير التقرير لملف Excel (منسق احترافي)"):
        excel_bytes = generate_excel(inputs, results, project_name_input)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{product_type.replace(' ', '_')}_report_{ts}.xlsx"
        st.download_button(
            label="تحميل ملف Excel",
            data=excel_bytes,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.caption("تم التصميم ليعمل محليًا وعلى Streamlit Cloud. تأكد من وجود الحزم المطلوبة في requirements.txt")
