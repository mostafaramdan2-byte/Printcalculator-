import streamlit as st
import math

st.set_page_config(page_title="حاسبة الطباعة الأوفست", page_icon="🖨️", layout="centered")

st.title("🖨️ حاسبة الطباعة الأوفست")
st.write("أدخل بيانات المطبوع وسيتم حساب عدد الأفرخ والتكلفة تلقائيًا.")

# ✅ إدخال بيانات المطبوع
st.header("📄 بيانات المطبوع")
copies = st.number_input("عدد النسخ المطلوبة", min_value=1, step=1, value=1000)
width = st.number_input("عرض المطبوع (سم)", min_value=1, step=1, value=21)
height = st.number_input("طول المطبوع (سم)", min_value=1, step=1, value=29)

# ✅ مواصفات الورق
st.header("📏 مواصفات ورق الأساس")
base_size = st.selectbox("مقاس ورق الأساس", ["70×100", "88×44"])
paper_price = st.number_input("سعر الفرخ الواحد (جنيه)", min_value=0.0, step=0.5, value=5.0)
print_price = st.number_input("تكلفة الطباعة للفرخ (جنيه)", min_value=0.0, step=0.5, value=3.0)

# تحديد أبعاد الورق الأساس
if base_size == "70×100":
    base_w, base_h = 70, 100
else:
    base_w, base_h = 88, 44

# ✅ حساب عدد النسخ في الفرخ
copies_per_sheet = (base_w // width) * (base_h // height)
if copies_per_sheet == 0:
    st.error("⚠️ المقاس المدخل أكبر من ورق الأساس!")
else:
    total_sheets = math.ceil(copies / copies_per_sheet)

    # ✅ حساب التكلفة
    total_paper_cost = total_sheets * paper_price
    total_print_cost = total_sheets * print_price
    total_cost = total_paper_cost + total_print_cost

    # ✅ عرض النتائج
    st.header("📊 النتائج")
    st.success(f"عدد النسخ في الفرخ الواحد: {copies_per_sheet}")
    st.success(f"عدد الأفرخ المطلوبة: {total_sheets}")
    st.info(f"إجمالي تكلفة الورق: {total_paper_cost:.2f} جنيه")
    st.info(f"إجمالي تكلفة الطباعة: {total_print_cost:.2f} جنيه")
    st.success(f"💰 التكلفة الكلية: {total_cost:.2f} جنيه")
