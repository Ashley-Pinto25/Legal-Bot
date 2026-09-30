from __future__ import annotations

import streamlit as st

from src.state import LEGAL_DISCLAIMER

EXAMPLES = (
    "I haven't received my salary.", "My landlord won't return my deposit.",
    "I received a legal notice.", "I bought a defective product.",
    "Someone is misusing my personal information.", "I want to understand my legal rights.",
)


def load_css() -> None:
    with open("assets/style.css", encoding="utf-8") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


def show_sidebar(conversations: list[dict], active_id: str) -> str | None:
    with st.sidebar:
        st.markdown("## ⚖️ Indian Legal Assistant")
        st.caption("Legal information and research — not legal representation.")
        if st.button("＋ New conversation", use_container_width=True):
            return "new"
        st.markdown("**Your conversations**")
        for conversation in conversations:
            marker = "● " if conversation["id"] == active_id else ""
            if st.button(marker + conversation["title"], key=f"conversation-{conversation['id']}", use_container_width=True):
                return conversation["id"]
        st.divider()
        st.markdown("**Research principles**")
        st.caption("• Source-grounded\n\n• No invented citations\n\n• Jurisdiction-aware\n\n• Privacy-conscious")
        st.divider()
        st.caption(LEGAL_DISCLAIMER)
        st.caption("Conversation history is stored locally for this browser profile.")
    return None


def display_chat() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("facts"):
                with st.expander("Situation summary", expanded=False):
                    st.json(message["facts"])


def show_welcome() -> None:
    st.markdown("### Describe your situation")
    st.write("Use ordinary language. You do not need to know the name of a law or a section.")
    columns = st.columns(2)
    for index, example in enumerate(EXAMPLES):
        if columns[index % 2].button(example, key=f"example-{index}", use_container_width=True):
            st.session_state.pending_question = example
            st.rerun()
