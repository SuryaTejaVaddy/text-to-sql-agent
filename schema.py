from pydantic import BaseModel, field_validator

class SQLResponse(BaseModel):
    sql: str

    @field_validator("sql")
    @classmethod
    def must_be_select(cls, v: str) -> str:
        clean = v.strip().upper()
        if not clean.startswith("SELECT"):
            raise ValueError("Only SELECT statements are allowed")
        return v.strip()
