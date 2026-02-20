import pytest
from polybot.notifier.formatter import format_alert_msg, escape_md

def test_escape_md():
    assert escape_md("Hello. World!") == "Hello\\. World\\!"
    assert escape_md("YES-NO") == "YES\\-NO"

def test_format_alert_msg():
    market = {
        "question": "Will it rain?",
        "score": 80,
        "outcomePrices": ["0.5", "0.5"],
        "volume24hr": "1000",
        "volume": "5000"
    }
    msg = format_alert_msg(market)
    assert "80/100" in msg
    # The question mark should be escaped
    assert "Will it rain\\?" in msg
    assert "Vol 24h: $1,000" in msg
