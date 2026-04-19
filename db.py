import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        url = os.environ["DATABASE_URL"]
        _engine = create_engine(url)
    return _engine

def execute_sql(sql: str) -> tuple[list[str], list[tuple]]:
    with get_engine().connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = [tuple(row) for row in result.fetchall()]
    return columns, rows

def get_schema_string() -> str:
    sql = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    columns, rows = execute_sql(sql)
    tables: dict[str, list[str]] = {}
    for _, (table, col, dtype) in enumerate(rows):
        tables.setdefault(table, []).append(f"  {col} ({dtype})")
    lines = []
    for table, cols in tables.items():
        lines.append(f"Table: {table}")
        lines.extend(cols)
        lines.append("")
    return "\n".join(lines)
