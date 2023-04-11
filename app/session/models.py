from sqlmodel import SQLModel, Field


class Session(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user: int = Field(foreign_key="user.id")
