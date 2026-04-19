# Text-to-SQL Agent

A natural language to SQL pipeline that lets you ask questions about your database in plain English using Google Gemini AI.

---

## How It Works

| Step | Description |
|------|-------------|
| **Ask** | Type a question in plain English in the Gradio web UI |
| **Generate** | Gemini 2.5 Flash converts your question into a SQL query using your live database schema |
| **Execute** | The SQL runs against a PostgreSQL database and returns real results |
| **Self-Correct** | If the SQL fails, the error is sent back to Gemini to fix it — up to 3 attempts automatically |

---

## Prerequisites

- Python 3.12+
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com) *(free tier)*
- A Neon PostgreSQL database from [neon.tech](https://neon.tech) *(free tier)*
- GitHub Codespaces *(recommended)* or a local Python environment

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SuryaTejaVaddy/text-to-sql-agent.git
cd text-to-sql-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Keys

**Option A — GitHub Codespaces (recommended)**

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Codespaces** → **New secret** and add:

| Name | Value |
|------|-------|
| `GEMINI_API_KEY_sql` | Your Gemini API key |
| `DATABASE_URL` | Your Neon connection string |

Then restart your Codespace. If the keys don't load automatically, run:

```bash
export GEMINI_API_KEY_sql="your-api-key-here"
export DATABASE_URL="your-neon-connection-string-here"
```

**Option B — Local `.env` file**

```bash
echo 'GEMINI_API_KEY_sql=your-api-key-here' > .env
echo 'DATABASE_URL=your-neon-connection-string-here' >> .env
```

---

## Running the App

### Step 1 — Load the Northwind Database

Run this **once** to populate your Neon database with sample data (replace with your connection string):

```bash
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
```

Expected output:
```
Done!
```

Verify the data loaded:

```bash
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
```

Expected output:
```
Customers: 91
Orders: 830
```

### Step 2 — Start the App

```bash
python app.py
```

Click **Open in Browser** when the popup appears on port `7860`.

### Step 3 — Ask a Question

Type any question about the data, for example:

```
Show me the top 5 customers by total order value
```

You will see the generated SQL and the results table:

```sql
SELECT c.company_name, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_order_value
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
JOIN order_details AS od ON o.order_id = od.order_id
GROUP BY c.company_name
ORDER BY total_order_value DESC
LIMIT 5;
```

```
(resolved in 1 attempt(s))
```

---

## Example Questions

| Question | What It Tests |
|----------|---------------|
| Show me the top 5 customers by total order value | JOIN + aggregation |
| Which products have never been ordered? | LEFT JOIN / NOT IN |
| List all employees and how many orders they handled | GROUP BY |
| What is the average freight cost per country? | AVG + GROUP BY |
| Show all orders placed in 1997 | Date filtering |

---

## Configuration

Edit `agent.py` to change defaults:

| Setting | Default | Description |
|---------|---------|-------------|
| `model_name` | `gemini-2.5-flash` | Gemini model used for SQL generation |
| `temperature` | `0.0` | Lower = more deterministic SQL output |
| `MAX_ATTEMPTS` | `3` | Max retries if SQL fails |

---

## Project Structure

```
text-to-sql-agent/
├── app.py            # Gradio web UI
├── agent.py          # Gemini 2.5 Flash prompt + response parsing
├── schema.py         # Pydantic model — enforces SELECT-only queries
├── db.py             # PostgreSQL connection + schema introspection
├── self_correct.py   # Retry loop with error feedback to the model
├── requirements.txt  # Python dependencies
└── .env.example      # API key template
```

---

## Troubleshooting

**`KeyError: GEMINI_API_KEY_sql`**
```bash
export GEMINI_API_KEY_sql="your-key-here"
```

**`429 RESOURCE_EXHAUSTED with limit: 0`**

Your API key's project doesn't have free tier access. Create a new key at [aistudio.google.com](https://aistudio.google.com) using **Create API key in new project**.

**`404 model not found`**

Run this to see available models for your key:
```bash
python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.environ['GEMINI_API_KEY_sql'])
[print(m.name) for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
"
```

**`relation does not exist`**

The Northwind data was not loaded. Re-run the **Step 1** loading command.
