import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout,style_background_home
def home_screen():

    style_base_layout()
    style_background_home()
    header_home()

  
    col1,col2 = st.columns(2 , gap="large")
    with col1:
         st.header("I am student");
         st.image("https://tse3.mm.bing.net/th/id/OIP.e2CPtIAKG1euf6JGQBs2wgHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3", width=120)
         if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']= 'student' 
            st.rerun()
    with col2:
       st.header("I am teacher");
       st.image("https://clipart-library.com/newhp/kissclipart-cartoon-blackboard-clip-art-teacher-31289aa4f8040b25.png" ,width=120 )
       if st.button('Teacher Portal', type ='primary', icon=':material/arrow_outward:', icon_position='right'):
           st.session_state[ 'login_type'] = 'teacher'
           st.rerun()
    footer_home()