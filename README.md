Text-to-SQL Agent
A web app that lets you ask questions about a database in plain English and get back real data. It uses Gemini 2.0 Flash to convert your question into a SQL query, runs it against a PostgreSQL database, and shows you the results in a table.

Example:

You type: Show me the top 5 customers by total order value

It generates: The SQL, runs it, and shows you a results table.

What This Project Uses
Tool	Purpose	Cost
GitHub Codespaces	Cloud development environment	Free (60 hrs/month)
Gemini 2.0 Flash	AI model that generates SQL	Free tier
Neon	Hosted PostgreSQL database	Free tier
Gradio	Web UI	Free
Northwind Dataset	Sample database (customers, orders, products)	Free
How It Works
You type a question in plain English.

The app sends your question + the database schema to Gemini 2.0 Flash.

Gemini returns a SQL query.

The app runs the SQL on the PostgreSQL database.

Results are shown in a table below.

If the SQL fails, it automatically retries up to 3 times, sending the error back to Gemini to fix the syntax.

Project Structure
Plaintext
text-to-sql-agent/
├── app.py            # Gradio web UI
├── agent.py          # Gemini 2.0 Flash integration
├── schema.py         # Validates that only SELECT queries are allowed
├── db.py             # PostgreSQL database connection
├── self_correct.py   # Retry loop (tries up to 3 times if SQL fails)
├── requirements.txt  # Python dependencies
└── .env.example      # Template for your API keys
Step-by-Step Setup Guide
Step 1 — Get Your API Keys
Gemini API Key:

Go to aistudio.google.com.

Click Get API Key → Create API key → Create API key in new project.

Copy the key and save it somewhere safe.

Neon Database Connection String:

Go to neon.tech and sign up free with GitHub.

Click New Project → give it a name → click Create.

Copy the connection string (looks like postgresql://user:pass@host/dbname).

Step 2 — Open the Project in GitHub Codespaces
Go to your GitHub repo.

Click the green Code button → Codespaces tab → Create codespace on main.

Wait about 1 minute for the environment to build.

Step 3 — Add Your API Keys as Codespaces Secrets
Go to your repo → Settings → Secrets and variables → Codespaces.

Click New repository secret and add:

Name	Value
GEMINI_API_KEY_sql	Your Gemini API key
DATABASE_URL	Your Neon connection string
Note: After adding secrets, restart your Codespace so they load into your environment automatically.

Step 4 — Load the Northwind Database
In the Codespaces terminal, run this (replace the placeholder with your Neon connection string):

Python
python -c "
import psycopg2, urllib.request
url = 'https://raw.githubusercontent.com/pthom/northwind_psql/master/northwind.sql'
sql = urllib.request.urlopen(url).read().decode()
conn = psycopg2.connect('YOUR_NEON_CONNECTION_STRING_HERE')
conn.autocommit = True
cur = conn.cursor()
cur.execute(sql)
conn.close()
print('Done!')
"
Verify it worked:

Python
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
Expected output: Customers: 91, Orders: 830.

Step 5 — Install Dependencies & Run
Bash
pip install -r requirements.txt
python app.py
Click "Open in Browser" when the popup appears on port 7860.

Example Questions to Try
"Show me the top 5 customers by total order value."

"Which products have never been ordered?"

"List all employees and how many orders they handled."

"What is the average freight cost per country?"

"Show all orders placed in 1997."

Security Note: Never commit your actual API keys to GitHub. Use the repository secrets method described in Step 3 to keep your credentials safe.
