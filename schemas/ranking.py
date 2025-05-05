"""Ranking pydantic schemas"""

from pydantic import BaseModel


class RankingBase(BaseModel):
    """Base pydantic model for Ranking"""

    name: str
    total_runs: int
    total_wickets: int
    cricketer_id: int


class ReadRanking(RankingBase):
    """Pydantic model for reading ranking"""
