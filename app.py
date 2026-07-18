import streamlit as st
import time

from src.state import initialize_session
from src.ui import load_css
from src.ui import show_sidebar
from src.ui import display_chat
from src.gemini import ask_gemini

st.set_page_config(
    page_title="Support Bot",
    page_icon="🤖",
    layout="wide"
)

load_css()

initialize_session()

show_sidebar()

st.markdown(
    "<div class='chat-title'>Enterprise Support Assistant</div>",
    unsafe_allow_html=True
)

display_chat()

prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.rerun()


if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):

    question = st.session_state.messages[-1]["content"]

    placeholder = st.empty()

    with placeholder.container():

        st.markdown(
            "<div class='bot-msg'>Thinking...</div>",
            unsafe_allow_html=True
        )

    try:

        answer = ask_gemini(question)

    except Exception as e:

        answer = str(e)

    time.sleep(0.2)

    placeholder.empty()

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()