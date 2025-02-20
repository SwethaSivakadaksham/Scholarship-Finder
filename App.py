import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 role TEXT)''')
    conn.commit()
    conn.close()

# Function to register a user
def register_user(username, password, role):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Function to validate login
def validate_user(username, password, role):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
    user = c.fetchone()
    conn.close()
    return user

# Initialize the database
init_db()

# Session State Setup
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None

# Login/Registration
if not st.session_state.authenticated:
    choice = st.radio("Login or Register", ["Login", "Register"])
    role = st.selectbox("Select Role", ["Student", "Admin"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Register"):
            if register_user(username, password, role):
                st.success("Registration Successful! Please Login.")
            else:
                st.error("Username already exists. Try another one.")

    if choice == "Login":
        if st.button("Login"):
            if validate_user(username, password, role):
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Try again.")

# Main App after Login
if st.session_state.authenticated:
    st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
    menu_options = ["Home", "Scholarships"]
    if st.session_state.role == "Admin":
        menu_options.append("Manage Scholarships")
    
    selected = option_menu("Navigation", menu_options, icons=["house", "book", "tools"])
    
    if selected == "Home":
        st.title("Welcome to the Scholarship Finder")
    elif selected == "Scholarships":
        st.title("Available Scholarships")
        # Scholarship Data Display
        data = pd.read_csv("Scholarshipsnew.csv")
        st.dataframe(data)
    elif selected == "Manage Scholarships" and st.session_state.role == "Admin":
        st.title("Manage Scholarships")
        st.write("(Admin functionality to add/remove scholarships will be here)")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()
