from typing import TypedDict

import streamlit as st


def initialize_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []


class GraphState(TypedDict):
    question: str
    department: str