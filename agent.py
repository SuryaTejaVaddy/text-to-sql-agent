import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from schema import SQLResponse

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY_sql"])

_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.0,
    ),
)

def generate_sql(user_query: str, schema: str, error_context: str = "") -> SQLResponse:
    error_part = f"\nPrevious attempt failed with error: {error_context}\nFix the SQL." if error_context else ""
    prompt = f"""You are a SQL expert. Given this PostgreSQL database schema:

{schema}

Convert the following natural language question into a valid SQL SELECT query.
Return ONLY a JSON object in this exact format: {{"sql": "<your SQL query here>"}}
Do NOT include any explanation, markdown, or code fences — only the raw JSON.
{error_part}

Question: {user_query}"""

    response = _model.generate_content(prompt)
    raw = response.text.strip()
    data = json.loads(raw)
    return SQLResponse(**data)
