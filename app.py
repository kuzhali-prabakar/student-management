import streamlit as st
import sqlite3
import pandas as pd

def get_db_connection():
    conn = sqlite3.connect('students.db')
    return conn

conn = get_db_connection()
conn.execute('''
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
course TEXT,
grade TEXT
)
''')
conn.commit()

st.title("Student Management System")

menu = ["View Students","Add Student","Update Student","Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Students":
    st.subheader("Student List")
    data = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(data)


elif choice == "Add Student":
    st.subheader("Add Student")

    name = st.text_input("Name")
    age = st.number_input("Age", 1,100)
    course = st.text_input("Course")
    grade = st.text_input("Grade")

    if st.button("Add Student"):
        conn.execute(
        "INSERT INTO students (name,age,course,grade) VALUES (?,?,?,?)",
        (name,age,course,grade)
        )
        conn.commit()
        st.success("Student Added Successfully")

elif choice == "Update Student":
    st.subheader("Update Student")

    data = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(data)

    student_id = st.number_input("Enter Student ID",1)

    name = st.text_input("New Name")
    age = st.number_input("New Age",1,100)
    course = st.text_input("New Course")
    grade = st.text_input("New Grade")

    if st.button("Update"):
        conn.execute(
        "UPDATE students SET name=?,age=?,course=?,grade=? WHERE id=?",
        (name,age,course,grade,student_id)
        )
        conn.commit()
        st.success("Student Updated")


elif choice == "Delete Student":
    st.subheader("Delete Student")

    data = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(data)

    student_id = st.number_input("Enter Student ID to Delete",1)

    if st.button("Delete"):
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        st.success("Student Deleted")