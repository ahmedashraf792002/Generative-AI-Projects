import streamlit as st
import g4f
import streamlit.components.v1 as components

def stream_llm_response_g4f(model_params):
    response_message = ""

    for chunk in g4f.ChatCompletion.create(
        model=model_params["model"],
        messages=st.session_state.messages,
        temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
        stream=True,
    ):
        chunk_text = chunk.choices[0].delta.content or ""
        response_message += chunk_text
        yield chunk_text

def main():
    # --- Page Config ---
    st.set_page_config(
        page_title="RadiantChat",  # Change the page name to RadiantChat
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # --- Header with Dark Background Matching the Page ---
    components.html("""<h1 style="text-align: center; color: #6ca395;">🤖 <i>RadiantChat</i> 💬</h1>""")

    # --- Side Bar ---
    with st.sidebar:
        st.divider()
        model = st.selectbox("Select a model:", ["gpt-3.5", "gpt-4"], index=0)  # Adjust according to g4f model names

        # Model parameters directly in the sidebar
        st.write("⚙️ Model parameters")
        model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)

        model_params = {
            "model": model,
            "temperature": model_temp,
        }

        def reset_conversation():
            if "messages" in st.session_state and len(st.session_state.messages) > 0:
                st.session_state.pop("messages", None)

        st.button(
            "🗑️ Reset conversation", 
            on_click=reset_conversation,
        )

        st.divider()

    # --- Main Content ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Displaying the previous messages if there are any
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            for content in message["content"]:
                if content["type"] == "text":
                    st.write(content["text"])
                elif content["type"] == "image_url":      
                    st.image(content["image_url"]["url"])
                elif content["type"] == "video_file":
                    st.video(content["video_file"])
                elif content["type"] == "audio_file":
                    st.audio(content["audio_file"])

    # Input box for user message
    user_message = st.text_input("Your message:")
    if st.button("Send"):
        if user_message:
            st.session_state.messages.append({"role": "user", "content": [{"type": "text", "text": user_message}]})

            # Stream the response
            response_chunks = stream_llm_response_g4f(model_params)
            for response in response_chunks:
                st.chat_message("assistant").write(response)

            # Store assistant message after streaming
            st.session_state.messages.append({
                "role": "assistant", 
                "content": [{"type": "text", "text": response}],
            })

if __name__ == "__main__":
    main()
