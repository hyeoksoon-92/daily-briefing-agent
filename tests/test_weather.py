# tests/test_weather.py
import pytest
import respx
import httpx
from tools.weather import get_weather


@respx.mock
def test_get_weather_returns_summary():
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=httpx.Response(200, json={
            "current": {
                "temperature_2m": 5.2,
                "weathercode": 3
            }
        })
    )
    result = get_weather()
    assert "5.2" in result
    assert "흐림" in result
    assert "°C" in result
    assert isinstance(result, str)
    assert respx.calls.call_count == 1


@respx.mock
def test_get_weather_unknown_code_uses_fallback():
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=httpx.Response(200, json={
            "current": {
                "temperature_2m": 10.0,
                "weathercode": 99
            }
        })
    )
    result = get_weather()
    assert "알 수 없음" in result
