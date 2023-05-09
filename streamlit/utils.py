import streamlit as st
import pandas as pd
import os
from PIL import Image

def sidebar():
    prefix = os.getcwd()+ '/streamlit/'
    image = Image.open(prefix+'imgs/deloitte-logo-white.png')
    # C:\Users\kcomriecarson\Documents\projects\esg_gdp\web-app\reg-mapping\streamlit\imgs\deloitte-logo-white.png
    st.sidebar.markdown("#")
    st.sidebar.markdown("#")

    st.sidebar.image(image)
    st.sidebar.header("S & C Reg Navigator v0.9")

    st.sidebar.caption("""
    Welcome to our tool! \n
    We are still working on it to make it even better.
    While we strive to provide you with accurate information and a smooth user experience,
    we cannot guarantee that everything on the site is perfect just yet. Therefore, please note that
    the mappings and attributes here are still subject to change.
    \n 
    We appreciate your patience and understanding as we work to make this tool the best it can be.
    If you have any questions or concerns, please don't hesitate to contact us!
    """)
    return 

def title(page:str):
    title_mapping = {
        'Home':['Sustainability & Climate Regulation Navigator', ''],
        'Overview':['Mapping Overview', 'A simple, interactive view of our current regulatory framework mapping'],

    }