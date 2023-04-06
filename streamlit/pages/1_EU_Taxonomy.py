import streamlit as st 
import pandas as pd 

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

path = r'eu_taxonomy_assessment.csv'
df = pd.read_csv(path)

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

st.title("EU Taxonomy")
st.text('''This app aims to decompose completx regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')


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
        st.write('Great, the criteria you need to align with are:')

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
