import os

import streamlit as st
from streamlit.logger import get_logger
from openai import OpenAI

LOGGER = get_logger(__name__)


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def generate_scenario():
    scenario = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": st.session_state["system"]},
            {"role": "user", "content": st.session_state["user"]},
        ],
    )
    st.markdown(scenario.choices[0].message.content)

def run():
    st.title('Brief Initial Report')

    with st.form("scenario"):
        st.text_area("System Prompt", key="system")
        st.text_area("User Prompt", key="user")
        st.selectbox(
            label="Scenario Type",
            options=[
                "EMS",
                "MVC",
                "Structure Fire",
                "Hazmat",
            ],
            index=None,
            key="scenario_type",
        )
        st.form_submit_button("Go", on_click=generate_scenario)

if __name__ == "__main__":
    run()
