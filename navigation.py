import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

class Side_Bar:
    def __init__(self):
        super().__init__()

    def logout(self):
        # st.session_state.logged_in = False
        st.info("Logged out successfully!")
        sleep(0.5)
        st.switch_page("main.py")

    def authenticated_menu(self):
        st.sidebar.page_link("pages/Record_module.py", label="RECORD")
        st.sidebar.page_link("pages/Learn_module.py", label="LEARN")
        if st.sidebar.button("Log out"):
                        self.logout()
                        st.markdown("""
                                <style>
                                div.stButton > button:first-child {
                                    background-color: #d90429;
                                    color: #ffffff;
                                    border-color: #d90429;
                                    width: 7em;
                                    margin-left: 0.5em;
                                }
                                div.stButton > button:first-child:hover {
                                    background-color: #ef233c;
                                }
                                </style>""", unsafe_allow_html=True)


