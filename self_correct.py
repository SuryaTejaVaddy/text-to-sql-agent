from agent import generate_sql
from db import execute_sql, get_schema_string

MAX_ATTEMPTS = 3

def run_with_correction(user_query: str) -> dict:
    schema = get_schema_string()
    error_context = ""
    result = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            result = generate_sql(user_query, schema, error_context)
            columns, rows = execute_sql(result.sql)
            return {
                "success": True,
                "sql": result.sql,
                "columns": columns,
                "rows": rows,
                "attempts": attempt,
            }
        except Exception as e:
            error_context = str(e)

    return {
        "success": False,
        "sql": result.sql if result else "",
        "error": error_context,
        "attempts": MAX_ATTEMPTS,
    }
