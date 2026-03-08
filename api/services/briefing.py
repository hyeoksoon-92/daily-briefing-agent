# api/services/briefing.py
import asyncio
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agent import run_agent
from api.models.briefing import Briefing


async def get_latest_briefing(session: AsyncSession) -> Briefing | None:
    result = await session.execute(
        select(Briefing).order_by(Briefing.date.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def list_briefings(session: AsyncSession) -> list[Briefing]:
    result = await session.execute(
        select(Briefing).order_by(Briefing.date.desc())
    )
    return list(result.scalars().all())


async def create_briefing(session: AsyncSession) -> Briefing:
    content = await asyncio.to_thread(run_agent)
    today = date.today()

    existing = await session.execute(
        select(Briefing).where(Briefing.date == today)
    )
    briefing = existing.scalar_one_or_none()

    if briefing:
        briefing.content = content
    else:
        briefing = Briefing(date=today, content=content)
        session.add(briefing)

    await session.commit()
    await session.refresh(briefing)
    return briefing
