from typing import Any

import hashlib
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    password: str

    def __init__(__pydantic_self__, **data: Any) -> None:
        hasher = hashlib.sha256()
        hasher.update(bytes(data["password"], "utf-8"))
        data["password"] = hasher.hexdigest()
        super().__init__(**data)

    def compare_passwords(self, password: str) -> bool:
        hasher = hashlib.sha256()
        hasher.update(bytes(password, "utf-8"))
        return self.password == hasher.hexdigest()
