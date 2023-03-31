import streamlit as st
import pandas as pd

st.title('Pillar 3')
st.text('''Use this page to ...''')

df = pd.read_excel('PILLAR3.xlsx')
df.rename(columns={'other products':'Other Products'}, inplace=True)
categories = df.columns[5:11]

options = st.multiselect(
    'What category of product does your business offer?',
    sorted(categories),
    [])


if options:
    st.text('Great, the attributes you need to report on are:')
    df['mask'] = df[options].apply(lambda x: x.any(), axis=1)
    st.write(df[df['mask'] == True])
