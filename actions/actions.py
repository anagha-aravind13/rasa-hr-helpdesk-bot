import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from rasa_sdk import Action


def load_dotenv(dotenv_path=".env"):
    if not os.path.exists(dotenv_path):
        return
    with open(dotenv_path, "r", encoding="utf-8") as f:
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


try:
    from dotenv import load_dotenv as _load_dotenv
except ImportError:
    _load_dotenv = load_dotenv

_load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hr_chatbot")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

engine = create_engine(DATABASE_URL)


class ActionCheckLeaveBalance(Action):

    def name(self):
        return "action_check_leave_balance"

    def run(self, dispatcher, tracker, domain):

        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT leave_balance FROM employees WHERE id=1")
            )
            balance = result.fetchone()[0]

        dispatcher.utter_message(
            text=f"Your remaining leave balance is {balance} days."
        )

        return []


class ActionFaqLookup(Action):

    def name(self):
        return "action_faq_lookup"

    def run(self, dispatcher, tracker, domain):
        query = tracker.latest_message.get("text", "").strip()

        if not query:
            dispatcher.utter_message(
                text="Please ask a FAQ-style question so I can look it up for you."
            )
            return []

        search_query = f"%{query}%"
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT answer FROM faq "
                    "WHERE question ILIKE :search_query "
                    "   OR answer ILIKE :search_query "
                    "ORDER BY char_length(question) ASC "
                    "LIMIT 1"
                ),
                {"search_query": search_query},
            ).fetchone()

        if result:
            dispatcher.utter_message(text=result[0])
        else:
            dispatcher.utter_message(
                text=(
                    "I couldn't find an FAQ answer for that. "
                    "Please try asking a different HR question, or ask about leave policy, payroll, or onboarding."
                )
            )

        return []