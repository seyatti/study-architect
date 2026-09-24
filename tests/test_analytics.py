from analytics import calculate_total_minutes, format_minutes, calculate_daily_average, calculate_top_subject, calculate_study_streak

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

def test_calculate_daily_average_week():
    records = [
        {
            "subject": "Python",
            "minutes": 70
        },
        {
            "subject": "English",
            "minutes": 35
        }
    ]

    result = calculate_daily_average(
        records,
        "1週間"
    )

    assert result == 15

def test_calculate_daily_average_month():
    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 120
        },
        {
            "date": "2026-09-05",
            "subject": "英語",
            "minutes": 90
        },
        {
            "date": "2026-09-10",
            "subject": "応用情報",
            "minutes": 60
        },
        {
            "date": "2026-09-15",
            "subject": "Python",
            "minutes": 30
        }
    ]

    result = calculate_daily_average(
        records,
        "1か月"
        )

    assert result == 10

def test_calculate_daily_average_years():
    records = [
        {
            "date": "2026-01-10",
            "subject": "Python",
            "minutes": 365
        },
        {
            "date": "2026-03-20",
            "subject": "英語",
            "minutes": 730
        },
        {
            "date": "2026-06-15",
            "subject": "応用情報",
            "minutes": 365
        }
    ]

    result = calculate_daily_average(
        records,
        "1年"
    )

    assert result == 4

def test_calculate_daily_average_alldays():
    records = [
        {
            "date": "2026-09-20",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-22",
            "subject": "英語",
            "minutes": 90
        }
    ]

    result = calculate_daily_average(
        records,
        "全期間"
    )

    assert result == 30

def test_calculate_daily_average_empty():
    records = []

    result = calculate_daily_average(
        records,
        "1週間"
    )

    assert result == 0

def test_calculate_top_subject():
    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 120
        },
        {
            "date": "2026-09-05",
            "subject": "英語",
            "minutes": 150
        },
        {
            "date": "2026-09-10",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-15",
            "subject": "応用情報",
            "minutes": 90
        }
    ]

    result = calculate_top_subject(records)

    assert result == "Python"

def test_calculate_top_subject_empty():
    records = []

    result = calculate_top_subject(records)

    assert result == "記録なし"

def test_calculate_study_streak():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-23",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-22",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-09-20",
            "subject": "Python",
            "minutes": 30
        }
    ]

    result = calculate_study_streak(records)

    assert result == 3

def test_calculate_study_streak_duplicate():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-24",
            "subject": "英語",
            "minutes": 30
        },
        {
            "date": "2026-09-23",
            "subject": "応用情報",
            "minutes": 45
        },
        {
            "date": "2026-09-22",
            "subject": "Python",
            "minutes": 90
        }
    ]

    result = calculate_study_streak(records)

    assert result == 3

def test_calculate_study_streak_today_empty():
    records = [
        {
            "date": "2026-09-23",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-22",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-21",
            "subject": "応用情報",
            "minutes": 90
        }
    ]

    result = calculate_study_streak(records)

    assert result == 0

def test_calculate_study_streak_empty():
    records = []

    result = calculate_study_streak(records)

    assert result == 0