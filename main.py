import streamlit as st
from login_screen import LogIn
import firebase_admin
from firebase_admin import credentials

class Page_config:
    def __init__(self):
        super().__init__()
        st.set_page_config(
            page_title="LOG IN - SQUARE DMS",
            initial_sidebar_state="collapsed"
        )
        st.markdown(
            """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

Page_config()

if not firebase_admin._apps:
    cred =credentials.Certificate(
        "Firebase/wordly-12d2f-firebase-adminsdk-czymf-011d95e979.json"
    )
    firebase_admin.initialize_app(cred)


LogIn()