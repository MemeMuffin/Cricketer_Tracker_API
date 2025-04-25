"""Models for Teams"""

from sqlmodel import SQLModel, Field, Relationship
from models.cricketer import Cricketer


class Team(SQLModel, table=True):
    """Team SQLModel for SQLite table"""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    country: str = Field(index=True)

    cricketers: list["Cricketer"] = Relationship(back_populates="team")
