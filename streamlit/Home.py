import streamlit as st
import pandas as pd
import os
from PIL import Image
from utils import sidebar
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title='SC Regs Model',
    layout='wide'
)
sidebar()

# get path, useful for deployed app
prefix=os.getcwd()+'/streamlit/data/'

# load data
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')

# title
st.title('Sustainability & Climate Regulation Data Navigator')
# st.subheader('Analytics Dashboard')
st.divider()
labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
          "UK"]




## KPI SECTION
# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Data Attribute Coverage', 'Regulation Coverage'])
fig.add_trace(go.Pie(labels=labels, values=[16, 15, 12, 6, 5, 4, 42], pull=[0,0,0,0,0,0,0.2], name="Attribute Coverage",
              scalegroup='one'),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=[27, 11, 25, 8, 1, 3, 25], pull=[0,0,0,0,0,0,0.2], name="Regulation Coverage"),
              1, 2)
# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")
fig.update_layout(
    title_text="Analytics Dashboard & Summary Statistics (placeholder)",)
st.plotly_chart(fig, use_container_width=True)
col1, col2, col3 = st.columns(3)
col1.metric("Number of Regulations Supported", "2", "2")
col2.metric("Number of Geographies Supported", df_all['Geographies'].nunique(), "3")
col3.metric("End to End Attributes Mapped (placeholder!)", "26%", "4%")

# getting started / FAQ section
st.divider()
st.subheader('Getting Started ')
st.write('''This app aims to decompose complex regulatory documents into tangible data attributes''')

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
st.caption("""In order to comply with Pillar 3 requirements, financial institutions must collect and maintain 
            a wide range of data related to their risk management practices, capital adequacy, and market risk exposure.
            This view attempts to consolidate those data requirements and display your necessary attributes.
           """)
