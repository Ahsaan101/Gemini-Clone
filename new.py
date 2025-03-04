import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the configuration for the Generative Model
generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192
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
    # Create a GenerativeModel instance with 'gemini-1.5-flash-latest' as the model type
    llm = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    # Generate content based on the input text
    response = llm.generate_content(input_text)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Chat")

st.title("Gemini Clone")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input("Message Gemini"):
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


