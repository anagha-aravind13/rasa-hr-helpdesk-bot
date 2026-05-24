from sqlalchemy import create_engine
from rasa_sdk import Action

engine = create_engine(
    "postgresql://postgres:1234@localhost/hr_chatbot"
)

class ActionCheckLeaveBalance(Action):

    def name(self):
        return "action_check_leave_balance"

    def run(self, dispatcher, tracker, domain):

        connection = engine.connect()

        result = connection.execute(
            "SELECT leave_balance FROM employees WHERE id=1"
        )

        balance = result.fetchone()[0]

        dispatcher.utter_message(
            text=f"Your remaining leave balance is {balance} days."
        )

        return []