from PIL import Image
import streamlit as st
import base64
import os

st.set_page_config(
    page_title="UBAR Dashboard",
    layout="wide"
)


st.image("hhhj_2.jpg", width=2000)   

import streamlit as st

col1, col2, col3 = st.columns([2.5, 1, 2.5])

with col2:


 st.markdown("""
    <style>
    div.stButton > button {
        width: 150px;
        height: 45px;
        font-size: 18px;
        margin: auto;
        display: block;
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        border: 1px solid #000000;
    }
    </style>
""", unsafe_allow_html=True)

 if st.button("Go to Dashboard", key="go_dash"):
    st.switch_page("pages/Dash.py")



st.markdown("""
## 🚗 Uber Dashboard Overview

This dashboard provides an **in-depth analysis of Uber ride data**, focusing on key metrics and trends:

- 🕒 **Trip Duration & Time of Day**  
- 📍 **Pickup & Drop-off Locations**  
- 💰 **Revenue & Pricing Patterns**  
- 👥 **Driver & Rider Behavior**

### 🎯 Objective
The goal of this analysis is to:
- Identify **high-demand and low-demand areas**
- Analyze **ride patterns and peak hours**
- Optimize **driver allocation and pricing strategies**

### 💡 Impact
By leveraging **data-driven insights**, this dashboard helps:
- Uber management teams  
- Data analysts  
- Urban planners  

to improve **ride efficiency**, maximize **driver earnings**, and enhance **customer experience**.
""") 

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:grey;'>Created by Surendra Oraon | Streamlit Dashboard</p>",
    unsafe_allow_html=True
)





   










        
