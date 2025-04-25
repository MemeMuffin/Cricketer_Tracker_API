"""Models for Match Performance"""

from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from models.cricketer import Cricketer


class MatchPerformance(SQLModel, table=True):
    """Match Performance SQLModel for SQLite table"""

    id: int | None = Field(default=None, primary_key=True, index=True)
    cricketer_id: int = Field(foreign_key="cricketer.id", index=True)
    match_date: date = Field(index=True)
    runs: int = Field(index=True)
    wickets: int = Field(index=True)
    opponent_team: str = Field(index=True)
    match_type: str = Field(index=True)

    cricketers: Optional["Cricketer"] = Relationship(back_populates="performances")
