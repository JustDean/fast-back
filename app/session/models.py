from sqlalchemy import Column, String, ForeignKey

from web.postgres import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(String(64), primary_key=True)
    user = Column(ForeignKey("user.id"))
