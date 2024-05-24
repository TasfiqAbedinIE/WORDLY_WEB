import streamlit as st
from navigation import Side_Bar
import random
from firebase_admin import credentials, db, firestore

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


@st.cache_data
def retrieve_words():
    db = firestore.client()
    collection_ref = db.collection("Words")
    docs = collection_ref.stream()

    word_list = [doc.to_dict() for doc in docs]
    return word_list


word_list = retrieve_words()

title = ("""<div style="text-align: center;">
            <h1 style="color: #0077b6">WORDLY</h1>
        </div>""")
st.html(title)

card_container = st.container(border=True, height=400)
def random_gen():
    num = random.randint(0, len(word_list))
    print(num)
    st.session_state.word = num

with card_container:
    card = f"""
        <div style="text-align: center">
            <h1>{word_list[st.session_state.get("word")]['word']}</h1>
        </div>
    """
    st.html(card)

    if st.button("Next"):
        random_gen()