import streamlit as st
import pandas as pd
import os
from PIL import Image
from utils import sidebar

sidebar()
prefix = os.getcwd()+ '/streamlit/'
# load data 
df = pd.read_csv(prefix+'data/PCAF.csv')

st.title("PCAF")
st.divider()
st.write('''The PCAF reporting framework is a tool that helps organizations 
measure and report their greenhouse gas emissions in a standardized and transparent way,
allowing for better comparisons and benchmarking. This page provides clear guidance on what
 data to collect anrd how to report it, helping you better understand their your 
 emissions profile and make informed decisions to reduce their impact on the environment. 
''')

geography = st.multiselect(
    'What geographies do you operate in?',
    sorted(df.Country.unique())
)

if geography:
    filtered_df = df.loc[df.Country.isin(geography)]
    asset_class = st.multiselect(
        'Which asset classes are applicable to you?',
        sorted(filtered_df["Asset class"].unique())
        )


    property_category = st.multiselect(
        'Which property category do your assets fall under?',
        filtered_df[filtered_df["Asset class"].isin(asset_class)]["Data level 1 information"].unique()
    )

    if property_category:
        property_sub_category = st.multiselect(
            'Which property sub-category do your assets fall under?',
            filtered_df[filtered_df["Data level 1 information"].isin(property_category)]["Data level 2 information"].unique()
        ) 

        if property_sub_category:
            st.write("Great, the data requirements for your assets are displayed in the table below:")
            
            st.dataframe(filtered_df.columns[6:12].values, use_container_width=True)
            st.download_button(
                "Export Fully Mapped Attributes to Excel",
                filtered_df.to_csv(),
                "pacf_attributes.csv",
                "text/csv",
                key='download-csv'
                )















#     if asset_class:
#         filtered_df_1 = filtered_df_1.loc[filtered_df_1.ProductCategories_AssetClasses.isin(asset_class)]
#         sub_asset_class = st.multiselect(
#             'Which sub asset classes',
#             sorted(filtered_df_1['Applicable Sub-Asset_Class'].unique())
#             )    

# st.subheader("Section 2")
# st.caption("Applicable Sector --> Value")
# st.divider()



# sector = st.multiselect(
#     'What sectors does your business operate in?',
#     df_2['Applicable Sector'].dropna().unique(),
#     [])

# if sector:
#     filtered_df_2 = df_2.loc[df_2['Applicable Sector'].isin(sector)]

#     activity = st.multiselect(
#         'Which activities',
#         filtered_df_2['Activity'].unique()
#     )

#     if activity:
#         filtered_df_2 = filtered_df_2.loc[filtered_df_2.Activity.isin(activity)]
#         st.write(filtered_df_2)


# if options:
#     # filtered_df = df_all.loc[df_all.Sector.isin(options)]
#     filtered_df = df.loc[df.Sector.isin(options)]
#     activities = st.multiselect(
#     'What activities do you partake in?',
#     sorted(set(filtered_df['Activity '])),
#     [])

#     if activities:
#         filtered_df = filtered_df.loc[filtered_df['Activity '].isin(activities)]
#         st.write('Great, the objectives you need to meet are:')
#         #Great, the criteria you need to align with are:



#         def check_for_criteria(df, attr, criterion, col):
#             if criterion in list(set(filtered_df[filtered_df['Attributes'] == attribute][col])):
#                 return u'\u2713'
#             else: return ''

#         has_ccm = []
#         has_cca = []
#         has_scc = []
#         has_dnsh = []

#         for attribute in filtered_df.Attributes.unique():
#             has_ccm.append(check_for_criteria(filtered_df, attribute, 'CCM', 'Objective'))
#             has_cca.append(check_for_criteria(filtered_df, attribute,  'CCA', 'Objective'))
#             has_scc.append(check_for_criteria(filtered_df,  attribute, 'SCC', 'SCC/DNSH'))
#             has_dnsh.append(check_for_criteria(filtered_df, attribute,  'DNSH', 'SCC/DNSH'))

#         criteria_df = pd.DataFrame({
#             'Attribute':filtered_df.Attributes.unique(),
#             'CCM?':has_ccm,
#             'CCA?':has_cca,
#             'SCC?':has_scc,
#             'DNSH?':has_dnsh
#         })

#         def color_df(val):
#             if val == u'\u2713':
#                 color='green'
#             else:
#                 color='black'
#             return f'color: {color}'
        
#         st.dataframe(criteria_df.style.applymap(color_df))

#         st.download_button(
#         "Export Fully Mapped Attributes to Excel",
#         filtered_df[['Activity ', 'Objective', 'SCC/DNSH', 'Attributes', 'Values']].to_csv(),
#         "eu_taxonomy_attributes.csv",
#         "text/csv",
#         key='download-csv'
#         )
