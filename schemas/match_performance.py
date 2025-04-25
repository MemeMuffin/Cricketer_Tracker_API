"""Match Performance Pydantic models"""

from datetime import date
from pydantic import BaseModel


class MatchPerformanceBase(BaseModel):
    """Basic Pydantic model for match_performance"""

    cricketer_id: int
    match_date: date
    runs: int
    wickets: int
    opponent_team: str
    match_type: str


class MatchPerformanceCreate(MatchPerformanceBase):
    """Pydantic model for creating new match_performance"""


class MatchPerformanceRead(MatchPerformanceBase):
    """Pydantic model for reading match_performance"""

    id: int

    class Config:
        """Allow creating model from ORM object"""

        from_attributes = True
