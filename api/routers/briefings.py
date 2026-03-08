# api/routers/briefings.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_session
from api.services import briefing as briefing_service

router = APIRouter(prefix="/briefings", tags=["briefings"])


@router.get("/latest")
async def get_latest(session: AsyncSession = Depends(get_session)):
    briefing = await briefing_service.get_latest_briefing(session)
    if not briefing:
        return {"content": None, "date": None}
    return {"content": briefing.content, "date": str(briefing.date)}


@router.get("/")
async def list_briefings(session: AsyncSession = Depends(get_session)):
    briefings = await briefing_service.list_briefings(session)
    return [{"id": b.id, "date": str(b.date)} for b in briefings]


@router.post("/refresh")
async def refresh(session: AsyncSession = Depends(get_session)):
    briefing = await briefing_service.create_briefing(session)
    return {"content": briefing.content, "date": str(briefing.date)}
