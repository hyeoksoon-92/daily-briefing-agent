# tests/test_output.py
from pathlib import Path
from unittest.mock import patch
from output import save_briefing, print_briefing


def test_save_briefing_creates_file(tmp_path):
    with patch("output.BRIEFINGS_DIR", tmp_path):
        filepath = save_briefing("오늘의 브리핑 내용")
    assert filepath.exists()
    assert "briefing-" in filepath.name
    assert filepath.suffix == ".md"
    assert "오늘의 브리핑 내용" in filepath.read_text(encoding="utf-8")


def test_save_briefing_filename_contains_date(tmp_path):
    from datetime import date
    today = date.today().isoformat()
    with patch("output.BRIEFINGS_DIR", tmp_path):
        filepath = save_briefing("test content")
    assert today in filepath.name


def test_print_briefing_does_not_raise():
    # Verifies it runs without error (rich output goes to console)
    print_briefing("# 테스트\n\n내용입니다.")
