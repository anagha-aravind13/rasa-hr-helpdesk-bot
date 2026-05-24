import os
import json
from pathlib import Path

import requests
import streamlit as st


def load_dotenv(dotenv_path=".env"):
    dotenv_file = Path(dotenv_path)
    if not dotenv_file.exists():
        return
    with dotenv_file.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv()

RASA_URL = os.getenv("RASA_SERVER_URL", "http://localhost:5005/webhooks/rest/webhook")
SAMPLE_QUESTIONS = [
    "What is the WFH policy?",
    "When will salary be credited?",
    "What are the office timings?",
    "What are the upcoming company holidays?",
    "How do I reset my password?",
    "I lost my ID card",
]


def send_to_rasa(message: str):
    payload = {"sender": "streamlit_user", "message": message}
    response = requests.post(RASA_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def add_message(role: str, text: str):
    st.session_state.messages.append({"role": role, "text": text})


def render_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['text']}")
        else:
            st.markdown(f"**Bot:** {message['text']}")


def main():
    st.set_page_config(page_title="HR Helpdesk Chatbot", page_icon="🤖")
    st.title("Enterprise HR Support Assistant")
    st.write(
        "Ask questions about leave, payroll, policies, onboarding, IT support, or HR FAQs."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "bot",
                "text": (
                    "Welcome to the Enterprise HR Support Assistant. "
                    "Ask me about leave policy, payroll, WFH, employee services, or IT support."
                ),
            }
        ]

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here", "")
        submit = st.form_submit_button("Send")

    if submit and user_input.strip():
        add_message("user", user_input.strip())
        try:
            bot_responses = send_to_rasa(user_input.strip())
            if not bot_responses:
                add_message(
                    "bot",
                    "I couldn't get an answer from the bot. Please try another question.",
                )
            else:
                for item in bot_responses:
                    text = item.get("text") or item.get("custom", json.dumps(item))
                    add_message("bot", text)
        except requests.RequestException as exc:
            add_message(
                "bot",
                f"Unable to connect to Rasa server at {RASA_URL}. Error: {exc}",
            )

    render_chat()

    with st.expander("Sample questions"):
        for sample in SAMPLE_QUESTIONS:
            st.write(f"- {sample}")

    st.markdown(
        "---\n"
        "**Configuration**: The app uses `RASA_SERVER_URL` from `.env` or defaults to `http://localhost:5005/webhooks/rest/webhook`."
    )


if __name__ == "__main__":
    main()
