from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.models import User
from web.postgres import BaseModel


class Attachment(BaseModel):
    __tablename__ = "attachment"

    name: Mapped[str] = mapped_column(String(128), unique=True)
    url: Mapped[str] = mapped_column(String(256), unique=True)

    # owner: Mapped["User"] = relationship(back_populates="attachments")
