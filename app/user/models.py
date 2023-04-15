from typing import Any

import hashlib
from sqlalchemy import Column, Integer, String

from web.postgres import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    password = Column(String(64))

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
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }