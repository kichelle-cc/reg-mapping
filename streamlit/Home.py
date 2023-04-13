from collections import Counter
import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
st.set_page_config(
    page_title='SC Regs Model',
    layout='wide'
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



print(st.__version__)
add_logo()


st.title('Sustainability & Climate Regulation Navigatior')

st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Number of Regulations Supported", "2", "2")
col2.metric("KPI #2", "9", "-8%")
col3.metric("KPI #3", "86%", "4%")

st.divider()
st.subheader('Getting Started ')
st.write('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')


st.caption("This is where the user guide will go")
