from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import graphviz
st.set_page_config(
    page_title='SC Regs Model',
    layout='wide'
)
import networkx as nx 
from nx.drawing.nx_agraph import graphviz_layout

def format_position(G, threshold=5):
    # function that reformats a network x graph, G to look 'nicer'
    pos = graphviz_layout(G, prog='dot')
    counts = dict(Counter(i[1] for i in pos.values()))
    
    old_y_vals = []
    new_y =[]
    for i in counts.items():
        y_val = i[0]
        count = i[1]
        if count > threshold:
            old_y_vals.append(y_val)
            for j in range(count):
                new_y.append(-2*(np.cos(j) - count/2)**2)

    for i, j in zip({k:v for k,v in pos.items() if v[1] in old_y_vals}, new_y):
        pos[i] = (pos[i][0], j)

    return pos


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


def out_df(
    # makes df of requirements for export
        df,
        geog,
        reg,
        sub_reg,
        industry,
        sector
    ):
    output = df.loc[
    (df["Geographies"] == geog) &
    (df["Framework"].isin(reg)) &
    (df["Industry"].isin(industry)) &
    (df["Sector"].isin(sector)) 
    ]
    cols = list(output.columns)
    cols.remove('ProductCategories_AssetClasses')
    return output[cols].to_csv()


def make_digraph(
    # uses networkx to produce a digraph of the regs
    # need to add subreg once we have subreg -> industry mapping
    geog,
    reg,
    sub_reg,
    industry,
    sector
    ):
        G = nx.DiGraph()

        for index, row in df_geo_reg.iterrows():
            if (row["Geographies"] in geog) & (row['Framework'] in reg):
                G.add_edge(str(row["Geographies"]), str(row["Framework"]))
        
        # if sub_reg:
        #     for index, row in df_reg_subreg.iterrows():
        #         if (row["Framework"] in reg) & (row["Framework Subcategory"] in sub_reg):
        #             G.add_edge(str(row["Framework"]), str(row["Framework Subcategory"]))
        #     for index, row in df_sub_reg_indus.iterrows():
        #         if (row["Framework Subcategory"] in reg) & (row["Industry"] in industry):
        #             G.add_edge(str(row["Framework Subcategory"]), str(row["Industry"]))
        # else:

        for index, row in df_reg_indus.iterrows():
            if (row["Framework"] in reg) & (row["Industry"] in industry):
                G.add_edge(str(row["Framework"]), str(row["Industry"]))
        for index, row in df_indus_sector.iterrows():
            if (row["Industry"] in industry) & (row["Sector"] in sector):
                G.add_edge(str(row["Industry"]), str(row["Sector"]))
        for index, row in df_sector_product.iterrows():
            if row["Sector"] in sector:
                G.add_edge(str(row["Sector"]), str(row["Asset_Class"]))

        fig = plt.figure(figsize=(20,20)) 
        nx.draw(G, pos=format_position(G), with_labels=True, node_color="None", node_shape='s', node_size=500, font_size=14,
                bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.25'))
        return fig


def display_fig_download(df, geog, reg, sub_reg, industry, sector):
    st.download_button(
    "Export Fully Mapped Attributes to Excel",
    out_df(df, geog, reg, sub_reg, industry, sector),
    "sc_reg_attributes.csv",
    "text/csv",
    key='download-csv'
    )
    with st.expander('''Show/Hide full mapping (Selecting 1-2 from each category at a time should 
    provide a good number of attributes to display at once)
    '''): 
        st.pyplot(make_digraph(
            geog,
            reg,
            sub_reg,
            industry,
            sector
            ))
    return


add_logo()
df_all = pd.read_csv('Reg & Data Relationship.csv')
df_geo_reg = pd.read_csv('Rel_Geo_Framework.csv')
df_reg_subreg = pd.read_csv('Rel_Framework_Framework_Subcategory.csv')
df_reg_indus = pd.read_csv('Rel_Framework_Industry.csv')
df_indus_sector = pd.read_csv('Rel_Industry_Sector.csv')
df_sector_product = pd.read_csv('Rel_Sector_Product.csv')
df_asset_subasset = pd.read_csv('Rel_Asset_SubAsset.csv')
ms = 2

st.title('Sustainability & Climate: Relational Data Model')
st.text('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')


geos = df_all['Geographies'].unique()
geo_choice = st.selectbox('Geography', np.insert(geos, 0, 'Select a Geography'))

if geo_choice:
    regs = df_all["Framework"].loc[df_all["Geographies"] == (geo_choice)].unique()
    reg_choice = st.multiselect('Framework', regs, max_selections=ms)
    
    if reg_choice:
        sub_regs = df_all["Framework Subcategory"].loc[df_all["Framework"].isin(reg_choice)]

        if not sub_regs.dropna().empty:
            sub_regs = sub_regs.unique()
            sub_reg_choice = st.multiselect('Framework Subcategory', sub_regs, max_selections=ms)

            industries = df_all['Industry'].loc[df_all["Framework Subcategory"].isin(sub_reg_choice)].unique()
            industry_choice = st.multiselect('Industry', industries,max_selections=ms)
            
            if industry_choice:
                sector = df_all['Sector'].loc[df_all['Industry'].isin(industry_choice)].unique()
                sector_choice = st.multiselect('Sector', sector, max_selections=ms)
                
                if sector_choice:
                    display_fig_download(
                        df_all,
                        geo_choice,
                        reg_choice,
                        sub_reg_choice,
                        industry_choice,
                        sector_choice
                    )
    
        else:
            sub_reg_choice = reg_choice

            industries = df_all['Industry'].loc[df_all["Framework"].isin(sub_reg_choice)].unique()
            industry_choice = st.multiselect('Industry', industries, max_selections=ms)
            
            if industry_choice:
                sector = df_all['Sector'].loc[df_all['Industry'].isin(industry_choice)].unique()
                sector_choice = st.multiselect('Sector', sector, max_selections=ms)
                
                if sector_choice:
                    display_fig_download(
                        df_all,
                        geo_choice,
                        reg_choice,
                        None,
                        industry_choice,
                        sector_choice
                    )
    
