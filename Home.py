import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    st.title(":bar_chart: Emporio Dashboard")

)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)