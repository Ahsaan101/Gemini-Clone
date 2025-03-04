# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

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

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to get response from Gemini model
def get_gemini_response(question):
    response = genai.generate_text(
        prompt=question,
        temperature=generation_config['temperature'],
        top_p=generation_config['top_p'],
        top_k=generation_config['top_k'],
        max_output_tokens=generation_config['max_output_tokens'],
    )
    return response.result

## Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini Clone")

input_text = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

## If ask button is clicked
if submit:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    st.write(response)