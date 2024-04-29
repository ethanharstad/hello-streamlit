import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import random
import time

LOGGER = get_logger(__name__)


def response_generator():
    response = random.choice([
        "I am a pretty basic chat bot. How can I assist you today?",
        "Hello human. Is there anything I can help you with?"
    ])
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def run():
    st.title("Simple Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })


if __name__ == "__main__":
    run()
