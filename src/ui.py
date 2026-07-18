
import streamlit as st

def load_css():
    with open("assets/style.css", "r") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )



def show_sidebar():

    with st.sidebar:

        st.title("Support Bot")

        if st.button("Clear Chat"):

            st.session_state.messages = []

            st.rerun()

        st.divider()

        st.subheader("Departments")

        departments = [
            "HR",
            "Accounts",
            "Web",
            "App",
            "Customer Relations"
        ]

        for department in departments:

            st.write(f"📂 {department}")


def display_chat():

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"<div class='user-msg'>{message['content']}</div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"<div class='bot-msg'>{message['content']}</div>",
                unsafe_allow_html=True
            )