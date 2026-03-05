"""Pydantic models for interactions."""

from datetime import datetime

from sqlmodel import Field, SQLModel

# Ensure referenced FK target tables are registered in SQLModel metadata
# whenever InteractionLog is imported.
from app.models.item import ItemRecord  # noqa: F401
from app.models.learner import Learner  # noqa: F401


class InteractionLog(SQLModel, table=True):
    """An interaction log entry in the database."""

    __tablename__ = "interacts"

    id: int | None = Field(default=None, primary_key=True)
    learner_id: int = Field(foreign_key="learner.id")
    item_id: int = Field(foreign_key="item.id")
    kind: str
    created_at: datetime | None = Field(default=None)


class InteractionLogCreate(SQLModel):
    """Request schema for creating an interaction log."""

    learner_id: int
    item_id: int
    kind: str


class InteractionModel(SQLModel):
    id: int
    learner_id: int
    item_id: int
    kind: str
    created_at: datetime
