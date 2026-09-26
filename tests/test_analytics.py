from analytics import (
    calculate_total_minutes,
    format_minutes,
    calculate_daily_average,
    calculate_top_subject,
    calculate_study_streak,
    filtered_records_by_period,
    filtered_previous_records_by_period,
    format_difference_minutes,
    calculate_subject_totals,
    calculate_daily_totals,
    fill_missing_dates,
    calculate_activity_level,
    create_heatmap_data
)

import pytest
from datetime import date

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
        "1週間",
        today=date(2026, 9, 24)
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
        "1か月",
        today=date(2026, 9, 24)
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
        "1年",
        today=date(2026, 9, 24)
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
        "全期間",
        today=date(2026, 9, 24)
    )

    assert result == 30

def test_calculate_daily_average_empty():
    records = []

    result = calculate_daily_average(
        records,
        "1週間",
        today=date(2026, 9, 24)
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

    result = calculate_study_streak(
        records,
        today=date(2026, 9, 24)
        )

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

    result = calculate_study_streak(
        records,
        today=date(2026, 9, 24)
        )

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

    result = calculate_study_streak(
        records,
        today=date(2026, 9, 24)
        )

    assert result == 0

def test_calculate_study_streak_empty():
    records = []

    result = calculate_study_streak(records)

    assert result == 0

def test_filtered_records_by_period_week():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-20",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-18",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-09-10",
            "subject": "Python",
            "minutes": 30
        }
    ]

    result = filtered_records_by_period(
        records,
        "1週間",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-20",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-18",
            "subject": "応用情報",
            "minutes": 90
        }
    ]

def test_filtered_records_by_period_month():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-08-26",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-08-25",
            "subject": "Python",
            "minutes": 30
        }
    ]

    result = filtered_records_by_period(
        records,
        "1か月",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-08-26",
            "subject": "応用情報",
            "minutes": 90
        }
    ]

def test_filtered_records_by_period_years():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-01-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-25",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2025-09-24",
            "subject": "Python",
            "minutes": 30
        }
    ]

    result = filtered_records_by_period(
        records,
        "1年",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-01-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-25",
            "subject": "応用情報",
            "minutes": 90
        }
    ]

def test_filtered_records_by_period_alldays():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-01-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-24",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2024-05-10",
            "subject": "数学",
            "minutes": 30
        }
    ]

    result = filtered_records_by_period(
        records,
        "全期間",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-01-01",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-24",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2024-05-10",
            "subject": "数学",
            "minutes": 30
        } 
    ]

def test_filtered_previous_records_by_period_week():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-18",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-09-17",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-09-11",
            "subject": "Python",
            "minutes": 30
        },
        {
            "date": "2026-09-10",
            "subject": "数学",
            "minutes": 120
        }
    ]

    result = filtered_previous_records_by_period(
        records,
        "1週間",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-09-17",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-09-11",
            "subject": "Python",
            "minutes": 30
        }
    ]

def test_filtered_previous_records_by_period_month():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-08-25",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-08-20",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-07-27",
            "subject": "Python",
            "minutes": 30
        },
        {
            "date": "2026-07-26",
            "subject": "数学",
            "minutes": 120
        }
    ]

    result = filtered_previous_records_by_period(
        records,
        "1か月",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2026-08-25",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2026-08-20",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2026-07-27",
            "subject": "Python",
            "minutes": 30
        }
    ]

def test_filtered_previous_records_by_period_years():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2025-09-24",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-23",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2024-09-26",
            "subject": "Python",
            "minutes": 30
        },
        {
            "date": "2024-09-25",
            "subject": "数学",
            "minutes": 120
        }
    ]

    result = filtered_previous_records_by_period(
        records,
        "1年",
        today=date(2026, 9, 24)
    )

    assert result == [
        {
            "date": "2025-09-24",
            "subject": "英語",
            "minutes": 45
        },
        {
            "date": "2025-09-23",
            "subject": "応用情報",
            "minutes": 90
        },
        {
            "date": "2024-09-26",
            "subject": "Python",
            "minutes": 30
        },
        {
            "date": "2024-09-25",
            "subject": "数学",
            "minutes": 120
        }
    ]

def test_format_difference_minutes_plus():
    difference_minutes = 150

    result = format_difference_minutes(difference_minutes)

    assert result == "+2時間30分"

def test_format_difference_minuts_minus():
    difference_minutes = -45

    result = format_difference_minutes(difference_minutes)

    assert result == "-45分"

def test_format_difference_minutes_zero():
    difference_minutes = 0

    result = format_difference_minutes(difference_minutes)

    assert result == "±0分"

def test_calculate_subject_totals():
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

    result = calculate_subject_totals(records)

    assert result == {
        "Python": 150,
        "英語": 45,
        "数学": 30
    }

def test_calculate_daily_totals():
    records = [
        {
            "date": "2026-09-01",
            "subject": "Python",
            "minutes": 60
        },
        {
            "date": "2026-09-01",
            "subject": "英語",
            "minutes": 30
        },
        {
            "date": "2026-09-02",
            "subject": "Python",
            "minutes": 45
        },
        {
            "date": "2026-09-03",
            "subject": "数学",
            "minutes": 90
        }
    ]

    result = calculate_daily_totals(records)

    assert result == {
        "2026-09-01": 90,
        "2026-09-02": 45,
        "2026-09-03": 90
    }

def test_fill_missing_dates_week():
    daily_totals = {
        "2026-09-10": 120,
        "2026-09-18": 60,
        "2026-09-20": 30,
        "2026-09-24": 90
    }

    result = fill_missing_dates(
        daily_totals,
        "1週間",
        today=date(2026, 9, 24)
    )

    assert result == {
        "2026-09-18": 60,
        "2026-09-19": 0,
        "2026-09-20": 30,
        "2026-09-21": 0,
        "2026-09-22": 0,
        "2026-09-23": 0,
        "2026-09-24": 90,
    }

def test_fill_missing_dates_month():
    daily_totals = {
        "2026-08-20": 120,
        "2026-08-26": 60,
        "2026-09-01": 30,
        "2026-09-15": 45,
        "2026-09-24": 90
    }

    result = fill_missing_dates(
        daily_totals,
        "1か月",
        today=date(2026, 9, 24)
    )

    assert result == {
        "2026-08-26": 60,
        "2026-08-27": 0,
        "2026-08-28": 0,
        "2026-08-29": 0,
        "2026-08-30": 0,
        "2026-08-31": 0,
        "2026-09-01": 30,
        "2026-09-02": 0,
        "2026-09-03": 0,
        "2026-09-04": 0,
        "2026-09-05": 0,
        "2026-09-06": 0,
        "2026-09-07": 0,
        "2026-09-08": 0,
        "2026-09-09": 0,
        "2026-09-10": 0,
        "2026-09-11": 0,
        "2026-09-12": 0,
        "2026-09-13": 0,
        "2026-09-14": 0,
        "2026-09-15": 45,
        "2026-09-16": 0,
        "2026-09-17": 0,
        "2026-09-18": 0,
        "2026-09-19": 0,
        "2026-09-20": 0,
        "2026-09-21": 0,
        "2026-09-22": 0,
        "2026-09-23": 0,
        "2026-09-24": 90
    }

def test_fill_missing_dates_years():
    daily_totals = {
        "2025-09-20": 120,
        "2025-09-25": 60,
        "2026-01-01": 90,
        "2026-06-15": 45,
        "2026-09-24": 180
    }

    result = fill_missing_dates(
        daily_totals,
        "1年",
        today=date(2026, 9, 24)
        )

    assert len(result) == 365
    assert list(result.keys())[0] == "2025-09-25"
    assert list(result.keys())[-1] == "2026-09-24"
    assert "2025-09-20" not in result
    assert result["2025-09-25"] == 60
    assert result["2026-01-01"] == 90
    assert result["2026-02-01"] == 0

def test_fill_missing_dates_alldays():
    daily_totals = {
        "2026-09-20": 120,
        "2026-09-22": 60,
        "2026-09-24": 90
    }

    result = fill_missing_dates(
        daily_totals,
        "全期間",
        today=date(2026, 9, 24)
    )

    assert len(result) == 5
    assert list(result.keys())[0] == "2026-09-20"
    assert list(result.keys())[-1] == "2026-09-24"
    assert result["2026-09-21"] == 0
    assert result["2026-09-24"] == 90

def test_fill_missing_dates_empty():
    daily_totals = {}

    result = fill_missing_dates(
        daily_totals,
        "全期間",
        today=date(2026, 9, 24)
    )

    assert result == {}

@pytest.mark.parametrize(
    "minutes, expected",
    [
        (0, 0),
        (1, 1),
        (30, 1),
        (31, 2),
        (60, 2),
        (61, 3),
        (120, 3),
        (121, 4),
    ]
)
def test_calculate_activity_level(minutes, expected):
    result = calculate_activity_level(minutes)

    assert result == expected

def test_create_heatmap_data():
    records = [
        {
            "date": "2026-09-24",
            "subject": "Python",
            "minutes": 90
        },
        {
            "date": "2026-09-23",
            "subject": "英語",
            "minutes": 30
        }
    ]

    result = create_heatmap_data(
                records,
                today=date(2026, 9, 24)
            )

    assert result[0]["date"] == "2025-09-22"
    assert result[-1]["date"] == "2026-09-24"
    assert len(result) == 368

    assert result[-2]["date"] == "2026-09-23"
    assert result[-2]["minutes"] == 30
    assert result[-2]["level"] == 1

    assert result[-1]["date"] == "2026-09-24"
    assert result[-1]["minutes"] == 90
    assert result[-1]["level"] == 3

    assert result[-2]["weekday"] == 2
    assert result[-2]["week"] == 52

    assert result[-1]["weekday"] == 3
    assert result[-1]["week"] == 52