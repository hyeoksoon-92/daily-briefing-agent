import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date
from api.services.briefing import get_latest_briefing, list_briefings, create_briefing
from api.models.briefing import Briefing


@pytest.mark.asyncio
async def test_get_latest_returns_none_when_empty():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    result = await get_latest_briefing(mock_session)
    assert result is None


@pytest.mark.asyncio
async def test_get_latest_returns_briefing():
    mock_briefing = Briefing(id=1, date=date.today(), content="오늘의 브리핑")
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_briefing
    mock_session.execute.return_value = mock_result
    result = await get_latest_briefing(mock_session)
    assert result.content == "오늘의 브리핑"


@pytest.mark.asyncio
async def test_create_briefing_saves_to_db():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    with patch("api.services.briefing.run_agent", return_value="새 브리핑"):
        briefing = await create_briefing(mock_session)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert briefing.content == "새 브리핑"
