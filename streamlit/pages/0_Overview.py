import streamlit as st 
import os
from PIL import Image
from utils import sidebar

sidebar()
prefix=os.getcwd()
path_to_html = prefix + '/streamlit/imgs/ESG Reg & Data Model Mapping_v7.html'
# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.title("Mapping Overview")
st.divider()
st.caption("A simple, interactive view of our current regulatory framework mapping")
st.components.v1.html(html_data, height=1400, scrolling=False)
