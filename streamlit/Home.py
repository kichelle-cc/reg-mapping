import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(
    page_title='SC Regs Model',
    layout='wide'
)

# get path, useful for deployed app
prefix=os.getcwd()+'/streamlit/data/'

# sidebar formatting
image = Image.open(os.getcwd()+'\\streamlit\\imgs\\deloitte-logo-black.png')
st.sidebar.image(image)
st.sidebar.header("S&C Reg Navigator v0.9")

# load data
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')

# title
st.title('Sustainability & Climate Regulation Navigatior')
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Number of Regulations Supported", "2", "2")
col2.metric("Number of Geographies Supported", df_all['Geographies'].nunique(), "3")
col3.metric("End to End Attributes Mapped (TBC!) #3", "26%", "4%")

# getting started / FAQ section
st.divider()
st.subheader('Getting Started ')
st.write('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into tangible data attributes''')

### Overview
st.divider()
st.subheader('Overview')
st.caption("""A simple, interactive view of our current regulatory framework mapping. This page
           demonstrates our current, WIP view of regulatory landscape for global, EU, and UK
           regulations. For brevity we have specifically expanded asset classes and data attributes 
           for FS, banking and capital markets.
           """)

st.caption("""
           Interactive components of the flow chart are denoted by cubes.  
           """)


### Framework Mapping
st.divider()
st.subheader('Framework Mapping')
st.caption("""This app aims to decompose complex regulatory documents 
            into digestable controls and requirements which we can then 
            simplify into physical data attributes. Select the geographies which you 
            operate in, allowing you to determine exactly which attributes apply to you.
           """)


### EU Taxonomy
st.divider()
st.subheader('EU Taxonomy')
st.caption("""
            A view of the EU-Taxonomy mapping for reporting, assessment and exposure. This tool aims
            to help you identify clear definitions for what environmentally sustainable economic 
            activities you need to comply with.
           """)

### Pillar 3 
st.divider()
st.subheader('Pillar 3')
st.caption("""TBC...
           """)
