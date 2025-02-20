import streamlit as st
import pandas as pd
import sqlite3

# Database connection
conn = sqlite3.connect("scholarships.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS scholarships (id INTEGER PRIMARY KEY, name TEXT, amount INTEGER, criteria TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS student_details (id INTEGER PRIMARY KEY, username TEXT, annual_income INTEGER, marks INTEGER, category TEXT)''')
conn.commit()

# Initialize session state
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["student_registered"] = False

# ----------------- HOME PAGE: Select User -----------------
if st.session_state["user_role"] is None:
    st.title("🎓 Scholarship Finder")
    role = st.radio("Choose your role:", ["Admin", "Student"])

    if st.button("Proceed to Login/Sign Up"):
        st.session_state["user_role"] = role
        st.experimental_rerun()

# ----------------- STUDENT REGISTRATION -----------------
elif st.session_state["user_role"] == "Student" and not st.session_state["authenticated"]:
    st.title("📝 Student Registration / Login")
    choice = st.radio("Do you have an account?", ["Yes (Login)", "No (Register)"])

    if choice == "No (Register)":
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")

        if st.button("Register"):
            cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
            if cursor.fetchone():
                st.error("Username already exists! Try another.")
            else:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'Student')", (new_username, new_password))
                conn.commit()
                st.success("Registration successful! Please login.")
    
    elif choice == "Yes (Login)":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role='Student'", (username, password))
            if cursor.fetchone():
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.experimental_rerun()
            else:
                st.error("Invalid login details!")

# ----------------- ADMIN LOGIN -----------------
elif st.session_state["user_role"] == "Admin" and not st.session_state["authenticated"]:
    st.title("🔑 Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role='Admin'", (username, password))
        if cursor.fetchone():
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Invalid admin credentials!")

# ----------------- ADMIN DASHBOARD -----------------
elif st.session_state["authenticated"] and st.session_state["user_role"] == "Admin":
    st.title("📊 Admin Dashboard")
    st.subheader("Manage Scholarships")

    # Add Scholarship
    with st.form("add_scholarship_form"):
        name = st.text_input("Scholarship Name")
        amount = st.number_input("Amount Provided", min_value=1000, step=1000)
        criteria = st.text_input("Eligibility Criteria")
        add_btn = st.form_submit_button("Add Scholarship")

        if add_btn:
            cursor.execute("INSERT INTO scholarships (name, amount, criteria) VALUES (?, ?, ?)", (name, amount, criteria))
            conn.commit()
            st.success("Scholarship added successfully!")

    # Display Scholarships
    st.subheader("Existing Scholarships")
    scholarships = cursor.execute("SELECT * FROM scholarships").fetchall()

    for s in scholarships:
        with st.expander(f"{s[1]} - ₹{s[2]}"):
            st.write(f"**Criteria:** {s[3]}")
            col1, col2 = st.columns(2)
            if col1.button(f"🗑️ Delete {s[1]}", key=f"delete_{s[0]}"):
                cursor.execute("DELETE FROM scholarships WHERE id=?", (s[0],))
                conn.commit()
                st.experimental_rerun()

# ----------------- STUDENT DETAILS PAGE -----------------
elif st.session_state["authenticated"] and st.session_state["user_role"] == "Student" and not st.session_state["student_registered"]:
    st.title("📋 Update Your Details")
    annual_income = st.number_input("Family Annual Income (₹)", min_value=0, step=5000)
    marks = st.slider("Marks (%)", min_value=0, max_value=100, value=50)
    category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority"])

    if st.button("Submit Details"):
        cursor.execute("INSERT INTO student_details (username, annual_income, marks, category) VALUES (?, ?, ?, ?)", 
                       (st.session_state["username"], annual_income, marks, category))
        conn.commit()
        st.session_state["student_registered"] = True
        st.experimental_rerun()

# ----------------- ELIGIBLE SCHOLARSHIPS PAGE -----------------
elif st.session_state["authenticated"] and st.session_state["user_role"] == "Student" and st.session_state["student_registered"]:
    st.title("🎉 Your Eligible Scholarships")

    # Get student details
    student = cursor.execute("SELECT * FROM student_details WHERE username=?", (st.session_state["username"],)).fetchone()
    if student:
        income, marks, category = student[2], student[3], student[4]

        # Fetch matching scholarships
        eligible_scholarships = cursor.execute("SELECT * FROM scholarships WHERE criteria LIKE ?", (f"%{category}%",)).fetchall()

        if eligible_scholarships:
            for s in eligible_scholarships:
                with st.expander(f"{s[1]} - ₹{s[2]}"):
                    st.write(f"**Criteria:** {s[3]}")
        else:
            st.warning("No scholarships match your criteria.")
    
    if st.button("🔄 Update Details"):
        st.session_state["student_registered"] = False
        st.experimental_rerun()

# ----------------- LOGOUT BUTTON -----------------
if st.session_state["authenticated"]:
    if st.button("🚪 Logout"):
        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None
        st.session_state["student_registered"] = False
        st.experimental_rerun()
