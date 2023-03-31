from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st
import pandas as pd
import graphviz
st.set_page_config(
    page_title='Regs Data Model & Mapping',
    layout='wide'
)

def add_logo():
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
# add_logo()

df_all = pd.read_csv('Reg & Data Relationship.csv')
df_geo_reg = pd.read_csv('Rel_Geo_Framework.csv')
df_reg_indus = pd.read_csv('Rel_Framework_Industry.csv')
df_indus_sector = pd.read_csv('Rel_Industry_Sector.csv')
df_sector_product = pd.read_csv('Rel_Sector_Product.csv')
df_asset_subasset = pd.read_csv('Rel_Asset_SubAsset.csv')


st.title('Regulatory Framework Mapping')
st.text('''This app aims to decompose completx regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')


geos = df_all['Geographies'].unique()
geo_choice = st.sidebar.selectbox('Select Geography', geos)

regs = df_all["Framework"].loc[df_all["Geographies"] == geo_choice].unique()
reg_choice = st.sidebar.selectbox('Select Framework', regs)

industries = df_all['Industry'].loc[df_all["Framework"] == reg_choice].unique()
industry_choice = st.sidebar.selectbox('Select Industry', industries)

sector = df_all['Sector'].loc[df_all['Industry'] == industry_choice].unique()
sector_choice = st.sidebar.selectbox('Select Sector', sector)


asset_class = df_all['Asset_Class'].loc[df_all['Sector'] == sector_choice].unique()
asset_class_choice = st.sidebar.selectbox('Product/Asset Class', asset_class)

sub_asste_class = df_all['Sub-Asset_Class'].loc[df_all['Asset_Class'] == asset_class_choice].unique()
sub_asset_class_choice = st.sidebar.selectbox('Sub-Asset Class', sub_asste_class)


graph = graphviz.Digraph()
graph.attr(rankdir="LR")

for index, row in df_geo_reg.iterrows():
    if row["Geographies"] == geo_choice:
        graph.edge(str(row["Geographies"]), str(row["Framework"]), lable='')
for index, row in df_reg_indus.iterrows():
    if row["Framework"] == reg_choice:
        graph.edge(str(row["Framework"]), str(row["Industry"]), lable='')
for index, row in df_indus_sector.iterrows():
    if row["Industry"] == industry_choice:
        graph.edge(str(row["Industry"]), str(row["Sector"]), lable='')
for index, row in df_sector_product.iterrows():
    if row["Sector"] == sector_choice:
        graph.edge(str(row["Sector"]), str(row["Asset_Class"]), lable='')
#for index, row in df_asset_subasset.iterrows():
#    if row["Asset_Class"] == asset_class_choice:
#        graph.edge(str(row["Asset_Class"]), str(row["Sub-Asset_Class"]), lable='')         
st.graphviz_chart(graph, use_container_width=True)
