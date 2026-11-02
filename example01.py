import streamlit as st

st.set_page_config(page_title="Grade Compass", page_icon="🎓")


def letter_grade(average, scale):
    thresholds = (90, 80, 70, 60) if scale == 0 else (85, 75, 65, 50)
    for cutoff, letter in zip(thresholds, "ABCD"):
        if average >= cutoff:
            return letter
    return "F"


language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])
ar = language == "العربية"


def t(en, arabic):
    return arabic if ar else en


st.title(t("🎓 Grade Compass", "🎓 بوصلة الدرجات"))
st.subheader(t("Four subjects. One clear result.", "أربع مواد ونتيجة واضحة."))
st.markdown(t(
    "### How to use\n- Enter your name and four scores out of 100.\n- Choose a grading scale.\n- Click Calculate to see your average and letter grade.",
    "### طريقة الاستخدام\n- أدخل اسمك ودرجات أربع مواد من 100.\n- اختر سلم التقديرات.\n- اضغط احسب لعرض المتوسط والتقدير."
))
st.info(t("Demo scales only: these are not official university policies. All subjects have equal weight.",
          "سلالم تجريبية وليست لوائح جامعية رسمية. جميع المواد لها نفس الوزن."))

name = st.text_input(t("Student name", "اسم الطالب"))
level = st.selectbox(t("Study level", "المرحلة الدراسية"),
                     [t("School", "مدرسة"), t("University", "جامعة"), t("Other", "أخرى")])
subjects = [t("Mathematics", "الرياضيات"), t("Programming", "البرمجة"),
            t("English", "اللغة الإنجليزية"), t("Science", "العلوم")]
scores = []
for i, subject in enumerate(subjects):
    scores.append(st.number_input(subject, min_value=0.0, max_value=100.0,
                                  value=0.0, step=0.5, key=f"score_{i}"))
scale = st.radio(t("Grading scale", "سلم التقديرات"), [0, 1],
                 format_func=lambda x: t("Scale A", "السلم أ") if x == 0 else t("Scale B", "السلم ب"))
st.caption("A ≥ 90 | B ≥ 80 | C ≥ 70 | D ≥ 60 | F < 60" if scale == 0
           else "A ≥ 85 | B ≥ 75 | C ≥ 65 | D ≥ 50 | F < 50")
show_details = st.checkbox(t("Show subject breakdown", "عرض تفاصيل المواد"), value=True)
confirmed = st.checkbox(t("I have checked all four scores", "راجعت درجات المواد الأربع"))

if st.button(t("Calculate", "احسب"), type="primary"):
    if not name.strip():
        st.error(t("Please enter your name.", "يرجى إدخال اسمك."))
    elif not confirmed:
        st.warning(t("Please check your scores and tick the confirmation box.",
                     "يرجى مراجعة الدرجات وتحديد مربع التأكيد."))
    else:
        average = sum(scores) / 4
        grade = letter_grade(average, scale)
        st.markdown(t("### Your results", "### نتيجتك"))
        st.write(t("Student:", "الطالب:"), name.strip())
        st.write(t("Study level:", "المرحلة الدراسية:"), level)
        st.metric(t("Average", "المتوسط"), f"{average:.2f}%")
        message = t(f"Letter grade: {grade}", f"التقدير: {grade}")
        if grade in ("A", "B"):
            st.success(message)
        elif grade in ("C", "D"):
            st.warning(message)
        else:
            st.error(message)
        if show_details:
            rows = "\n".join(f"| {subject} | {score:.2f} / 100 |" for subject, score in zip(subjects, scores))
            st.markdown(t("| Subject | Score |", "| المادة | الدرجة |") + "\n|---|---|\n" + rows)
        st.caption(t("Average = sum of four scores ÷ 4. Grade uses the unrounded average.",
                     "المتوسط = مجموع الدرجات الأربع ÷ 4. يُحسب التقدير قبل تقريب المتوسط."))
