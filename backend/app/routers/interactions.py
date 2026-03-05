"""Router for interaction endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.db.interactions import create_interaction, read_interactions
from app.models.interaction import InteractionLog, InteractionLogCreate, InteractionModel

router = APIRouter()


def _filter_by_item_id(
    interactions: list[InteractionLog], item_id: int | None
) -> list[InteractionLog]:
    if item_id is None:
        return interactions
    return [i for i in interactions if i.item_id == item_id]


@router.get("/", response_model=list[InteractionModel])
async def get_interactions(
    item_id: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    """Get all interactions, optionally filtered by item."""
    interactions = await read_interactions(session)
    interactions = _filter_by_item_id(interactions, item_id)

    return [
        {
            "id": log.id,
            "learner_id": log.learner_id,
            "item_id": log.item_id,
            "kind": log.kind,
            "created_at": log.created_at,
        }
        for log in interactions
    ]


@router.post("/", response_model=InteractionLog, status_code=201)
async def post_interaction(
    body: InteractionLogCreate, session: AsyncSession = Depends(get_session)
):
    """Create a new interaction log."""
    try:
        return await create_interaction(
            session,
            learner_id=body.learner_id,
            item_id=body.item_id,
            kind=body.kind,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="learner_id or item_id does not reference an existing record",
        )
