from collections import Counter
import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import os
st.set_page_config(
    page_title='SC Regs Model',
    layout='wide'
)

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375PX;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
def add_logo():
    # adds logo to sider, can insert a png here later
    st.markdown(
        """
        <style>
        
            [data-testid="stSidebarNav"]::before {
                content: "Navigation";
                margin-left: 20px;
                margin-top: 0px;
                font-size: 22px;
                position: relative;
                top: 50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )



add_logo()


prefix=os.getcwd()+'/streamlit/data/'
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')

st.title('Sustainability & Climate Regulation Navigatior')
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Number of Regulations Supported", "2", "2")
col2.metric("Number of Geographies Supported", df_all['Geographies'].nunique(), "3")
col3.metric("End to End Attributes Mapped (TBC!) #3", "26%", "4%")

st.divider()
st.subheader('Getting Started ')
st.write('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')

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
st.caption("""A simple, interactive view of our current regulatory framework mapping. This page
           demonstrates our current, WIP view of regulatory landscape for global, EU, and UK
           regulations. For brevity we have specifically expanded asset classes and data attributes 
           for FS, banking and capital markets.
           """)

st.caption("""
           Interactive components of the flow chart are denoted by cubes.  
           """)

### EU Taxonomy
st.divider()
st.subheader('EU Taxonomy')
st.caption("""A simple, interactive view of our current regulatory framework mapping. This page
           demonstrates our current, WIP view of regulatory landscape for global, EU, and UK
           regulations. For brevity we have specifically expanded asset classes and data attributes 
           for FS, banking and capital markets.
           """)

st.caption("""
           Interactive components of the flow chart are denoted by cubes.  
           """)

### Pillar 3 
st.divider()
st.subheader('Pillar 3')
st.caption("""A simple, interactive view of our current regulatory framework mapping. This page
           demonstrates our current, WIP view of regulatory landscape for global, EU, and UK
           regulations. For brevity we have specifically expanded asset classes and data attributes 
           for FS, banking and capital markets.
           """)

st.caption("""
           Interactive components of the flow chart are denoted by cubes.  
           """)
