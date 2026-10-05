import streamlit as st

st.set_page_config(page_title="Business Agent", page_icon="😎")

pg = st.navigation([
    st.Page("1User_ui.py", title="Customer Chat", icon="😎"),
    ## st.Page("2Owner_ui.py", title="Owner Panel", icon="🤑"),
])
pg.run()