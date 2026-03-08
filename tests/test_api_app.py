import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_app_has_briefings_routes():
    from api_app import app
    routes = [r.path for r in app.routes]
    assert "/briefings/latest" in routes
    assert "/briefings" in routes or "/briefings/" in routes
    assert "/briefings/refresh" in routes


@pytest.mark.asyncio
async def test_app_cors_middleware_present():
    from api_app import app
    from starlette.middleware.cors import CORSMiddleware
    middleware_classes = [m.cls for m in app.user_middleware]
    assert CORSMiddleware in middleware_classes
