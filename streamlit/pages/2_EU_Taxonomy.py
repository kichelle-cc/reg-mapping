import streamlit as st
import pandas as pd
import os
from PIL import Image
from collections import Counter
from utils import sidebar

sidebar()

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

sectors = list(set(df.Sector))
# sectors = sorted(list(set(df_all.Sector)))

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
industry = st.multiselect(
    'Which industry does your business operate in?',
    df_all.Industry.unique()
)

if industry:
    options = st.multiselect(
        'Which EU Taxonomy sectors apply? Please select from the list below.',
        sorted(sectors))

    if options:
        filtered_df = df.loc[df.Sector.isin(options)]
        activities = st.multiselect(
        'For those EU Taxonomy sectors, what activities do you partake in?',
        sorted(set(filtered_df['Activity '])))

        if activities:
            filtered_df = filtered_df.loc[filtered_df['Activity '].isin(activities)]
            
            asset_class = st.multiselect(
                'Finally, select the applicabe asset classes associated with your activities.',
                df_all.loc[df_all.Industry.isin(industry)].ProductCategories_AssetClasses.unique()
            )
            if asset_class:
                # st.write('Great, your activites need you to contribute to the following criteria and objectives:')
                st.write('Great, the activities you partake in align to the below taxonomy criteria and objectives:')
                #Great, the criteria you need to align with are:



                grouped_df = filtered_df.groupby(['Objective', 'SCC/DNSH', 'Attributes']).size().reset_index(name='Count')

                # pivot table to reshape the data
                output_df = grouped_df.pivot_table(index=['Objective', 'SCC/DNSH'], columns='Attributes', values='Count', aggfunc='sum').reset_index()

                # fill NaN values with empty string
                output_df = output_df.fillna('')

                # format output table
                output_df.columns.name = ''
                output_df = output_df.rename(columns={'SCC/DNSH': 'Type'})


                filtered_df["Attributes"].replace({"CCA/CCM":"CCM/CCA"}, inplace=True)
                gpt_df = filtered_df.groupby(["Objective", "SCC/DNSH"])["Attributes"].agg({list}).reset_index()
                gpt_df['dict'] = gpt_df.iloc[:,2].apply(lambda x: Counter(x))
                gpt_df['Attribute'] = gpt_df['dict'].apply(
                    lambda y: [f"{v}x {k}" for k,v in sorted(
                    dict(y).items(),
                    reverse=True,
                    key=lambda item: item[1]
                    )])
                
                # print(gpt_df['out'])
                st.dataframe(gpt_df[['Objective', 'SCC/DNSH', 'Attribute']].sort_values('Objective'), use_container_width=True)#, ascending=False))
                # print(Counter(gpt_df.iloc[0,2]))
                # st.write(gpt_df.groupby('list').count())
                # st.write(filtered_df.groupby(["Objective", "SCC/DNSH"])["Attributes"].agg(list).reset_index())

                # st.write(filtered_df)
                # st.write(filtered_df.groupby(['Objective', 'Attributes']).first())

                def check_for_criteria(df, attribute, criterion, col):
                    if criterion in list(set(filtered_df[filtered_df['Attributes'] == attribute][col])):
                        return u'\u2713'
                    else: return None

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


                st.download_button(
                "Export Fully Mapped Attributes to Excel",
                filtered_df[['Activity ', 'Objective', 'SCC/DNSH', 'Attributes', 'Values']].to_csv(),
                "eu_taxonomy_attributes.csv",
                "text/csv",
                key='download-csv'
                )
