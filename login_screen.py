import time

import streamlit as st
from Firebase import firebaseConnection

class LogIn:
    def __init__(self):
        super().__init__()
        self.not_registered = False

        r1 = st.container()
        with r1:
            st.markdown(
                "<p style='font-size: 6vw; font-family: fantasy; text-align: center; color: #a2d2ff'>WORDLY</p>",
                unsafe_allow_html=True)
            st.markdown("")
            # st.markdown("")

        login_tab, signup_tab = st.tabs(["LOG IN", "SIGN UP"])
        with login_tab:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.button("LOG IN")
            st.markdown("""
                            <style>
                                div.stButton > button:first-child {
                                    background-color: #a2d2ff;
                                    color: #ffffff;
                                    border-color: #a2d2ff;
                                    width: 10em;
                                    height: 3em;
                                    margin-left: 15.5em;
                                }
                                div.stButton > button:first-child:hover {
                                    background-color: #bde0fe;
                                }
                            </style>""", unsafe_allow_html=True)

            if login_button:
                username_matched, password_matched = firebaseConnection.login_user(username, password)
                if username_matched and password_matched:
                    st.success("LogIn successful")
                    st.session_state.logged_in = True
                    time.sleep(2)
                    st.session_state.username = username
                    st.switch_page("pages/Study_board.py")
                else:
                    st.error("Please check your Username and Password")

        with signup_tab:
            username_sign_up = st.text_input("Username", key="signup_username")
            password_sign_up = st.text_input("Password", type="password", key="signup_password")
            confirm_password_sign_up = st.text_input("Confirm Password", type="password", key="confirm_signup_password")
            signup_button = st.button("SIGN UP", key="signup")
            st.markdown("""
                            <style>
                                div.stButton > button:first-child {
                                    background-color: #a2d2ff;
                                    color: #ffffff;
                                    border-color: #a2d2ff;
                                    width: 10em;
                                    height: 3em;
                                    margin-left: 15.5vw;
                                }
                                div.stButton > button:first-child:hover {
                                    background-color: #bde0fe;
                                }
                            </style>""", unsafe_allow_html=True)
            if signup_button:
                if password_sign_up == confirm_password_sign_up:
                    try:
                        firebaseConnection.registering_user(username_sign_up, password_sign_up)
                        st.success("Successfully Registered")
                    except Exception as e:
                        st.error(e)
                else:
                    st.warning("Password didn't match")













