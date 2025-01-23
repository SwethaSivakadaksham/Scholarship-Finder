import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from num2words import num2words

# Load the data
data = pd.read_csv("Scholarshipsnew.csv")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "About Us", "Government Funded Scholarships", 
                 "Private Funded Scholarships", "Scholarship for Women", 
                 "International Scholarships"],
        icons=["house", "info-circle", "bank", "briefcase", "gender-female", "globe"],
        default_index=0,
        menu_icon="list",
    )

# CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background-color: #e6e6e6;
    }
    h1, h2, h3, h5 {
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Header HTML templates
def header(title, bg_color="purple", text_color="yellow"):
    return f"""
        <div style="background-color:{bg_color};padding:10px;border-radius:5px">
            <h1 style="color:{text_color};text-align:center">{title}</h1>
        </div>
        <br>
    """

# Reusable function to display scholarships
def display_scholarships(df):
    for index, row in df.iterrows():
        st.markdown(f"**{row['Scholarship Name']}**")
        st.write(f"- Amount: ₹{row['Amount Provided']}")
        st.write(f"- [Details]({row['Link']})")
        st.write("---")

# Home Page
if selected == "Home":
    st.markdown(header("Scholarship Finder"))
    name = st.text_input("Enter your Name:", placeholder="Name")
    if name:
        st.write(f"Hello, {name}!")
        minority = st.radio("Are you in Minorities (SC/ST) category?", ["Yes", "No"], index=1)
        disability = st.radio("Do you have any disability?", ["Yes", "No"], index=1)
        sports_person = st.radio("Do you play professional sports?", ["Yes", "No"], index=1)
        armed_forces = st.radio("Are any of your relatives in Armed Forces?", ["Yes", "No"], index=1)
        annual_income = st.number_input("Enter your family's annual income:", max_value=1100000)
        income_words = num2words(annual_income, lang='en_IN')
        st.write(f"Your annual income: {income_words.capitalize()}")
        if annual_income > 1000000:
            st.warning("Annual income should be less than ₹10 Lakhs.")
        marks = st.slider("Enter your marks in the last final examination:", 0, 100, 30)
        gender = st.selectbox("Select your gender:", ["Male", "Female"])
        nationality = st.radio("Include International Scholarships?", ["Yes", "No"], index=1)

        # Filtering scholarships
        filters = (
            (data["Minorities"] == minority) &
            (data["Disabilities"] == disability) &
            (data["Armed Forces"] == armed_forces) &
            (data["Sports Person"] == sports_person) &
            (data["Grades in Prev Exam"] <= marks)
        )
        if gender == "Female":
            filters &= (data["Gender"] == "Yes")
        if nationality == "No":
            filters &= (data["Country"] == "India")
        eligible_scholarships = data.loc[filters, ["Scholarship Name", "Amount Provided", "Link", "Funded By"]]
        
        if st.button("Find Scholarships"):
            if eligible_scholarships.empty:
                st.info("No scholarships match your criteria.")
            else:
                display_scholarships(eligible_scholarships)

# Government Funded Scholarships
if selected == "Government Funded Scholarships":
    st.markdown(header("Government Funded Scholarships"))
    govt_scholarships = data[data["Funded By"] == "Government"]
    display_scholarships(govt_scholarships)

# Private Funded Scholarships
if selected == "Private Funded Scholarships":
    st.markdown(header("Private Funded Scholarships"))
    private_scholarships = data[data["Funded By"] == "Private"]
    display_scholarships(private_scholarships)

# Scholarship for Women
if selected == "Scholarship for Women":
    st.markdown(header("Scholarships for Women"))
    women_scholarships = data[data["Gender"] == "Yes"]
    display_scholarships(women_scholarships)

# International Scholarships
if selected == "International Scholarships":
    st.markdown(header("International Scholarships"))
    international_scholarships = data[data["Country"] != "India"]
    display_scholarships(international_scholarships)

# About Us
if selected == "About Us":
    st.markdown(header("About Us"))
    st.markdown("""
        **Scholarship Finder** is a platform designed to assist students in finding scholarships that suit their needs and eligibility.
        Our team is dedicated to helping students achieve their dreams by removing financial barriers to education.
    """)
    st.image("team_photo.jpg", caption="Our Team", use_column_width=True)
