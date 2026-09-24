from analytics import calculate_total_minutes, format_minutes

def test_calculate_total_minutes():
    records = [
        {
            "date": "2026-08-01",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-16",
            "subject": "英語",
            "minutes": 30
        },
        {
            "date": "2026-09-03",
            "subject": "Python",
            "minutes": 45
        },
    ]

    result = calculate_total_minutes(records)

    assert result == 135

def test_calculate_total_minutes_empty():
    records = []

    result = calculate_total_minutes(records)

    assert result == 0

def test_format_minutes():
    result = format_minutes(135)

    assert result == "2時間15分"

def test_format_minutes_just_hours():
    result = format_minutes(120)

    assert result == "2時間"

def test_format_minutes_minutes():
    result = format_minutes(45)

    assert result == "45分"

def test_format_minutes_just_minutes():
    result = format_minutes(0)

    assert result == "0分"