import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from datetime import date
from fastapi import FastAPI
from api.routers.briefings import router
from api.database import get_session
from api.models.briefing import Briefing

test_app = FastAPI()
test_app.include_router(router)


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.mark.asyncio
async def test_get_latest_returns_content(mock_session):
    mock_briefing = Briefing(id=1, date=date.today(), content="테스트 브리핑")
    with patch("api.routers.briefings.briefing_service.get_latest_briefing",
               return_value=mock_briefing):
        test_app.dependency_overrides[get_session] = lambda: mock_session
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            response = await client.get("/briefings/latest")
    assert response.status_code == 200
    assert response.json()["content"] == "테스트 브리핑"
    test_app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_latest_returns_null_when_empty(mock_session):
    with patch("api.routers.briefings.briefing_service.get_latest_briefing",
               return_value=None):
        test_app.dependency_overrides[get_session] = lambda: mock_session
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            response = await client.get("/briefings/latest")
    assert response.status_code == 200
    assert response.json()["content"] is None
    test_app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_briefings_returns_array(mock_session):
    mock_list = [Briefing(id=1, date=date.today(), content="브리핑")]
    with patch("api.routers.briefings.briefing_service.list_briefings",
               return_value=mock_list):
        test_app.dependency_overrides[get_session] = lambda: mock_session
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test",
            follow_redirects=True
        ) as client:
            response = await client.get("/briefings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    test_app.dependency_overrides.clear()
