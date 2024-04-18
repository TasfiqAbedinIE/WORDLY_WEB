import streamlit as st
from navigation import Side_Bar
from datetime import datetime

class streamlit_page_config:
    st.set_page_config(
        page_title="WORDLY - RECORD YOUR WORD",
        layout= "wide",
        initial_sidebar_state='auto',

    )

    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    hide_footer_style = '''<style>.reportview-container .main footer {visibility: hidden;} </style>'''
    st.markdown(hide_footer_style, unsafe_allow_html=True)
    hide_menu_style = '''<style> #MainMenu {visibility: hidden;} </style>'''
    st.markdown(hide_menu_style, unsafe_allow_html=True)


streamlit_page_config()
side_bar = Side_Bar()
side_bar.authenticated_menu()

i = 0
@st.experimental_fragment(run_every='1s')
def second_count():
    time_now = datetime.now()
    time = time_now.strftime("%d-%B-%Y %H:%M:%S %p")
    st.markdown(f"{time} second")

    time_counter = f"""
    <div style='width:20vw; height: 10vh; background-color: blue; border-radius: 1vw'>
        <p style='color:white; font-size: 18px'>
            {time}
        </p>
    </div>
    """
    st.html(time_counter)

second_count()