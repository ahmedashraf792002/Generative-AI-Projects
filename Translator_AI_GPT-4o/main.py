import streamlit as st
from translator_utils import translate_using_g4f

st.set_page_config(
    page_title="Translator.AI",
    page_icon="🈶",
    layout="centered"
)

# streamit page title
st.title("🈶 Translator App  - GPT-4o")

col1, col2 = st.columns(2)

with col1:
    all_languages_list = [
    "Arabic", "English" ,"Spanish", "French", "German", "Latin", "Chinese", "Japanese", "Russian", "Portuguese",
    "Italian", "Hindi", "Korean", "Dutch", "Greek", "Turkish", "Swedish", "Norwegian", "Polish",
    "Danish", "Finnish", "Czech", "Hungarian", "Hebrew", "Vietnamese", "Thai", "Indonesian", "Swahili",
    "Urdu", "Bengali", "Punjabi", "Tamil", "Telugu", "Malay", "Filipino", "Ukrainian", "Romanian",
    "Bulgarian", "Serbian", "Croatian", "Slovak", "Slovenian", "Lithuanian", "Latvian", "Estonian",
    "Irish", "Welsh", "Scottish Gaelic", "Icelandic", "Maltese", "Basque", "Galician"  
    ] 
    input_language = st.selectbox(label="Input Language", options=all_languages_list)

with col2:
    output_languages_list = [x for x in all_languages_list if x != input_language]
    output_language = st.selectbox(label="Output Language", options=output_languages_list)

input_text = st.text_area("Type the text to be translated")

if st.button("Translate"):
    translated_text = translate_using_g4f(input_language, output_language, input_text)
    st.success(translated_text)