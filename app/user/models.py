from typing import Any

import hashlib
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from web.postgres import BaseModel


__all__ = [
    "User",
]


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(64))

    def __init__(__pydantic_self__, **data: Any) -> None:
        hasher = hashlib.sha256()
        hasher.update(bytes(data["password"], "utf-8"))
        data["password"] = hasher.hexdigest()
        super().__init__(**data)

    def compare_passwords(self, password: str) -> bool:
        hasher = hashlib.sha256()
        hasher.update(bytes(password, "utf-8"))
        return self.password == hasher.hexdigest()

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "password": self.password}
