# tools/weather.py
import httpx

WEATHER_CODES = {
    0: "맑음", 1: "대체로 맑음", 2: "부분적으로 흐림", 3: "흐림",
    45: "안개", 48: "착빙 안개",
    51: "가랑비", 53: "보통 가랑비", 55: "강한 가랑비",
    61: "약한 비", 63: "보통 비", 65: "강한 비",
    71: "약한 눈", 73: "보통 눈", 75: "강한 눈",
    80: "소나기", 81: "보통 소나기", 82: "강한 소나기",
    95: "뇌우",
}

def get_weather(latitude: float = 37.5665, longitude: float = 126.9780) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weathercode",
        "timezone": "Asia/Seoul",
    }
    response = httpx.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["current"]
    temp = data["temperature_2m"]
    code = data["weathercode"]
    condition = WEATHER_CODES.get(code, "알 수 없음")
    return f"현재 기온: {temp}°C, 날씨: {condition}"
