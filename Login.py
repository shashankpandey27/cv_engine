import streamlit_authenticator as stauth
import streamlit as st 
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title ="Login")

def get_authenticator():

    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)  

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    return authenticator

# LOGIN WIDGET 
authenticator = get_authenticator()
name, auth_status, username =  authenticator.login()

if auth_status:
    st.session_state["authentication_status"] = True 
    st.session_state["name"] = name 
    st.success(f"Welcome {name}")

    #st.set_page_config(page_title="Candidate CV App")
    st.title("🏠 CV Review Platform")
    st.sidebar.image("logo.svg")

    st.markdown("""
    Welcome! Use the sidebar to navigate between:
    - 🔍 **Resume Review**
    - 📊 **Analytics Dashboard**
    """)
    #st.switch_page("pages/0_Home.py")

# throw errors and logout functionality 
elif auth_status is False:
    st.error('Username/password is incorrect')
    st.info("❗ Forgot your Username/password? Please contact Shashank Pandey.", icon="✉️")
elif auth_status is None:
    st.warning('Please enter your username and password')
    st.info("❗ Don't have an account? Please contact Shashank Pandey for user creation.", icon="✉️")     
