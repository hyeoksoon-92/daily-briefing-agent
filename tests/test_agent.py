# tests/test_agent.py
from unittest.mock import patch, MagicMock
from agent import run_agent


def _make_text_response(text: str) -> MagicMock:
    block = MagicMock()
    block.type = "text"
    block.text = text
    msg = MagicMock()
    msg.stop_reason = "end_turn"
    msg.content = [block]
    return msg


def test_run_agent_returns_briefing():
    with patch("agent.get_weather", return_value="기온: 5°C, 맑음"), \
         patch("agent.get_github_trending", return_value="1. owner/repo - 100★"), \
         patch("agent.get_news", return_value="- AI news\n  https://example.com"), \
         patch("agent.anthropic.Anthropic") as mock_client:

        mock_client.return_value.messages.create.return_value = _make_text_response(
            "오늘의 브리핑입니다."
        )
        result = run_agent()

    assert isinstance(result, str)
    assert len(result) > 0
    assert result == "오늘의 브리핑입니다."


def test_run_agent_handles_tool_use_then_end():
    """Simulates Claude making tool calls before producing final text."""
    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.name = "get_weather"
    tool_block.id = "tool_123"
    tool_block.input = {}

    tool_call_msg = MagicMock()
    tool_call_msg.stop_reason = "tool_use"
    tool_call_msg.content = [tool_block]

    final_msg = _make_text_response("완성된 브리핑")

    with patch("agent.get_weather", return_value="기온: 5°C") as mock_weather, \
         patch("agent.get_github_trending", return_value="repo"), \
         patch("agent.get_news", return_value="news"), \
         patch("agent.anthropic.Anthropic") as mock_client:

        mock_client.return_value.messages.create.side_effect = [
            tool_call_msg,
            final_msg,
        ]
        result = run_agent()

    assert result == "완성된 브리핑"
    mock_weather.assert_called_once_with()
