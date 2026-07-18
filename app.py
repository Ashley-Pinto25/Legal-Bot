from dotenv import load_dotenv
from google import genai
import os
import streamlit as st

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL")

st.title("Enterprise Support Assistant")

prompt = st.chat_input("Ask your question")

if prompt:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(response.text)