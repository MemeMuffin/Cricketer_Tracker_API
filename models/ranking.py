"""Models for ranking system"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.cricketer import Cricketer


class Ranking(SQLModel, table=True):
    """Model for Ranking table"""

    name: str = Field(index=True)
    total_runs: int = Field(index=True)
    total_wickets: int = Field(index=True)
    score: int = Field(index=True)
    rank_position: int | None = Field(index=True)
    cricketer_id: int = Field(foreign_key="cricketer.id", primary_key=True, index=True)

    cricketer: Optional["Cricketer"] = Relationship(back_populates="ranking")
