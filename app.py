import streamlit as st

from database import (
    create_tables,
    add_student,
    get_students,
    update_student,
    delete_student,
    add_marks,
    get_marks,
    delete_marks
)

from calculations import (
    get_grade,
    calculate_sgpa
)


# -------------------- PAGE SETUP --------------------

st.set_page_config(
    page_title="Student Management App",
    page_icon="🎓",
    layout="wide"
)

create_tables()

st.title("🎓 Student Management System")

st.write(
    "Add students, manage their details, "
    "and calculate subject grades and SGPA."
)

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Student",
        "View / Update Students",
        "Add Marks",
        "View Marks & SGPA",
        "Delete Subject",
        "Delete Student"
    ]
)

students_data = get_students()


# -------------------- DASHBOARD --------------------

if menu == "Dashboard":

    st.header("Dashboard")

    total_students = len(students_data)

    total_subjects = sum(
        len(get_marks(student[0]))
        for student in students_data
    )

    col1, col2 = st.columns(2)

    col1.metric("Total Students", total_students)
    col2.metric("Total Subject Records", total_subjects)

    if students_data:

        st.subheader("Student Records")

        for student in students_data:

            st.write(f"Student ID: {student[0]}")
            st.write(f"Name: {student[1]}")
            st.write(f"Email: {student[2]}")
            st.write(f"Course: {student[3]}")

            st.divider()

    else:

        st.info("No students added yet.")


# -------------------- ADD STUDENT --------------------

elif menu == "Add Student":

    st.header("Add Student")

    with st.form("add_student_form", clear_on_submit=True):

        name = st.text_input("Student name")
        email = st.text_input("Email")
        course = st.text_input("Course")

        submitted = st.form_submit_button("Add Student")

        if submitted:

            if not name.strip():

                st.error("Please enter the student's name.")

            else:

                add_student(
                    name.strip(),
                    email.strip(),
                    course.strip()
                )

                st.success("Student added successfully.")

                st.rerun()


# -------------------- VIEW / UPDATE STUDENTS --------------------

elif menu == "View / Update Students":

    st.header("View / Update Students")

    if not students_data:

        st.info("No students added yet.")

    else:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students_data
        }

        selected_student = st.selectbox(
            "Select student",
            list(student_options.keys())
        )

        student_id = student_options[selected_student]

        student = next(
            s for s in students_data
            if s[0] == student_id
        )

        with st.form("update_student_form"):

            name = st.text_input(
                "Student name",
                value=student[1] or ""
            )

            email = st.text_input(
                "Email",
                value=student[2] or ""
            )

            course = st.text_input(
                "Course",
                value=student[3] or ""
            )

            submitted = st.form_submit_button("Update Student")

            if submitted:

                if not name.strip():

                    st.error("Student name cannot be empty.")

                else:

                    update_student(
                        student_id,
                        name.strip(),
                        email.strip(),
                        course.strip()
                    )

                    st.success(
                        "Student details updated successfully."
                    )

                    st.rerun()

        st.subheader("All Students")

        for student in students_data:

            st.write(f"Student ID: {student[0]}")
            st.write(f"Name: {student[1]}")
            st.write(f"Email: {student[2]}")
            st.write(f"Course: {student[3]}")

            st.divider()


# -------------------- ADD MARKS --------------------

elif menu == "Add Marks":

    st.header("Add Subject Marks")

    if not students_data:

        st.info("Add a student before entering marks.")

    else:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students_data
        }

        selected_student = st.selectbox(
            "Select student",
            list(student_options.keys())
        )

        student_id = student_options[selected_student]

        with st.form("add_marks_form", clear_on_submit=True):

            subject = st.text_input("Subject name")

            marks = st.number_input(
                "Marks",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0
            )

            credits = st.number_input(
                "Credits",
                min_value=0.5,
                max_value=20.0,
                value=3.0,
                step=0.5
            )

            submitted = st.form_submit_button("Add Marks")

            if submitted:

                if not subject.strip():

                    st.error("Please enter a subject name.")

                else:

                    add_marks(
                        student_id,
                        subject.strip(),
                        marks,
                        credits
                    )

                    st.success("Marks added successfully.")

                    st.rerun()


# -------------------- VIEW MARKS & SGPA --------------------

elif menu == "View Marks & SGPA":

    st.header("View Marks and Calculate SGPA")

    if not students_data:

        st.info("No students added yet.")

    else:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students_data
        }

        selected_student = st.selectbox(
            "Select student",
            list(student_options.keys())
        )

        student_id = student_options[selected_student]

        marks_data = get_marks(student_id)

        if marks_data:

            st.subheader("Subject Details")

            for mark in marks_data:

                st.write(f"Subject: {mark[1]}")
                st.write(f"Marks: {mark[2]}")
                st.write(f"Credits: {mark[3]}")
                st.write(f"Grade: {get_grade(mark[2])}")

                st.divider()

            st.metric(
                "SGPA",
                calculate_sgpa(marks_data)
            )

        else:

            st.info("No marks added for this student.")


# -------------------- DELETE SUBJECT --------------------

elif menu == "Delete Subject":

    st.header("Delete Subject")

    if not students_data:

        st.info("No students added yet.")

    else:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students_data
        }

        selected_student = st.selectbox(
            "Select student",
            list(student_options.keys())
        )

        student_id = student_options[selected_student]

        marks_data = get_marks(student_id)

        if marks_data:

            mark_options = {
                f"{mark[1]} - {mark[2]} marks": mark[0]
                for mark in marks_data
            }

            selected_mark = st.selectbox(
                "Select subject",
                list(mark_options.keys())
            )

            mark_id = mark_options[selected_mark]

            if st.button("Delete Subject"):

                delete_marks(mark_id)

                st.success("Subject deleted successfully.")

                st.rerun()

        else:

            st.info("No marks added for this student.")


# -------------------- DELETE STUDENT --------------------

elif menu == "Delete Student":

    st.header("Delete Student")

    if students_data:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students_data
        }

        selected_student = st.selectbox(
            "Select student to delete",
            list(student_options.keys())
        )

        student_id = student_options[selected_student]

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button(
            "Delete Student",
            disabled=not confirm
        ):

            delete_student(student_id)

            st.success("Student deleted successfully.")

            st.rerun()

    else:

        st.info("No students available to delete.")
