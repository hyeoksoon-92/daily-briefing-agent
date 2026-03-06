# agent.py
import anthropic
from tools.weather import get_weather
from tools.github import get_github_trending
from tools.news import get_news

TOOLS = [
    {
        "name": "get_weather",
        "description": "현재 날씨와 기온을 가져옵니다.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_github_trending",
        "description": "GitHub에서 오늘 인기 있는 레포지토리 목록을 가져옵니다.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_news",
        "description": "기술 관련 최신 뉴스 헤드라인을 가져옵니다.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
]

# Map tool names to module-level names so patches applied to this module's
# namespace are picked up at call time (via globals()).
_TOOL_NAME_MAP = {
    "get_weather": "get_weather",
    "get_github_trending": "get_github_trending",
    "get_news": "get_news",
}

SYSTEM_PROMPT = """당신은 개인 브리핑 어시스턴트입니다.
도구를 사용해 날씨, GitHub 트렌딩, 뉴스를 수집하고,
한국어로 간결하고 읽기 쉬운 아침 브리핑을 작성하세요.
각 섹션에 이모지를 사용하고, 핵심 내용만 요약하세요."""


def _call_tool(name: str, inputs: dict):
    """Look up the tool function from the current module globals at call time.

    This ensures that unittest.mock patches applied to the module namespace
    (e.g. patch("agent.get_weather", ...)) are honoured correctly.
    """
    import agent as _self
    fn = getattr(_self, _TOOL_NAME_MAP.get(name, ""), None)
    if fn is None:
        return "Tool not found"
    return fn(**inputs)


def run_agent() -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": "오늘의 브리핑을 만들어주세요."}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        # Handle tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = _call_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
