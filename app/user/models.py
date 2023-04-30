from typing import Any

import hashlib
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web.postgres import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(64))

    # attachments: Mapped[list["Attachment"]] = relationship(
    #     back_populates="owner"
    # )

    def __init__(__pydantic_self__, **data: Any) -> None:
        hasher = hashlib.sha256()
        hasher.update(bytes(data["password"], "utf-8"))
        data["password"] = hasher.hexdigest()
        super().__init__(**data)

    def compare_passwords(self, password: str) -> bool:
        hasher = hashlib.sha256()
        hasher.update(bytes(password, "utf-8"))
        return self.password == hasher.hexdigest()  # type: ignore
