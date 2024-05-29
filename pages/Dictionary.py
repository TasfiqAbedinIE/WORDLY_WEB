import streamlit as st
from navigation import Side_Bar
from datetime import datetime
import requests
from firebase_admin import credentials, db, firestore

api_address = "https://api.dictionaryapi.dev/api/v2/entries/en/"

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

# i = 0
# @st.experimental_fragment(run_every='1s')
# def second_count():
#     time_now = datetime.now()
#     time = time_now.strftime("%d-%B-%Y %H:%M:%S %p")
#     st.markdown(f"{time} second")
#
#     time_counter = f"""
#     <div style='width:20vw; height: 10vh; background-color: blue; border-radius: 1vw'>
#         <p style='color:white; font-size: 18px'>
#             {time}
#         </p>
#     </div>
#     """
#     st.html(time_counter)
#
# second_count()

error = False
def get_word_meaning(url, get_word):
    response = requests.get(url+get_word)
    if response.status_code == 200:
        data =response.json()

    word = data[0]['word']
    meanings = data[0]['meanings']
    phonetics = data[0]['phonetics']

    definitions = []
    synonyms = []
    antonyms = []

    # Extract and print meanings, synonyms, and antonyms
    for meaning in meanings:
        part_of_speech = meaning['partOfSpeech']
        # print(f"Part of Speech: {part_of_speech}")

        for definition in meaning['definitions']:
            # print(f"Definition: {definition['definition']}")
            definitions.append(definition['definition'])

            if definition['synonyms']:
                # print(f"Synonyms: {', '.join(definition['synonyms'])}")
                synonyms.append(definition['synonyms'])

            if definition['antonyms']:
                # print(f"Antonyms: {', '.join(definition['antonyms'])}")
                antonyms.append(definition['antonyms'])

        if meaning['synonyms']:
            # print(f"Overall Synonyms: {', '.join(meaning['synonyms'])}")
            synonyms.append(meaning['synonyms'])

        if meaning['antonyms']:
            # print(f"Overall Antonyms: {', '.join(meaning['antonyms'])}")
            antonyms.append(meaning['antonyms'])


    # Extract and print phonetics
    for phonetic in phonetics:
        text = phonetic.get('text', 'N/A')
        audio = phonetic.get('audio', 'N/A')
        print(f"Phonetic: {text}, Audio: {audio}")

    return word, definitions, synonyms, antonyms, part_of_speech

r1c1, r1c2 = st.columns([8, 2])
with r1c1:
    search_word = st.text_input("Search Word", placeholder="Search Your Word", label_visibility="collapsed")

with r1c2:
    if st.button("SEARCH", use_container_width=True):
        try:
            word, definitions, synonyms, antonyms, pos = get_word_meaning(api_address, search_word)
            # print(word, definitions, synonyms, antonyms)
        except:
            error = True
            error_message = "No Data Found, please check your spelling or word."

def display_word_meaning(word, definitions, synonyms, antonyms, pos):
    # display_pos = ','.join(map(str, pos))
    st.markdown(f"<p style='font-size: 2vw; font-weight: bold'>{word.upper()}, <span style='font-size: 1vw; color:#3a86ff'>{pos}</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 2vw; font-weight: bold; color:#3a86ff'>Definition:</p>", unsafe_allow_html=True)
    for i in range(len(definitions)):
        st.markdown(f"<li>{definitions[i]}</li>", unsafe_allow_html=True)

    syn_col, ant_col = st.columns(2)
    with syn_col:
        st.markdown("<p style='font-size: 2vw; font-weight: bold; color:#3a86ff'>Synonyms:</p>", unsafe_allow_html=True)
        merge_synonyms = [item for sublist in synonyms for item in sublist]
        unique_synonyms = list(set(merge_synonyms))
        display_synonyms = ','.join(map(str, unique_synonyms))
        st.markdown(display_synonyms)

    with ant_col:
        st.markdown("<p style='font-size: 2vw; font-weight: bold; color:#3a86ff'>Antonyms:</p>", unsafe_allow_html=True)
        merge_antonyms = [item for sublist in antonyms for item in sublist]
        unique_antonyms = list(set(merge_antonyms))
        display_antonyms = ','.join(map(str, unique_antonyms))
        st.markdown(display_antonyms)



r2c1 = st.container(border=True, height=400)

with r2c1:
    try:
        display_word_meaning(word, definitions, synonyms, antonyms, pos)
    except:
        pass

@st.experimental_dialog("REGISTER WORD")
def word_register_screen(word, pos, definition):
    col1, col2 = st.columns(2)
    with col1:
        dicword = st.text_input("WORD", value=word.upper())
    with col2:
        dicpsp = st.text_input("PARTS OF SPEECH", value=pos)
    dicdefinition = st.text_area("DEFINITION", value=definition)
    example = st.text_area("EXAMPLE")

    if st.button("REGISTER"):
        def record_word(dicword, dicpsp, dicdefinition, example):
            db = firestore.client()
            word_data = {
                'word': dicword,
                'psp': dicpsp,
                'definition': dicdefinition,
                'example': example,
                'user': st.session_state.get('username'),
                'letter': dicword[0]
            }

            print(word_data)
            try:
                document_id = dicword
                db.collection("Words").document(document_id).set(word_data)
            except:
                st.error("Failed to Register.")

        record_word(dicword, dicpsp, dicdefinition, example)
        st.rerun()

if error == False:
  if st.button("Register This Word"):
      word, definitions, synonyms, antonyms, pos = get_word_meaning(api_address, search_word)
      word_register_screen(word, pos, definitions[0])

elif error == True:
    st.error(error_message)