from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import datetime

# Load environment variables
load_dotenv()

# Set up the configuration for the Generative Model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the Gemini model
def get_gemini_response(input_text):
    # Create a GenerativeModel instance with 'gemini-1.5-pro' as the model type
    llm = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    # Generate content based on the input text
    response = llm.generate_content(input_text)
    return response.text

# Function to save a new chat session
def save_chat(session):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["previous_chats"].append({"timestamp": timestamp, "session": session})

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Chat")

st.title("ChatGPT-like Clone using Gemini")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for previous chats
if "previous_chats" not in st.session_state:
    st.session_state.previous_chats = []

# Sidebar for previous chat sessions
st.sidebar.header("Previous Chats")
if st.session_state.previous_chats:
    for i, chat in enumerate(st.session_state.previous_chats):
        if st.sidebar.button(f"Chat from {chat['timestamp']}"):
            st.session_state.messages = chat["session"]
else:
    st.sidebar.write("No previous chats yet.")

# Display the chat messages from the current session
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input("You:"):
    # Add user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response using Gemini
    response = get_gemini_response(prompt)
    
    # Add assistant's message to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save the current chat session after every interaction
    save_chat(st.session_state.messages)
