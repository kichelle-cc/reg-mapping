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


st.title('Pillar 3')
st.text('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')

df = pd.read_csv('PILLAR3.csv')
df.rename(columns={
    'other products':'Other Products',
    ' Values':'Values',
    ' Attribute':'Attribute',
}, inplace=True)
categories = df.columns[5:11]

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
