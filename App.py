import streamlit as st
import pandas as pd

# Mock database for users and scholarships
users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "student1": {"password": "student123", "role": "student", "details": {}},
}

scholarships_db = pd.DataFrame({
    "name": ["Scholarship A", "Scholarship B", "Scholarship C"],
    "eligibility": ["GPA > 3.5", "GPA > 3.0", "GPA > 2.5"],
    "amount": ["₹50,000", "₹30,000", "₹10,000"]  # Updated to Indian Rupees
})

def login(username, password):
    if username in users_db and users_db[username]["password"] == password:
        return users_db[username]["role"]
    return None

def register(username, password):
    if username not in users_db:
        users_db[username] = {"password": password, "role": "student", "details": {}}
        return True
    return False

def manage_scholarships():
    st.write("Manage Scholarships")
    new_scholarship_name = st.text_input("Scholarship Name")
    new_scholarship_eligibility = st.text_input("Eligibility Criteria")
    new_scholarship_amount = st.text_input("Amount (in ₹)")
    if st.button("Add Scholarship"):
        global scholarships_db
        new_scholarship = pd.DataFrame({
            "name": [new_scholarship_name],
            "eligibility": [new_scholarship_eligibility],
            "amount": [f"₹{new_scholarship_amount}"]  # Add ₹ symbol
        })
        scholarships_db = pd.concat([scholarships_db, new_scholarship], ignore_index=True)
        st.success("Scholarship added successfully!")

def student_details_page(username):
    st.write("Update Your Details")
    gpa = st.number_input("Enter your GPA", min_value=0.0, max_value=4.0, step=0.1)
    income = st.number_input("Enter your family income (in ₹)", min_value=0, step=1000)
    if st.button("Submit Details"):
        users_db[username]["details"] = {"gpa": gpa, "income": income}
        st.success("Details updated successfully!")
        st.session_state["page"] = "eligible_scholarships"  # Redirect to next page

def eligible_scholarships_page(username):
    st.write("Eligible Scholarships")
    student_details = users_db[username]["details"]
    gpa = student_details.get("gpa", 0.0)
    income = student_details.get("income", 0)

    # Filter scholarships based on GPA
    eligible_scholarships = scholarships_db[
        scholarships_db["eligibility"].apply(lambda x: eval(x.replace("GPA", str(gpa))))
    ]
    st.write(eligible_scholarships)

def main():
    st.title("Scholarship Finder")

    if "page" not in st.session_state:
        st.session_state["page"] = "user_selection"

    if st.session_state["page"] == "user_selection":
        st.write("Are you an Admin or a Student?")
        user_type = st.radio("Select User Type", ["Admin", "Student"])
        if user_type == "Admin":
            st.session_state["user_type"] = "admin"
            st.session_state["page"] = "login"
        elif user_type == "Student":
            st.session_state["user_type"] = "student"
            st.session_state["page"] = "student_options"

    elif st.session_state["page"] == "student_options":
        st.write("Student Options")
        option = st.radio("Select Option", ["Login", "Register"])
        if option == "Login":
            st.session_state["page"] = "login"
        elif option == "Register":
            st.session_state["page"] = "register"

    elif st.session_state["page"] == "login":
        st.write("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            role = login(username, password)
            if role:
                st.session_state["username"] = username
                if role == "admin":
                    st.session_state["page"] = "manage_scholarships"
                elif role == "student":
                    st.session_state["page"] = "student_details"
            else:
                st.error("Invalid username or password")

    elif st.session_state["page"] == "register":
        st.write("Student Registration")
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        if st.button("Register"):
            if register(username, password):
                st.success("Registration successful! Please login.")
                st.session_state["page"] = "login"
            else:
                st.error("Username already exists.")

    elif st.session_state["page"] == "manage_scholarships":
        manage_scholarships()

    elif st.session_state["page"] == "student_details":
        student_details_page(st.session_state["username"])

    elif st.session_state["page"] == "eligible_scholarships":
        eligible_scholarships_page(st.session_state["username"])

if __name__ == "__main__":
    main()
