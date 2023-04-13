import streamlit as st
import pandas as pd
import numpy as np
import os 

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

add_logo()


st.title('Pillar 3')
st.divider()
st.caption('''Pilar 3 is a ...''')

prefix=r'C:\Users\kcomriecarson\Documents\projects\esg_gdp\web-app\reg-mapping\streamlit\data\\'
prefix=os.getcwd()+'\\streamlit\\data\\'
df_all = pd.read_csv(prefix+'Reg & Data Relationship.csv')
df_all = df_all.loc[df_all.Framework == 'Pillar 3']
df = pd.read_csv(prefix+'PILLAR3.csv')
df.rename(columns={
    'other products':'Other Products',
    ' Values':'Values',
    ' Attribute':'Attribute',
}, inplace=True)
categories = df.columns[5:11]
ms = 3


geos = df_all['Geographies'].unique()
geo_choice = st.selectbox('Geography', np.insert(geos, 0, 'Select a Geography'))

if geo_choice != 'Select a Geography':

    industries = df_all['Industry'].unique()
    industry_choice = st.multiselect('Industry', industries,max_selections=ms)    
    if industry_choice:


        options = st.multiselect(
            'What category of product does your business offer?',
            sorted(categories),
            [])


        if options:
            st.text('Great, the attributes you need to report on are:')
            df['mask'] = df[options].apply(lambda x: x.any(), axis=1)
            
            reported_tbl = df[df['mask'] == True]
            base = ['Attribute', 'Values']
            st.write(reported_tbl.reset_index()[base])
            st.metric("My metric", 42, 2)
            st.download_button(
                        "Export Fully Mapped Attributes to Excel",
                        reported_tbl.reset_index()[base].to_csv(),
                        "sc_reg_attributes.csv",
                        "text/csv",
                        key='download-csv'
                        )
            # st.write(reported_tbl.iloc[:,:10])
            # st.write(reported_tbl[options+base])
            # print((reported_tbl.reset_index()['Attribute ']))
            # print(reported_tbl.columns)
