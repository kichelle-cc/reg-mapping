import streamlit as st
import pandas as pd
import os
from PIL import Image

# sidebar
image = Image.open(os.getcwd()+'\\streamlit\\imgs\\deloitte-logo-black.png')
st.sidebar.image(image)
st.sidebar.header("S&C Reg Navigator v0.9")

# load data (moving to df_all via master spreadsheet soon)
prefix=os.getcwd()+'/streamlit/data/'
path = r'eu_taxonomy_assessment.csv'
df = pd.read_csv(prefix+path)
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')
df_all = df_all.loc[df_all.Framework=='EU Taxonomy']

df.Sector.replace(
    'Energy ',
    'Energy',
    inplace=True
)

df.Attributes.replace(
    {'Activity requirement': 'Activity Requirements',
    'Activity requirements': 'Activity Requirements'},
    inplace=True
)

# sectors = list(set(df.Sector))
sectors = sorted(list(set(df_all.Sector)))

st.title("EU Taxonomy")
st.divider()
st.caption('''The Taxonomy Regulation sits under the umbrella of the Non-Financial Reporting Directive 
(NFRD) and Sustainable Finance Disclosure Regulation (SFDR) which mandates EU-listed corporates, 
financial institutions and asset managers to disclose against. The current NFRD is being superseded by the 
Corporate Sustainability Reporting Directive (CSRD) which increases the scope 
of Taxonomy reporting. In its essence, the Taxonomy is a list of scientifically verified green activities
(i.e. a ‘dictionary’ of what is green or not) where entities will have to identify which 
of their activities align to the Taxonomy framework. \n 
This tool aims to simplify, and display a list of data attributes that are needed to report on 
for a given business operating in a set of industries and sectors 
''')

# cascading select boxes
# categories = st.multiselect('[TBC] type of reporting/assessment',
#                             ['Assesment', 'Reporting', 'Exposure'],
#                             )

geographies = st.multiselect('[TBC] Which geographies do you operate in?',
                            sorted(list(set(df_all.Geographies))),
                            )


options = st.multiselect(
    'What sectors does your business operate in?',
    sorted(sectors),
    [])

if options:
    filtered_df = df.loc[df.Sector.isin(options)]
    activities = st.multiselect(
    'What activities do you partake in?',
    sorted(set(filtered_df['Activity '])),
    [])

    if activities:
        filtered_df = filtered_df.loc[filtered_df['Activity '].isin(activities)]
        st.write('Great, the objectives you need to meet are:')
        #Great, the criteria you need to align with are:



        def check_for_criteria(df, attr, criterion, col):
            if criterion in list(set(filtered_df[filtered_df['Attributes'] == attribute][col])):
                return u'\u2713'
            else: return ''

        has_ccm = []
        has_cca = []
        has_scc = []
        has_dnsh = []

        for attribute in filtered_df.Attributes.unique():
            has_ccm.append(check_for_criteria(filtered_df, attribute, 'CCM', 'Objective'))
            has_cca.append(check_for_criteria(filtered_df, attribute,  'CCA', 'Objective'))
            has_scc.append(check_for_criteria(filtered_df,  attribute, 'SCC', 'SCC/DNSH'))
            has_dnsh.append(check_for_criteria(filtered_df, attribute,  'DNSH', 'SCC/DNSH'))

        criteria_df = pd.DataFrame({
            'Attribute':filtered_df.Attributes.unique(),
            'CCM?':has_ccm,
            'CCA?':has_cca,
            'SCC?':has_scc,
            'DNSH?':has_dnsh
        })

        def color_df(val):
            if val == u'\u2713':
                color='green'
            else:
                color='black'
            return f'color: {color}'
        
        st.dataframe(criteria_df.style.applymap(color_df))

        st.download_button(
        "Export Fully Mapped Attributes to Excel",
        filtered_df[['Activity ', 'Objective', 'SCC/DNSH', 'Attributes', 'Values']].to_csv(),
        "eu_taxonomy_attributes.csv",
        "text/csv",
        key='download-csv'
        )
