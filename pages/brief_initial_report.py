import os

import streamlit as st
from streamlit.logger import get_logger
from openai import OpenAI

LOGGER = get_logger(__name__)

SCENARIO_SYSTEM_PROMPT = """
You are a trainer for emergency responder communications.
Your primary purpose is to provide example emergency scenarios and evaluate users responses.
When provided with an scenario type, generate the requested scenario information.
"""


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def generate_scenario():
    messages = [
        {"role": "system", "content": SCENARIO_SYSTEM_PROMPT},
    ]
    # Generate scenario
    messages.append({
        "role": "user", "content": st.session_state["user"],
    })
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
    )
    scenario = response.choices[0].message.content
    messages.append({
        "role": "assistant", "content": scenario,
    })
    st.markdown(scenario)
    # Generate address
    messages.append({
        "role": "user", "content": "Generate a realistic address for the incident. The address should be a street address, an intersection, or a block of a street.",
    })
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
    )
    address = response.choices[0].message.content
    messages.append({
        "role": "assistant", "content": address,
    })
    st.markdown(address)
    # Generate time
    messages.append({
        "role": "user", "content": "Generate a realistic time for the incident",
    })
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
    )
    time = response.choices[0].message.content
    messages.append({
        "role": "assistant", "content": time,
    })
    st.markdown(time)
    # Generate dispatch
    dispatch = generate_dispatch(address, scenario)
    st.markdown(dispatch)
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=dispatch,
    )
    st.audio(response.content)

def generate_dispatch(location, incident):
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": "You are a 911 dispatcher. When provided with a location and incident you will dispatch Engine 65 and Medic 176. The incident description in the dispatch should be a single sentence and should only describe what happened in broad strokes without extra details."},
            {"role": "user", "content": "Location: 123 First St"},
            {"role": "user", "content": "Incident: two vehicle accident with injuries"},
            {"role": "assistant", "content": "Attention Engine 65, Medic 176, Engine 65, Medic 176. You are needed emergent to One Two Three First street, 123 First Street for a two vehicle accident with injuries. Again that is One Two Three First Street, 123 First street for a two vehicle accident with injuries."},
            {"role": "user", "content": location},
            {"role": "user", "content": incident},
        ],
    )
    dispatch = response.choices[0].message.content
    return dispatch

def run():
    st.title('Brief Initial Report Trainer')

    with st.form("scenario"):
        # st.text_area("System Prompt", key="system")
        st.text_area("User Prompt", key="user")
        st.selectbox(
            label="Scenario Type",
            options=[
                "EMS",
                "MVC",
                "Structure Fire",
                "Hazmat",
                "Custom",
            ],
            index=None,
            key="scenario_type",
        )
        st.form_submit_button("Go", on_click=generate_scenario)

if __name__ == "__main__":
    run()
