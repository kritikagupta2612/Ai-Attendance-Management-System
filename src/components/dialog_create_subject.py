import streamlit as st
from src.database.db import create_subject

st.dialog("Create New Subject")
st.write("Enter the details of new subjects")
sub_id = st.text