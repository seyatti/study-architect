import pytest
from subjects import normalize_subject, get_subject_options, find_existing_subject

@pytest.mark.parametrize(
    "subject, expected",
    [
        ("Python", "python"),
        ("PYTHON", "python"),
        ("  Python  ", "python"),
        ("Ｐｙｔｈｏｎ", "python"),
        ("JavaScript", "javascript"),
    ]
)

def test_normalize_subject(subject, expected):

    result = normalize_subject(subject)

    assert result == expected

def test_get_subject_options():

    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-02",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-03",
            "subject": "Python",
            "minutes": 90
        },
        {
            "date": "2026-09-04",
            "subject": "数学",
            "minutes": 30
        }
    ]

    result = get_subject_options(records)

    assert result == ["Python", "数学", "英語"]

def test_find_existing_subject():
    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-02",
            "subject": "英語",
            "minutes": 45
        }
    ]

    result = find_existing_subject("ＰＹＴＨＯＮ", records)

    assert result == "Python"

def test_find_existing_subject_empty():
    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-02",
            "subject": "英語",
            "minutes": 45
        }
    ]

    result = find_existing_subject("数学", records)

    assert result == "数学"
