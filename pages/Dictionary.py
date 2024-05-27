import streamlit as st
from navigation import Side_Bar
from datetime import datetime
import requests

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

    return word, definitions, synonyms, antonyms

r1c1, r1c2 = st.columns([8, 2])
with r1c1:
    search_word = st.text_input("Search Word", placeholder="Search Your Word", label_visibility="collapsed")

with r1c2:
    if st.button("SEARCH", use_container_width=True):
        try:
            word, definitions, synonyms, antonyms = get_word_meaning(api_address, search_word)
            print(word, definitions, synonyms, antonyms)
        except:
            error = True
            error_message = "No Data Found, please check your spelling or word."

def display_word_meaning(word, definitions, synonyms, antonyms):
    st.markdown(f"<h2>{word.upper()}</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Definition:</h4>", unsafe_allow_html=True)
    for i in range(len(definitions)):
        st.markdown(f"<li>{definitions[i]}</li>", unsafe_allow_html=True)


r2c1 = st.container(border=True, height=400)

with r2c1:
    try:
        display_word_meaning(word, definitions, synonyms, antonyms)
    except:
        pass

if error == True:
    st.error(error_message)