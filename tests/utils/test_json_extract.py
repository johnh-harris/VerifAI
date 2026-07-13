import pytest

from verifai.utils.json_extract import JsonExtractionError, extract_json_object


def test_extract_plain_json() -> None:
    assert extract_json_object('{"a": 1}') == {"a": 1}


def test_extract_fenced_json() -> None:
    assert extract_json_object('```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_with_surrounding_prose() -> None:
    text = 'Sure, here you go:\n{"a": 1}\nHope that helps!'
    assert extract_json_object(text) == {"a": 1}


def test_extract_raises_on_garbage() -> None:
    with pytest.raises(JsonExtractionError):
        extract_json_object("not json at all")
