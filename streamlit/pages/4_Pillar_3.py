import streamlit as st
import pandas as pd
import numpy as np
import os 
from PIL import Image
from utils import sidebar

sidebar()


st.title('Pillar 3')
st.divider()
st.caption('''Pillar 3 is a regulatory requirement for banks, insurers, and other financial 
institutions to disclose relevant information about their risk management, capital structure, 
and governance practices. The goal of Pillar 3 is to promote transparency and help stakeholders 
better understand the risks and financial position of financial institutions. 
The disclosure requirements cover areas such as credit risk, market risk, liquidity risk, 
and operational risk, as well as information on capital adequacy, leverage, and funding.
The disclosures must be made on a regular basis and are typically included in public
reports such as annual reports, prospectuses, and other regulatory filings.
Pillar 3 is part of the Basel III framework for bank regulation and is overseen by national 
regulators.''')

# read data
prefix=os.getcwd()+'/streamlit/data/'
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')
df_all = df_all.loc[df_all.Framework == 'Pillar 3']
df = pd.read_csv(prefix+'PILLAR3.csv')
df.rename(columns={
    'other products':'Other Products',
    ' Values':'Values',
    ' Attribute':'Attribute',
}, inplace=True)
categories = df.columns[5:11]
ms = 3

# cacading select boxes
geos = df_all['Geographies'].unique()
geo_choice = st.selectbox('Geography', np.insert(geos, 0, 'Select a Geography'))

if geo_choice != 'Select a Geography':

    sectors = df_all['Sector'].unique()
    sector_choice = st.multiselect('Sector', sectors,max_selections=ms)    
    if sector_choice:
        # ProductCategories_AssetClasses,Sub-Asset_Class,Asset_Class

        product_categories = df_all['ProductCategories_AssetClasses'].unique()
        product_choice = st.multiselect('Asset Class', product_categories,max_selections=ms)    
        if product_choice:
            options = st.multiselect(
                'What category of product does your business offer? (WIP)',
                sorted(categories),
                [])


            if options:
                st.text('Great, the attributes you need to report on are:')
                df['mask'] = df[options].apply(lambda x: x.any(), axis=1)
                
                reported_tbl = df[df['mask'] == True]
                base = ['Attribute', 'Values']
                st.dataframe(reported_tbl.reset_index()[base], use_container_width=True)
                st.download_button(
                            "Export Fully Mapped Attributes to Excel",
                            reported_tbl.reset_index()[base].to_csv(),
                            "sc_reg_attributes.csv",
                            "text/csv",
                            key='download-csv'
                            )
