# Text-to-SQL Agent

  Convert plain English questions into SQL queries using Gemini
  2.5 Flash, executed against a live PostgreSQL database with an
   automatic self-correction loop.

  ![Python](https://img.shields.io/badge/Python-3.12-blue)
  ![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
  ![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash
  -green)
  ![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-blue)

  ---

  ## Demo

  **Input:** `Show me the top 5 customers by total order value`

  **Generated SQL:**
  ```sql
  SELECT c.company_name, SUM(od.unit_price * od.quantity * (1 -
  od.discount)) AS total_order_value
  FROM customers AS c
  JOIN orders AS o ON c.customer_id = o.customer_id
  JOIN order_details AS od ON o.order_id = od.order_id
  GROUP BY c.company_name
  ORDER BY total_order_value DESC
  LIMIT 5;

  Output: A results table rendered in the browser.

  ---
  Features

  - Natural language to SQL conversion using Gemini 2.5 Flash
  - Self-correction loop — automatically retries up to 3 times
  if the SQL fails
  - Schema-aware — reads your live database structure before
  generating queries
  - Safety guardrail — only SELECT queries are allowed, no
  writes or deletes
  - Clean Gradio UI — runs in browser, accessible via Codespaces
   public URL

  ---
  Tech Stack

  ┌──────────────────────────────────┬───────────┬──────────┐
  │                Tool               │  Purpose  │  Cost    │
  ├──────────────────────────────────┼───────────┼──────────┤
  │                                  │ Cloud dev │ Free (60 │
  │ [https://github.com/features/code](https://github.com/features/code) │ elopment  │  hrs/mon │
  │ spaces                           │ environme │ th)      │
  │                                  │ nt        │          │
  ├──────────────────────────────────┼───────────┼──────────┤
  │                                  │ AI model  │          │
  │ [https://aistudio.google.com](https://aistudio.google.com)      │ that      │ Free     │
  │                                  │ generates │ tier     │
  │                                  │  SQL      │          │
  ├──────────────────────────────────┼───────────┼──────────┤
  │                                  │ Hosted Po │ Free     │
  │ [https://neon.tech](https://neon.tech)                │ stgreSQL  │ tier     │
  │                                  │ database  │          │
  ├──────────────────────────────────┼───────────┼──────────┤
  │ [https://gradio.app](https://gradio.app)               │ Web UI    │ Free     │
  ├──────────────────────────────────┼───────────┼──────────┤
  │ [https://github.com/pthom/northwi](https://github.com/pthom/northwi) │ Sample    │ Free     │
  │ nd_psql                          │ database  │          │
  └──────────────────────────────────┴───────────┴──────────┘

  ---
  Project Structure

  text-to-sql-agent/
  ├── app.py            # Gradio web UI
  ├── agent.py          # Gemini 2.5 Flash prompt + response
  parsing
  ├── schema.py          # Pydantic model — enforces SELECT-only
  queries
  ├── db.py              # PostgreSQL connection + schema
  introspection
  ├── self_correct.py   # Retry loop with error feedback to the
  model
  ├── requirements.txt  # Python dependencies
  └── .env.example      # API key template

  ---
  Setup Guide

  Prerequisites

  - A GitHub account
  - A Google account (for Gemini API)

  No local installs required — everything runs in GitHub
  Codespaces.

  ---
  Step 1 — Get Your API Keys

  Gemini API Key
  1. Go to [https://aistudio.google.com](https://aistudio.google.com)
  2. Click Get API Key → Create API key → Create API key in new
  project
  3. Copy and save the key securely

  Neon Database URL
  1. Go to [https://neon.tech](https://neon.tech) and sign up with GitHub
  2. Click New Project → name it → click Create
  3. Copy the connection string — it looks like:
  postgresql://user:password@host/dbname?sslmode=require

  ---
  Step 2 — Open in GitHub Codespaces

  1. Go to this repository on GitHub
  2. Click the green Code button → Codespaces tab → Create
  codespace on main
  3. Wait ~1 minute for the environment to load

  ---
  Step 3 — Add Secrets to Codespaces

  1. Go to your repo → Settings → Secrets and variables →
  Codespaces
  2. Add the following secrets:

  ┌────────────────────┬─────────────────────────────┐
  │    Secret Name     │            Value            │
  ├────────────────────┼─────────────────────────────┤
  │ GEMINI_API_KEY_sql │ Your Gemini API key         │
  ├────────────────────┼─────────────────────────────┤
  │ DATABASE_URL       │ Your Neon connection string │
  └────────────────────┴─────────────────────────────┘

  3. Restart your Codespace after adding secrets so they load
  automatically

  ---
  Step 4 — Load the Northwind Database

  Run this in the Codespaces terminal (replace with your actual
  connection string):

  python -c "
  import psycopg2, urllib.request
  url = '[https://raw.githubusercontent.com/pthom/northwind_psql/](https://raw.githubusercontent.com/pthom/northwind_psql/)
  master/northwind.sql'
  sql = urllib.request.urlopen(url).read().decode()
  conn = psycopg2.connect('YOUR_NEON_CONNECTION_STRING_HERE')
  conn.autocommit = True
  cur = conn.cursor()
  cur.execute(sql)
  conn.close()
  print('Done!')
  "

  Verify the data loaded:

  python -c "
  import psycopg2
  conn = psycopg2.connect('YOUR_NEON_CONNECTION_STRING_HERE')
  cur = conn.cursor()
  cur.execute('SELECT COUNT(*) FROM customers')
  print('Customers:', cur.fetchone()[0])
  cur.execute('SELECT COUNT(*) FROM orders')
  print('Orders:', cur.fetchone()[0])
  conn.close()
  "

  Expected output:
  Customers: 91
  Orders: 830

  ---
  Step 5 — Install Dependencies

  pip install -r requirements.txt

  ---
  Step 6 — Run the App

  python app.py

  When the popup appears for port 7860, click Open in Browser.

  ---
  Example Queries

  ┌───────────────────────────────────────┬─────────────────┐
  │                Question                │  What It Tests  │
  ├───────────────────────────────────────┼─────────────────┤
  │ Show me the top 5 customers by total  │ JOIN +          │
  │ order value                           │ aggregation     │
  ├───────────────────────────────────────┼─────────────────┤
  │ Which products have never been        │ LEFT JOIN / NOT │
  │ ordered?                              │  IN             │
  ├───────────────────────────────────────┼─────────────────┤
  │ List all employees and how many        │ GROUP BY        │
  │ orders they handled                   │                 │
  ├───────────────────────────────────────┼─────────────────┤
  │ What is the average freight cost per  │ AVG + GROUP BY  │
  │ country?                              │                 │
  ├───────────────────────────────────────┼─────────────────┤
  │ Show all orders placed in 1997        │ Date filtering  │
  └───────────────────────────────────────┴─────────────────┘

  ---
  How the Self-Correction Loop Works

  for attempt in range(1, 4):
      sql = generate_sql(question, schema, previous_error)
      try:
          results = execute(sql)
          return results         # success
      except Exception as e:
          previous_error = str(e)  # send error back to Gemini
  on next attempt

  If the generated SQL fails, the error message is sent back to
  Gemini as context so it can fix the query — up to 3 attempts
  before giving up.

  ---
  Security

  - API keys are stored as Codespaces secrets, never hardcoded
  in files
  - .env is listed in .gitignore and will never be committed
  - Only SELECT statements are permitted — write operations are
  blocked at the application level
  - If a key is ever leaked, revoke it immediately at
  [https://aistudio.google.com](https://aistudio.google.com) and generate a new one in a new
  project

  After pasting, scroll down and click **Commit changes** →
  **Commit changes** again to confirm.
