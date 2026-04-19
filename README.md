Text-to-SQL AgentConvert plain English questions into SQL queries using Gemini 2.0 Flash, executed against a live PostgreSQL database with an automatic self-correction loop.DemoInput: Show me the top 5 customers by total order valueGenerated SQL:SQLSELECT c.company_name, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_order_value
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
JOIN order_details AS od ON o.order_id = od.order_id
GROUP BY c.company_name
ORDER BY total_order_value DESC
LIMIT 5;
Output: A results table rendered in the browser.FeaturesNatural language to SQL conversion using Gemini 2.0 FlashSelf-correction loop — automatically retries up to 3 times if the SQL failsSchema-aware — reads your live database structure before generating queriesSafety guardrail — only SELECT queries are allowed, no writes or deletesClean Gradio UI — runs in browser, accessible via Codespaces public URLTech StackToolPurposeCostGitHub CodespacesCloud development environmentFree (60 hrs/month)Google AI StudioAI model that generates SQLFree tierNeonHosted PostgreSQL databaseFree tierGradioWeb UIFreeNorthwind DatasetSample databaseFreeProject StructurePlaintexttext-to-sql-agent/
├── app.py            # Gradio web UI
├── agent.py          # Gemini 2.0 Flash prompt + response parsing
├── schema.py         # Pydantic model — enforces SELECT-only queries
├── db.py             # PostgreSQL connection + schema introspection
├── self_correct.py   # Retry loop with error feedback to the model
├── requirements.txt  # Python dependencies
└── .env.example      # API key template
Setup GuidePrerequisitesA GitHub accountA Google account (for Gemini API)No local installs required — everything runs in GitHub Codespaces.Step 1 — Get Your API KeysGemini API KeyGo to https://aistudio.google.comClick Get API Key → Create API key → Create API key in new projectCopy and save the key securelyNeon Database URLGo to https://neon.tech and sign up with GitHubClick New Project → name it → click CreateCopy the connection string — it looks like:postgresql://user:password@host/dbname?sslmode=requireStep 2 — Open in GitHub CodespacesGo to this repository on GitHubClick the green Code button → Codespaces tab → Create codespace on mainWait ~1 minute for the environment to loadStep 3 — Add Secrets to CodespacesGo to your repo → Settings → Secrets and variables → CodespacesAdd the following secrets:Secret NameValueGEMINI_API_KEY_sqlYour Gemini API keyDATABASE_URLYour Neon connection stringRestart your Codespace after adding secrets so they load automaticallyStep 4 — Load the Northwind DatabaseRun this in the Codespaces terminal (replace with your actual connection string):Pythonpython -c "
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
Verify the data loaded:Pythonpython -c "
import psycopg2
conn = psycopg2.connect('YOUR_NEON_CONNECTION_STRING_HERE')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM customers')
print('Customers:', cur.fetchone()[0])
cur.execute('SELECT COUNT(*) FROM orders')
print('Orders:', cur.fetchone()[0])
conn.close()
"
Expected output: Customers: 91Orders: 830Step 5 — Install DependenciesBashpip install -r requirements.txt
Step 6 — Run the AppBashpython app.py
When the popup appears for port 7860, click Open in Browser.Example QueriesQuestionWhat It TestsShow me the top 5 customers by total order valueJOIN + aggregationWhich products have never been ordered?LEFT JOIN / NOT INList all employees and how many orders they handledGROUP BYWhat is the average freight cost per country?AVG + GROUP BYShow all orders placed in 1997Date filteringHow the Self-Correction Loop WorksPythonfor attempt in range(1, 4):
    sql = generate_sql(question, schema, previous_error)
    try:
        results = execute(sql)
        return results         # success
    except Exception as e:
        previous_error = str(e)  # send error back to Gemini on next attempt
If the generated SQL fails, the error message is sent back to Gemini as context so it can fix the query — up to 3 attempts before giving up.SecurityAPI keys are stored as Codespaces secrets, never hardcoded in files.env is listed in .gitignore and will never be committedOnly SELECT statements are permitted — write operations are blocked at the application levelIf a key is ever leaked, revoke it immediately at https://aistudio.google.com and generate a new one in a new project
