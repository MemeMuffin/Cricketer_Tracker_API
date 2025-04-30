"""Models for administrator"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from models.superuser import Superuser


class Administrator(SQLModel, table=True):
    """Model for administrator"""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    username: str = Field(index=True)
    password: str = Field(index=True)
    is_superuser: bool | None = Field(index=True, default=False)

    # Relationship with superuser table
    superuser: Optional["Superuser"] = Relationship(back_populates="admin")
