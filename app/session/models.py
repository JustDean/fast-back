from sqlalchemy import Column, String, ForeignKey

from web.postgres import Base


__all__ = [
    "Session",
]


class Session(Base):
    __tablename__ = "session"

    id = Column(String(64), primary_key=True)
    user = Column(ForeignKey("user.id"))
