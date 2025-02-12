import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from chat_function import chat_response
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

audio_prompt = None
audio_data = None

os.makedirs("audio_files", exist_ok=True)

def reset_conversation():
    st.session_state["messages"] = [] 
    st.session_state["audio"] = []  
    global audio_prompt, audio_data
    audio_prompt = None
    audio_data = None

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

def main():
    global audio_data, audio_prompt
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "audio" not in st.session_state:
        st.session_state["audio"] = []

    st.set_page_config(
        page_title="RadiantChat",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown("<h1 style='text-align: center; color: #6ca395;'>🤖 <i>RadiantChat</i> 💬</h1>", unsafe_allow_html=True)

    with st.sidebar:
        model = st.selectbox("Select a model:", [
            "gpt-4-turbo", 
            "gpt-4", 
            "gpt-4o",
            "gpt-3.5-turbo",
            "gemini-1.5-pro",
            "gemma:2b",
            "llama3:instruct"
        ], index=0)
        
        with st.expander("Model parameters"):
            model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)

        audio_response = st.checkbox("Audio response", value=False)

        st.button("🗑️ Reset conversation", on_click=reset_conversation)
        st.divider()
        
        speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395")
        if speech_input:
            audio_file_path = "audio_files/input_audio.wav"
            with open(audio_file_path, "wb") as f:
                f.write(speech_input)
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                if audio_data:
                    try:
                        audio_prompt = recognizer.recognize_google(audio_data, language="ar")
                    except sr.UnknownValueError:
                        audio_prompt = recognizer.recognize_google(audio_data)
                    except sr.UnknownValueError as e:
                        st.error(f"Could not request results from Google Speech Recognition service; {e}")

    for message in st.session_state["messages"]:
        with st.chat_message(translate_role_for_streamlit(message["role"])):
            st.markdown(message["text"])

    for audio in st.session_state["audio"]:
        with st.chat_message(translate_role_for_streamlit(audio["role"])):
            st.markdown(audio["text"])

    user_prompt = st.chat_input(f"Ask {model}...")

    if user_prompt:
        st.session_state["messages"].append({"role": "user", "text": user_prompt})
        st.chat_message("user").markdown(user_prompt)
        model_response = chat_response(model, model_temp, user_prompt)

        st.session_state["messages"].append({"role": "assistant", "text": model_response})

        with st.chat_message("assistant"):
            st.markdown(model_response)
        
        if audio_response:
            tts = gTTS(text=model_response, lang="ar")
            audio_output_path = "audio_files/model_response.mp3"
            tts.save(audio_output_path)

            if os.path.exists(audio_output_path):
                audio = AudioSegment.from_mp3(audio_output_path)
                play(audio)
            else:
                st.error(f"Audio file not found: {audio_output_path}")

    elif audio_prompt is not None and audio_data is not None:
        st.session_state["audio"].append({"role": "user", "text": audio_prompt})
        st.chat_message("user").markdown(audio_prompt)
        model_response = chat_response(model, model_temp, audio_prompt)

        st.session_state["audio"].append({"role": "assistant", "text": model_response})

        with st.chat_message("assistant"):
            st.markdown(model_response)
        
        if audio_response:
            tts = gTTS(text=model_response, lang="ar")
            audio_output_path = "audio_files/model_response.mp3"
            tts.save(audio_output_path)

            if os.path.exists(audio_output_path):
                audio = AudioSegment.from_mp3(audio_output_path)
                play(audio)
            else:
                st.error(f"Audio file not found: {audio_output_path}")

if __name__ == "__main__":
    main()
