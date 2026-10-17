import streamlit as st

def footer_home():
    logo_url =  r"https://c8.alamy.com/comp/2JDYGB7/k-letter-monogram-elegant-luxury-k-logo-calligraphic-style-corporate-identity-and-personal-logo-vector-design-2JDYGB7.jpg";
  
    st.markdown(f""" 
        <div style=" margin-top :2rem;
        display:flex;
        gap: 6px;
        justify-content:center ; 
        align-items:center ">
    <p style = "font-weight:bold; color: white"> 
      Created ❤️ by 
    </p>
      <img src='{logo_url}' style= 'max-height:25px'>
      </div>
            """,
      unsafe_allow_html=True)

def footer_dashboard():
      logo_url =  r"https://c8.alamy.com/comp/2JDYGB7/k-letter-monogram-elegant-luxury-k-logo-calligraphic-style-corporate-identity-and-personal-logo-vector-design-2JDYGB7.jpg";
  
      st.markdown(f""" 
        <div style=" margin-top :2rem;
        display:flex;
        gap: 6px;
        justify-content:center ; 
        align-items:center ">
    <p style = "font-weight:bold; color: black"> 
      Created ❤️ by 
    </p>
      <img src='{logo_url}' style= 'max-height:25px'>
      </div>
            """,
      unsafe_allow_html=True)