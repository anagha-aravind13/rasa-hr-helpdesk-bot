# HR Helpdesk Chatbot

An enterprise-ready HR support assistant built with Rasa and PostgreSQL. This project demonstrates a practical HR chatbot capable of handling:

- HR FAQs
- leave policy and balance checks
- payroll queries
- work-from-home policies
- office timings
- holiday calendar information
- password reset guidance
- employee ID card requests

A simple Streamlit interface is included for UI demonstration, while PostgreSQL is used for FAQ storage and custom action support.

## Project Overview
This assistant is designed for HR support scenarios and is structured to showcase an enterprise-ready chatbot with:

- intent recognition for HR-related questions
- fallback handling for unclear inputs
- dynamic FAQ retrieval from PostgreSQL
- custom actions for leave balance and service lookups
- optional Streamlit demo UI for interaction

## Architecture
The project is organized into these components:

- `data/`
  - `nlu.yml`: intent examples and training phrases
  - `stories.yml`: conversation flows
  - `rules.yml`: fallback and rule-based behavior
- `domain.yml`
  - intents, responses, actions, and session configuration
- `actions/actions.py`
  - custom actions and database integration
- `streamlit_app.py`
  - optional chat UI for demonstration
- `.env`
  - environment configuration for database and service URLs

## Setup
Install dependencies in a Python virtual environment.

```bash
python -m venv venv
& ".\venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
```

Configure the `.env` file with database credentials and the Rasa webhook URL if needed.

## Database
The assistant uses PostgreSQL for FAQ storage and leave-related data.

Use the following database schema and sample data:

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    leave_balance INTEGER
);

CREATE TABLE leave_requests (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER,
    leave_date DATE,
    reason TEXT,
    status VARCHAR(50)
);

INSERT INTO employees (name, email, leave_balance)
VALUES ('John', 'john@gmail.com', 12);

INSERT INTO leave_requests (employee_id, leave_date, reason, status)
VALUES (1, '2025-08-20', 'Sick Leave', 'Pending');

CREATE TABLE faq (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO faq (question, answer) VALUES
('What is the WFH policy?', 'Employees can work remotely up to 2 days per week with manager approval.'),
('When will salary be credited?', 'Payroll is processed on the last working day of each month.'),
('What are the office timings?', 'Standard office hours are 9:00 AM to 6:00 PM Monday through Friday.'),
('What are the upcoming company holidays?', 'The upcoming company holidays are Independence Day and Onam.'),
('How do I reset my password?', 'You can reset your password using the internal self-service portal or contact IT support.'),
('How do I request a new ID card?', 'Please raise an admin request through the HR portal for ID card replacement.');
```

## Running the Bot
Train the assistant, start the action server, and run the bot.

```bash
rasa train
rasa run actions
rasa shell
```

For the Streamlit demo UI:

```bash
streamlit run streamlit_app.py
```

## Sample Interaction Flow
The bot is built to handle questions such as:

- `what is leave policy?`
- `can I work from home?`
- `when will salary be credited?`
- `what are the office timings?`
- `what holidays are coming up?`
- `reset my password`
- `I lost my ID card`

Expected responses include:

- `Employees receive 12 casual leaves annually.`
- `Employees can work remotely up to 2 days per week with manager approval.`
- `Payroll is processed on the last working day of each month.`
- `Standard office hours are 9:00 AM to 6:00 PM Monday through Friday.`
- `Please raise an admin request through the HR portal for ID card replacement.`

## Screenshots
The `screenshots/` folder contains the visual evidence of the chatbot flow, UI screens, and interaction examples.

- [Chatbot flow screenshots](screenshots/)
- [Architecture diagram](screenshots/architecture.png)

## Notes
This project is intended as a realistic HR support assistant showcase, with both NLU-based conversational flows and database-backed FAQ retrieval.