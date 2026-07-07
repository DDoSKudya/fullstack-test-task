from src.services.files import resolve_title


def test_resolve_title_uses_value_when_provided() -> None:
    assert resolve_title("  My doc  ") == "My doc"


def test_resolve_title_generates_token_when_empty() -> None:
    title = resolve_title("")
    assert len(title) == 8
    assert all(ch in "0123456789abcdef" for ch in title)


def test_resolve_title_generates_token_for_whitespace() -> None:
    title = resolve_title("   ")
    assert len(title) == 8


def test_resolve_title_tokens_are_unique() -> None:
    titles = {resolve_title("") for _ in range(20)}
    assert len(titles) > 1
