import streamlit as st
from navigation import Side_Bar
import random
from firebase_admin import credentials, db, firestore


class streamlit_page_config:
    st.set_page_config(
        page_title="WORDLY - RECORD YOUR WORD",
        layout="wide",
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
# print(word_list)

title = ("""<div style="text-align: center;">
            <p style="color: #0077b6; font-size: 3vw; font-weight: bold">WORDLY</p>
        </div>""")
st.html(title)

card_container = st.container(border=True, height=400)
number = 0

def random_gen():
    num = random.randint(0, len(word_list) - 1)
    print(num)
    st.session_state.word = num


def display_word_function():
    with card_container:
        try:
            card = f"""
                    <div style="text-align: center; margin-bottom: 15vh">
                        <h1>{word_list[st.session_state.get("word")]['word'].upper()}</h1>
                        <p>{word_list[st.session_state.get("word")]['psp']}</p>
                        <p style="font-size: 24px; font-weight: bold">{word_list[st.session_state.get("word")]['definition']}</p>
                        <p>{word_list[st.session_state.get("word")]['example']}</p>
                    </div>
                    """
            st.html(card)

        except:
            card = f"""
                    <div style="text-align: center">
                        <h1>Press Next to Start</h1>
                    </div>
                    """
            st.html(card)

# display_word_function()
# if st.session_state.get("word") == None:
#     with card_container:
#         card = f"""
#                     <div style="text-align: center">
#                         <h1>Press Next to Start</h1>
#                     </div>
#                 """
#         st.html(card)

print(st.session_state.get("word"))

btn1, btn2, btn3 = st.columns((2, 15, 2))
with btn1:
    if st.button("LEARNED", use_container_width=True):
        pass
with btn2:
    pass
with btn3:
    if st.button("NEXT", use_container_width=True):
        random_gen()
        display_word_function()


record_container = st.container()
with record_container:
    def record_word(word, psp, definition, example):
        db = firestore.client()
        word_data = {
            'word': word,
            'psp': psp,
            'definition': definition,
            'example': example,
            'user': st.session_state.get('username'),
            'letter': word[0]
        }

        print(word_data)
        try:
            document_id = word
            db.collection("Words").document(document_id).set(word_data)
        except:
            st.error("Failed to Register.")


    @st.experimental_dialog("REGISTER WORD")
    def word_register_screen():
        col1, col2 = st.columns(2)
        with col1:
            word = st.text_input("WORD")
        with col2:
            psp = st.text_input("PARTS OF SPEECH")
        definition = st.text_area("DEFINITION")
        example = st.text_area("EXAMPLE")

        if st.button("REGISTER"):
            record_word(word, psp, definition, example)
            st.rerun()
            # try:
            #     record_word(word, psp, definition, example)
            #     st.rerun()
            # except:
            #     st.error("Failed to register")


    if st.button("REGISTER NEW WORD"):
        word_register_screen()
        display_word_function()
