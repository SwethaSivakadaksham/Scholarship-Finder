#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from num2words import num2words

# MAIN CODE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

data = pd.read_csv("Scholarshipsnew.csv")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Government Funded Scholarships", "Private Funded Scholarships", "Scholarship for Women", "International Scholarships"],
        icons=["house", "bank", "hand-thumbs-up", "gender-female", "globe"],
        default_index=0,
        menu_icon="cast",
        orientation="vertical"
    )

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Styling of the website
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

html_temp = """
<div style="background-color:#0d6efd; padding:10px; border-radius: 5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h1 style="color:white;text-align:center;">Scholarships Finder</h1>
</div>
"""

html_temp2 = """
<div>
    <h5 style="color:black;text-align:left;font-size:18px">Hello, {}! Welcome to your personalized Scholarship Finder.</h5>
</div>
"""

html_temp3 = """
<div>
    <h5 style="color:#0d6efd;text-align:left;font-size:18px">{}</h5>
</div>
"""

html_temp4 = """
<div>
    <h5 style="color:gray;text-align:left;font-size:16px">{}</h5>
</div>
"""

html_temp5 = """
<div style="background-color:#0d6efd; padding:10px; border-radius: 5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h1 style="color:white;text-align:center;">Government Funded Scholarships</h1>
</div>
"""

html_temp6 = """
<div style="background-color:#0d6efd; padding:10px; border-radius: 5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h1 style="color:white;text-align:center;">Private Funded Scholarships</h1>
</div>
"""

html_temp7 = """
<div style="background-color:#0d6efd; padding:10px; border-radius: 5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h1 style="color:white;text-align:center;">Scholarships for Women</h1>
</div>
"""

html_temp8 = """
<div style="background-color:#0d6efd; padding:10px; border-radius: 5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <h1 style="color:white;text-align:center;">International Scholarships</h1>
</div>
"""

html_temp9 = """
<br>
<div style="background-color:white;padding:15px;">
    <h3 style="color:black;text-align:left;font-size:20px;">Nelson Mandela rightly quoted:</h3>
</div>
<div style="background-color:#0d6efd;padding:15px;border-radius: 5px;">
    <h2 style="color:white;text-align:center;font-size:22px;">“Education is the most powerful weapon we can use to change the world.”</h2>
</div>
<br>
"""

html_temp10 = """
<div style="background-color:white;padding:15px;">
    <h4 style="color:black;text-align:center;font-size:20px;">But in this fast-growing world, education has become costly. Thus, we bring you the “Scholarship Finder”, where those in need can find scholarships to fulfill their dreams of affordable education.</h4>
</div>
<br>
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN CODE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

if selected == "Home":
    st.markdown(html_temp, unsafe_allow_html=True)
    
    # User Input Form (Collapsible for better layout)
    with st.form(key="user_input_form", clear_on_submit=True):
        name = st.text_input("Enter your Name", placeholder="Name", label_visibility="collapsed")
        minority = st.radio("Are you in Minorities(SC/ST) category?", ["Yes", "No"], index=1)
        disability = st.radio("Do you have any disability?", ["Yes", "No"], index=1)
        sports_person = st.radio("Do you play professional sports?", ["Yes", "No"], index=1)
        armed_forces = st.radio("Are any of your relatives in Armed Forces?", ["Yes", "No"], index=1)
        annual_income = st.number_input("Enter your family's annual income (in INR)", max_value=1100000, step=1000)
        income_words = num2words(annual_income)
        marks = st.slider("Enter your marks in the last final examination", min_value=0, max_value=100, value=30, step=1)
        gender = st.selectbox("Enter your gender:", ["Male", "Female"])
        nationality = st.radio("Do you want to include International Scholarships?", ["Yes", "No"])

        # Submit Button
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if name:
            st.markdown(html_temp2.format(name), unsafe_allow_html=True)
            st.info(f"Your annual income in words: {income_words}")
        
            # Data Filtering
            if gender == "Female":
                if nationality == "Yes":
                    mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= annual_income) & 
                                    (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & 
                                    (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks)]
                else:
                    mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= annual_income) & 
                                    (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & 
                                    (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & 
                                    (data["Country"] == "India")]
            else:
                if nationality == "Yes":
                    mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= annual_income) & 
                                    (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & 
                                    (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & 
                                    (data["Gender"] == "No")]
                else:
                    mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= annual_income) & 
                                    (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & 
                                    (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & 
                                    (data["Gender"] == "No") & (data["Country"] == "India")]
            
            mask_new = mask[["Scholarship Name", "Amount Provided", "Link", "Funded By"]]
            rows = mask_new.shape[0]
            
            if rows > 0:
                # Display the scholarships as cards
                st.subheader("Available Scholarships")
                for i in range(rows):
                    with st.beta_expander(mask_new.iloc[i, 0]):
                        st.markdown(f"**Amount Provided:** {mask_new.iloc[i, 1]} INR")
                        st.markdown(f"**Funded By:** {mask_new.iloc[i, 3]}")
                        st.markdown(f"[Click here to apply]({mask_new.iloc[i, 2]})")
            else:
                st.warning("No scholarships found based on your input!")
        else:
            st.info("Please enter your name!")

# Government Funded Scholarships Section
if selected == "Government Funded Scholarships":
    st.markdown(html_temp5, unsafe_allow_html=True)
    govt_funded = data[data["Funded By"] == "Government"]
    govt_funded = govt_funded[["Scholarship Name", "Amount Provided", "Link"]]
    
    st.subheader("Government Funded Scholarships")
    for i in range(govt_funded.shape[0]):
        with st.beta_expander(govt_funded.iloc[i, 0]):
            st.markdown(f"**Amount Provided:** {govt_funded.iloc[i, 1]} INR")
            st.markdown(f"[Click here to apply]({govt_funded.iloc[i, 2]})")

# Private Funded Scholarships Section
if selected == "Private Funded Scholarships":
    st.markdown(html_temp6, unsafe_allow_html=True)
    prvt_funded = data[data["Funded By"] == "Private"]
    prvt_funded = prvt_funded[
