import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama
from langchain_community.llms import Ollama

# Streamlit web app configuration
st.set_page_config(
    page_title="DF Chat",
    page_icon="💬",
    layout="centered"
)

# Function to read data
def read_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Streamlit page title
st.title("🤖 DataFrame ChatBot - Ollama")

# Initialize chat history and DataFrame in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "df" not in st.session_state:
    st.session_state.df = None

# File upload widget
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file:
    st.session_state.df = read_data(uploaded_file)
    st.write("DataFrame Preview:")
    st.dataframe(st.session_state.df.head())

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask LLM...")

if user_prompt:
    # Add user's message to chat history and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Loading the LLM
    llm = Ollama(model="llama3:instruct", temperature=0)

    # Create the DataFrame agent
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        st.session_state.df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )

    # Try executing the agent's response
    try:
        # Use run() instead of invoke()
        response = pandas_df_agent.run(user_prompt)
        assistant_response = response["output"]

    except Exception as e:
        # Display any errors encountered during execution
        assistant_response = f"Error: {str(e)}"

    # Add the assistant's response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
