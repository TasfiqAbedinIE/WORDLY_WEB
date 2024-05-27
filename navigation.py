import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

class Side_Bar:
    def __init__(self):
        super().__init__()

    def logout(self):
        # st.session_state.logged_in = False
        st.sidebar.info("Logged out successfully!")
        sleep(0.5)
        st.switch_page("main.py")

    def authenticated_menu(self):
        username = st.session_state.get('username')
        st.sidebar.markdown(f"Welcome, {username}")
        st.sidebar.page_link("pages/Study_board.py", label="STUDY BOARD", icon=":material/app_registration:")
        st.sidebar.page_link("pages/Dictionary.py", label="DICTIONARY", icon=":material/dictionary:")
        st.markdown("")
        st.markdown("")
        st.markdown("")
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


