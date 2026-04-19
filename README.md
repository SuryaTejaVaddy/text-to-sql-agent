 Text-to-SQL Agent

  A natural language to SQL pipeline that lets you ask questions about your
  PostgreSQL database using Google Gemini AI — no SQL knowledge required.

  How It Works

  1. Ask — You type a question in plain English
  2. Generate — Gemini reads your database schema and converts your question
   into a SQL query
  3. Execute — The query runs against your PostgreSQL database
  4. Self-Correct — If the query fails, the error is sent back to Gemini and
   it retries up to 3 times

  Prerequisites

  - Python 3.10+
  - A Gemini API key from aistudio.google.com (free tier)
  - A running PostgreSQL database (local or hosted on Neon.tech)
  - GitHub Codespaces (recommended) or local Python environment

  Setup

  1. Clone the Repository

  git clone https://github.com/SuryaTejaVaddy/text-to-sql-agent.git
  cd text-to-sql-agent

  2. Install Dependencies

  pip install -r requirements.txt

  3. Set Your API Keys

  Option A — GitHub Codespaces (recommended):

  Go to your GitHub repository → Settings → Secrets and variables →
  Codespaces → New secret:

  ┌────────────────┬───────────────────────────────────┐
  │      Name      │               Value               │
  ├────────────────┼───────────────────────────────────┤
  │ GEMINI_API_KEY │ your Gemini API key               │
  ├────────────────┼───────────────────────────────────┤
  │ DATABASE_URL   │ your PostgreSQL connection string │
  └────────────────┴───────────────────────────────────┘

  Then restart your Codespace. If keys don't load automatically, run:
  export GEMINI_API_KEY="your-api-key-here"
  export DATABASE_URL="postgresql://user:password@host/dbname"

  Option B — Local .env file:
  echo 'GEMINI_API_KEY=your-api-key-here' > .env
  echo 'DATABASE_URL=postgresql://user:password@host/dbname' >> .env

  Running the App

  Step 1 — Load sample data (optional)

  If you don't have a database yet, load the Northwind sample dataset
  (customers, orders, products):
  python -c "
  import psycopg2, urllib.request
  url = 'https://raw.githubusercontent.com/pthom/northwind_psql/master/north
  wind.sql'
  sql = urllib.request.urlopen(url).read().decode()
  conn = psycopg2.connect('YOUR_DATABASE_URL_HERE')
  conn.autocommit = True
  conn.cursor().execute(sql)
  conn.close()
  print('Done!')
  "

  Step 2 — Start the app

  python app.py
  Open your browser and go to http://localhost:7860

  Step 3 — Ask a question

  Type a question like:
  Show me the top 5 customers by total order value
  Click Run Query. You'll see the generated SQL and a results table below
  it.

  Example Questions

  Which products have never been ordered?
  List all employees and how many orders they handled
  What is the average freight cost per country?
  Show all orders placed in 1997

  Project Structure

  text-to-sql-agent/
  ├── app.py            # Gradio web UI — the entry point
  ├── agent.py          # Sends question + schema to Gemini, returns SQL
  ├── self_correct.py   # Retry loop — retries up to 3 times on failure
  ├── db.py             # PostgreSQL connection, query execution, schema
  reader
  ├── schema.py         # Validates that AI only returns SELECT queries
  └── requirements.txt  # Python dependencies

  Configuration

  Edit agent.py to change defaults:

  ┌──────────────┬────────────────────────────────┬──────────────────────┐
  │   Setting    │            Default             │     Description      │
  ├──────────────┼────────────────────────────────┼──────────────────────┤
  │ model_name   │ gemini-2.5-flash-preview-04-17 │ Gemini model used    │
  │              │                                │ for generation       │
  ├──────────────┼────────────────────────────────┼──────────────────────┤
  │              │                                │ Lower = more         │
  │ temperature  │ 0.0                            │ deterministic SQL    │
  │              │                                │ output               │
  ├──────────────┼────────────────────────────────┼──────────────────────┤
  │              │                                │ Max retries if SQL   │
  │ MAX_ATTEMPTS │ 3                              │ fails (in            │
  │              │                                │ self_correct.py)     │
  └──────────────┴────────────────────────────────┴──────────────────────┘

  Safety

  The agent only allows SELECT queries. Any AI-generated query that tries to
   insert, update, or delete data is automatically rejected before it
  reaches the database.

  Troubleshooting

  KeyError: GEMINI_API_KEY
  export GEMINI_API_KEY="your-key-here"

  OperationalError on database connection
  Check your DATABASE_URL format:
  postgresql://username:password@host:5432/dbname

  429 RESOURCE_EXHAUSTED
  Your API key's project doesn't have free tier access. Create a new key at
  aistudio.google.com using "Create API key in new project".

  SQL keeps failing after 3 attempts
  Try rephrasing your question to be more specific, or check that your
  database has the tables you're asking about.
