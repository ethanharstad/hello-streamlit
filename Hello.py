import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import random
import time
import os
from openai import OpenAI

LOGGER = get_logger(__name__)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Setup OpenAI model
client = OpenAI(api_key=OPENAI_API_KEY)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


def run():
    st.title("Simple Bot")

    # Setup chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })


if __name__ == "__main__":
    run()
