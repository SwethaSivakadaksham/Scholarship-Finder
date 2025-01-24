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

# st.sidebar.header("Navigation")
# navigation = st.sidebar.radio("Navigation",["Home","About Us","List of Government Funded Scholarships","List of Private Funded Scholarships","Specially for Women Scholarships"], label_visibility="hidden")

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home","Government Funded Scholarships","Private Funded Scholarships","Scholarship for Women","International Scholarships"],
        icons=["house","compass","envelope","geo","gender-female","mortarboard-fill"],
        default_index=0,
        menu_icon="cast", 
        orientation="horizontal"
    )

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# styling of the website
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

html_temp = """
<div style = background-color:black;padding:5px>
<h1 style="color:white;text-align:Center">Scholarships Finder</h1>
</div>
<br>   
"""

html_temp2 = """
<div>
<h5 style="color:black;text-align:Left;font-size:20px">Hello , {} !</h5>
</div>
"""

html_temp3 = """
<div>
<h5 style="color:black;text-align:Left;font-size:24px">{}</h5>
</div>
"""

html_temp4 = """
<div>
<h5 style="color:gray;text-align:Left;font-size:16px">{}</h5>
</div>
"""

html_temp5 = """
<div style = background-color:black;padding:5px>
<h1 style="color:white;text-align:Center">Government Funded Scholarships</h1>
</div>
<br>   
"""

html_temp6 = """
<div style = background-color:black;padding:5px>
<h1 style="color:white;text-align:Center">Private Funded Scholarships</h1>
</div>
<br>   
"""

html_temp7 = """
<div style = background-color:black;padding:5px>
<h1 style="color:white;text-align:Center">Specifically For Women</h1>
</div>
<br>   
"""

html_temp8 = """
<div style = background-color:black;padding:5px>
<h1 style="color:white;text-align:Center">International Scholarships</h1>
</div>
<br>   
"""

html_temp9 = """
<br>
<div style = background-color:white;padding:5px>
<h3 style="color:black;text-align:Left;font-size:20px">Nelson Mandela rightly quoted:</h3>
</div>
<div style = background-color:black;padding:5px>
<h2 style="color:white;text-align:Center;font-size:22px">“ Education is the most powerful weapon we can use to change the world “.</h2>
</div>
<br>
"""

html_temp10 = """
<div style = background-color:white;padding:5px>
<h4 style="color:black;text-align:Center;font-size:20px">But in this fast-growing world, Education has become costly. And thus we come up with an idea of “ Scholarship Finder “ where a needy can find a scholarship. By this, one can definitely fulfill the dreams of educating themselves at a low cost.</h4>
</div>
<br>  
"""

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

# MAIN CODE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

if selected == "Home":
    st.markdown(html_temp,unsafe_allow_html=True)
    # st.title("Scholarship Finder")
    # st.dataframe(data)
    name = st.text_input("Enter your Name",placeholder="Name")
    if len(name) >= 1:
        st.markdown(html_temp2.format(name),unsafe_allow_html=True)
        minority = st.radio("Are you in Minorities(SC/ST) category?" ,["Yes","No"],index=1)
        disability = st.radio("Do you have any disability?",["Yes","No"],index=1)
        sports_person = st.radio("Do you play professional sports?",["Yes","No"],index=1)
        armed_forces = st.radio("Are any of your relatives in Armed Forces?",["Yes","No"],index=1)
        
        # Annual Income slider
        anual_income = st.slider(
            "Select your family's annual income (in Rupees):",
            min_value=0,
            max_value=1100000,
            value=300000,
            step=10000
        )
        
        income_words = num2words(anual_income)
        st.info(income_words)
        
        if anual_income >= 1100000:
            st.info("Annual Income should be less than 10 Lakh Rupees")
        
        marks = st.slider("Enter your marks in last final examination",min_value=0,max_value=100,value=30,step=1)
        gender = st.selectbox("Enter your gender:",["Male","Female"])
        nationality = st.radio("Do you want to include International Scholarships",["Yes","No"])

        if gender == "Female":
            if nationality == "Yes":
                mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= anual_income ) & (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks)]
            else:
                mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= anual_income ) & (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & (data["Country"] == "India") ]
        else:
            if nationality == "Yes":
                # st.write(nationality)
                mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= anual_income ) & (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & (data["Gender"] == "No")]
            else:
                mask = data.loc[(data["Minorities"] == minority) & (data["Annual Income"] >= anual_income ) & (data["Disablities"] == disability) & (data["Armed Forces"] == armed_forces) & (data["Sports Person"] == sports_person) & (data["Grades in Prev Exam"] <= marks) & (data["Gender"] == "No") & (data["Country"] == "India")]
        mask_new = mask[["Scholarship Name" , "Amount Provided","Link" ,"Funded By"]]
        rows = mask_new.shape[0]
        cols = mask_new.shape[1]
        a = []
        for i in range(rows):
            a.append(f"{ mask_new.iloc[i,0] } : {mask_new.iloc[i,1]} Rs")
            a.append(f"{ mask_new.iloc[i,2] }")
            a.append("-------------------------------------------")
        if st.button("Submit"):   
            for i in range(len(a)):
                if(i%3==0):
                    st.markdown(html_temp3.format(a[i]),unsafe_allow_html=True)
                else:
                    st.markdown(html_temp4.format(a[i]),unsafe_allow_html=True)
    else:
        st.info("This can't be empty!")

if selected == "Government Funded Scholarships":
    st.markdown(html_temp5,unsafe_allow_html=True)
    new = data["Funded By"] == "Government"
    govt_funded = data[new]
    govt_funded = govt_funded[["Scholarship Name" , "Amount Provided","Link"]]
    st.table(govt_funded)

if selected == "Private Funded Scholarships":
    st.markdown(html_temp6,unsafe_allow_html=True)
    new_2 = data["Funded By"] == "Private"
    prvt_funded = data[new_2]
    prvt_funded = prvt_funded[["Scholarship Name" , "Amount Provided","Link"]]
    st.table(prvt_funded)

if selected == "Scholarship for Women":
    st.markdown(html_temp7,unsafe_allow_html=True)
    new_3 = data["Gender"] == "Yes"
    women_funded = data[new_3]
    women_funded = women_funded[["Scholarship Name" , "Amount Provided","Link"]]
    st.table(women_funded)

if selected == "International Scholarships":
    st.markdown(html_temp8,unsafe_allow_html=True)
    new_4 = data["Country"] != "India"
    international_funded = data[new_4]
    international_funded = international_funded[["Scholarship Name" , "Amount Provided","Link"]]
    st.table(international_funded)

    st.markdown(html_temp9,unsafe_allow_html=True)
    st.markdown(html_temp10,unsafe_allow_html=True)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
