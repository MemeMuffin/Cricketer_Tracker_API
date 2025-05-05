"""Models for Cricketer"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

# from models import team as Team, match_performance

if TYPE_CHECKING:
    from models.team import Team
    from models.match_performance import MatchPerformance
    from models.ranking import Ranking


class Cricketer(SQLModel, table=True):
    """Crickter SQLModel for SQLite table"""

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    country: str = Field(index=True)
    role: str = Field(index=True)
    team_id: int = Field(foreign_key="team.id", index=True)

    team: Optional["Team"] = Relationship(back_populates="cricketers")
    performances: list["MatchPerformance"] = Relationship(back_populates="cricketers")
    ranking: Optional["Ranking"] = Relationship(back_populates="cricketer")
