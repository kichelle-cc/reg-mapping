import streamlit as st 
import os
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

add_logo()
prefix=os.getcwd()
path_to_html = r"C:\Users\kcomriecarson\OneDrive - Deloitte (O365D)\Data Model\Data Models\ESG Reg & Data Model Mapping_v7.html" 
path_to_html = prefix + '/streamlit/imgs/ESG Reg & Data Model Mapping_v7.html'
# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.title("Mapping Overview")
st.divider()
st.caption("A simple, interactive view of our current regulatory framework mapping")
# st.write(help(st.components.v1.html))
st.components.v1.html(html_data, height=1400, scrolling=False)#,width=1000,height=1400)