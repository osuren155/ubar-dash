# cd /d "D:\ubar dash"
# py -m streamlit run home.py

from PIL import Image
import streamlit as st
import base64
import os

st.set_page_config(
    page_title="UBAR Dashboard",
    layout="wide"
)

# ---------------- IMAGE PATH ----------------

image_path = "hhhj.jpg"

# Image ko base64 me convert karo
with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# ---------------- RESPONSIVE BACKGROUND CSS ----------------
st.markdown(
    f"""
    <style>
    /* 🌍 Base setup */
    html, body, .stApp {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }}

    /* 🖥 Desktop / Laptop */
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
    }}

    /* 📱 Mobile & Tablet */
    @media (max-width: 768px) {{
        .stApp {{
            background-size: contain;
            background-position: center top;
            background-color: black;
        }}
    }}

    /* 📱 Small Mobile */
    @media (max-width: 480px) {{
        .stApp {{
            background-size: contain;
            background-position: center top;
        }}
    }}

    /* 🔘 Button fixed bottom center */
    div[data-testid="stButton"] {{
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        display: flex;
        justify-content: center;
    }}

    div[data-testid="stButton"] button {{
        width: 200px;
        font-size: 16px;
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* 🌍 Base setup */
    html, body, .stApp {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: white;   /* 👈 WHITE background */
    }

    /* 🧼 Remove default Streamlit padding */
    .main {
        padding: 0;
    }

    /* 🔘 Button fixed bottom center */
    div[data-testid="stButton"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        display: flex;
        justify-content: center;
    }

    /* 🎨 Button style */
    div[data-testid="stButton"] button {
        width: 200px;
        font-size: 16px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------- BUTTON ----------------
if st.button("Go to Dashboard", key="go_dash"):
    st.switch_page("pages/Dash.py")









        
