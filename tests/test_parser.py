import pytest

from llm.parser import parse_intent


def test_valid_unread_trash_intent():
    intent = parse_intent(
        {
            "action": "trash",
            "gmail_query": "is:unread older_than:30d -is:starred",
            "reason": "Old unread messages except starred.",
        }
    )

    assert intent.action == "trash"
    assert "is:unread" in intent.gmail_query


def test_rejects_non_unread_cleanup():
    with pytest.raises(ValueError):
        parse_intent(
            {
                "action": "trash",
                "gmail_query": "older_than:30d",
                "reason": "Everything old.",
            }
        )


def test_help_is_safe():
    intent = parse_intent(
        {
            "action": "help",
            "gmail_query": "",
            "reason": "Unsupported request.",
        }
    )

    assert intent.action == "help"
