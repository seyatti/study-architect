from datetime import date, timedelta
import pandas as pd

def calculate_subject_totals(records):
    totals = {}

    for record in records:
        if record["subject"] in totals:
            totals[record["subject"]] += record["minutes"]
        else:
            totals[record["subject"]] = record["minutes"]

    return totals

def calculate_daily_totals(records):
    totals = {}

    for record in records:
        if record["date"] in totals:
            totals[record["date"]] += record["minutes"]
        else:
            totals[record["date"]] = record["minutes"]

    return totals

def fill_missing_dates(daily_totals, period, today=None):
    completed_totals = {}

    if period == "1週間":
        if today is None:
            today = date.today()

        for i in range(7):
            current_date = today - timedelta(days=6 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "1か月":
        if today is None:
            today = date.today()

        for i in range(30):
            current_date = today - timedelta(days=29 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "1年":
        if today is None:
            today = date.today()

        for i in range(365):
            current_date = today - timedelta(days=364 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "全期間":
        if not daily_totals:
            return completed_totals
        if today is None:
            today = date.today()
        old_day = date.fromisoformat(min(daily_totals))
        difference_days = (today - old_day).days + 1

        for i in range(difference_days):
            current_date = today - timedelta(days=(difference_days - 1) - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)

    return completed_totals

def filtered_previous_records_by_period(records, period, today=None):
    filtered_records = []
    if today is None:
        today = date.today()

    for record in records:
        record_date = date.fromisoformat(record["date"])

        if period == "1週間":
            start_date = today - timedelta(days=13)
            end_date = today - timedelta(days=7)

            if start_date <= record_date <= end_date:
                filtered_records.append(record)
        elif period == "1か月":
            start_date = today - timedelta(days=59)
            end_date = today - timedelta(days=30)

            if start_date <= record_date <= end_date:
                filtered_records.append(record)
        elif period == "1年":
            start_date = today - timedelta(days=729)
            end_date = today - timedelta(days=365)

            if start_date <= record_date <= end_date:
                filtered_records.append(record)

    return filtered_records

def format_difference_minutes(difference_minutes):
    if difference_minutes > 0:
        sign = "+"
    elif difference_minutes < 0:
        sign = "-"
    else:
        sign = "±"

    formatted_difference = format_minutes(
        abs(difference_minutes)
    )

    return f"{sign}{formatted_difference}"

def calculate_total_minutes(records):
    total = 0
    for record in records:
        total += record["minutes"]

    return total

def format_minutes(total_minutes):

    result = ""

    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0 and minutes > 0:
        result = f"{hours}時間{minutes}分"
    elif hours > 0 and minutes == 0:
        result = f"{hours}時間"
    elif hours == 0:
        result = f"{minutes}分"

    return result

def calculate_daily_average(records, period, today=None):
    if not records:
        return 0

    if today is None:
        today = date.today()

    total_minutes = calculate_total_minutes(records)
    
    if period == "1週間":
        days = 7
    elif period == "1か月":
        days = 30
    elif period == "1年":
        days = 365
    else:
        dates = [
            date.fromisoformat(record["date"])
            for record in records
            ]
        first_date = min(dates)
        days = (today - first_date).days + 1

    return round(total_minutes / days)

def calculate_top_subject(records):
    if not records:
        return "記録なし"

    subject_totals = calculate_subject_totals(records)

    top_subject = max(subject_totals, key=subject_totals.get)

    return top_subject

def calculate_study_streak(records, today=None):
    study_dates = set()

    for record in records:
        study_dates.add(date.fromisoformat(record["date"]))

    streak = 0
    if today is None:
        current_date = date.today()
    else:
        current_date = today

    while current_date in study_dates:
        streak += 1
        current_date = current_date - timedelta(days=1)

    return streak

def filtered_records_by_period(records, period, today=None):
    if today is None:
        today = date.today()
    filtered_records = []

    for record in records:
        record_date = date.fromisoformat(record["date"])

        if period == "1週間":
            if record_date >= today - timedelta(days=6):
                filtered_records.append(record)
        elif period == "1か月":
            if record_date >= today - timedelta(days=29):
                filtered_records.append(record)
        elif period == "1年":
            if record_date >= today - timedelta(days=364):
                filtered_records.append(record)
        else:
            filtered_records.append(record)

    return filtered_records

def create_heatmap_data(records, today=None):
    daily_totals = calculate_daily_totals(records)

    heatmap_data = []
    if today is None:
        today = date.today()
    raw_start_date = today - timedelta(days=364)
    start_date = raw_start_date - timedelta(days=raw_start_date.weekday())
    total_days = (today - start_date).days + 1

    for i in range(total_days):
        current_date = start_date + timedelta(days=i)

        date_key = current_date.isoformat()
        minutes = daily_totals.get(date_key, 0)

        level = calculate_activity_level(minutes)

        weekday = current_date.weekday()
        week = i // 7

        heatmap_data.append(
            {
                "date": date_key,
                "minutes": minutes,
                "weekday": weekday,
                "week": week,
                "level": level
            }
        )

    return heatmap_data

def calculate_activity_level(minutes):
    if minutes == 0:
        return 0
    elif 1 <= minutes <= 30:
        return 1
    elif 31 <= minutes <= 60:
        return 2
    elif 61 <= minutes <= 120:
        return 3
    else:
        return 4

def create_records_dataframe(records):
    df = pd.DataFrame(records)

    if not df.empty:
        df["date"] = pd.to_datetime(
            df["date"]
        )

    return df

def calculate_weekday_average(records):
    df = create_records_dataframe(records)

    if df.empty:
        return {}

    daily = df.groupby(
        "date",
        as_index=False
    )["minutes"].sum()

    daily["weekday"] = daily["date"].dt.weekday

    result = daily.groupby("weekday")["minutes"].mean()

    result = result.reindex(
        range(7),
        fill_value=0
    )

    return result.to_dict()

def calculate_moving_average(records, window):
    df = create_records_dataframe(records)

    if df.empty:
        return pd.DataFrame()

    daily = df.groupby(
        "date",
        as_index=False
    )["minutes"].sum()

    date_range = pd.date_range(
        start=daily["date"].min(),
        end=daily["date"].max()
    )

    daily = daily.set_index("date")

    daily = daily.reindex(
        date_range,
        fill_value=0
    )

    daily = daily.reset_index()

    daily = daily.rename(
        columns={"index": "date"}
    )

    daily["moving_average"] = (
        daily["minutes"]
        .rolling(
            window=window,
            min_periods=1
        ).mean()
    )

    return daily

def calculate_recent_trend(records, days=7, today=None):
    if today is None:
        today = date.today()

    recent_end = today
    recent_start = today - timedelta(days= days - 1)

    previous_end = recent_start - timedelta(days=1)
    previous_start = previous_end - timedelta(days= days - 1)

    df = create_records_dataframe(records)

    if df.empty:
        return {
        "recent_total": 0,
        "previous_total": 0,
        "difference": 0,
        "change_rate": None,
        "trend": "stable"
    }

    recent_mask = (
        (df["date"].dt.date >= recent_start)
        & (df["date"].dt.date <= recent_end) 
    )

    recent_records = df[recent_mask]

    previous_mask = (
        (df["date"].dt.date >= previous_start)
        & (df["date"].dt.date <= previous_end)
    )

    previous_records = df[previous_mask]

    recent_total = recent_records["minutes"].sum()
    previous_total = previous_records["minutes"].sum()

    difference = recent_total - previous_total

    if difference > 0:
        trend = "increase"
    elif difference < 0:
        trend = "decrease"
    else:
        trend = "stable"

    if previous_total > 0:
        change_rate = round(difference / previous_total * 100, 1)
    else:
        change_rate = None

    return {
        "recent_total": recent_total,
        "previous_total": previous_total,
        "difference": difference,
        "change_rate": change_rate,
        "trend": trend
    }

def calculate_subject_stats(records, today=None):
    df = create_records_dataframe(records)

    if today is None:
        today = date.today()

    if df.empty:
        return {}

    subject_totals = df.groupby("subject")["minutes"].sum()
    study_days = df.groupby("subject")["date"].nunique()
    average_minutes = round(subject_totals / study_days, 1)
    last_studied_date = df.groupby("subject")["date"].max()
    today_timestamp = pd.Timestamp(today)
    days_since_last_study = (
        today_timestamp - last_studied_date
    ).dt.days
    last_studied_date = last_studied_date.dt.strftime("%Y-%m-%d")

    stats = pd.DataFrame(
        {
            "total_minutes": subject_totals,
            "study_days": study_days,
            "average_minutes": average_minutes,
            "last_studied_date": last_studied_date,
            "days_since_last_study": days_since_last_study
        }
    )

    return stats.to_dict(orient="index")

def calculate_subject_trends(records, days=7, today=None):
    df = create_records_dataframe(records)

    if df.empty:
        return {}

    subjects = df["subject"].unique()

    result = {}

    for subject in subjects:
        subject_df = df[df["subject"] == subject]

        subject_dict = subject_df.to_dict(orient="records")

        result[subject] = calculate_recent_trend(
            subject_dict,
            days=days,
            today=today
            )

    return result

def calculate_weekly_study_days(records):
    df = create_records_dataframe(records)

    if df.empty:
        return {}

    study_dates = df[["date"]].drop_duplicates()
    study_dates["weekday"] = study_dates["date"].dt.weekday

    study_dates["week_start"] = (
        study_dates["date"] - pd.to_timedelta(
            study_dates["weekday"],
            unit="D"
        )
    )

    weekly_count = study_dates.groupby("week_start").size()

    return weekly_count.to_dict()

def calculate_weekday_study_rate(records):
    df = create_records_dataframe(records)

    if df.empty:
        return {}

    all_dates = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max()
    )

    all_weekdays = all_dates.weekday
    weekday_total_count = (
        pd.Series(all_weekdays)
        .value_counts()
    )

    study_dates = df[["date"]].drop_duplicates()
    study_dates["weekday"] = study_dates["date"].dt.weekday

    weekday_study_counts = (
        study_dates["weekday"]
        .value_counts()
    )

    weekday_study_counts = weekday_study_counts.reindex(
        weekday_total_count.index,
        fill_value = 0
    )
    weekday_study_percent = weekday_study_counts / weekday_total_count * 100

    return weekday_study_percent.round(1).to_dict()

def calculate_daily_study_statistics(records):
    df = create_records_dataframe(records)

    if df.empty:
        return {}

    daily = df.groupby("date")["minutes"].sum()

    all_dates = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max()
    )

    daily = daily.reindex(
        all_dates,
        fill_value=0
    )

    daily_study_statistics = {
        "mean": daily.mean(),
        "median": daily.median(),
        "std": daily.std(ddof=0)
    }

    return daily_study_statistics

def calculate_goal_progress(
        records,
        target_minutes,
        start_date,
        end_date,
        today=None
):
    df = create_records_dataframe(records)

    if df.empty:
        actual_minutes = 0
    else:
        goal_mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
        goal_records = df[goal_mask]
        actual_minutes = goal_records["minutes"].sum()

    if today is None:
        today = date.today()

    if target_minutes > 0:
        achievement_rate = round(actual_minutes / target_minutes * 100, 1)
    else:
        achievement_rate = 0.0

    remaining_minutes = max(target_minutes - actual_minutes, 0)
    remaining_days = max((end_date - today).days + 1, 0)
    if remaining_days > 0:
        required_daily_minutes = round(remaining_minutes / remaining_days, 1)
    else:
        required_daily_minutes = 0.0

    result = {
        "actual_minutes": actual_minutes,
        "achievement_rate": achievement_rate,
        "remaining_minutes": remaining_minutes,
        "remaining_days": remaining_days,
        "required_daily_minutes": required_daily_minutes
    }

    return result

def create_analysis_summary(records, today=None):

    daily_statistics = calculate_daily_study_statistics(records)
    weekday_average = calculate_weekday_average(records)
    recent_trend = calculate_recent_trend(records, today=today)
    subject_stats = calculate_subject_stats(records, today=today)
    subject_trends = calculate_subject_trends(records, today=today)
    weekday_study_rate = calculate_weekday_study_rate(records)
    weekly_study_days = calculate_weekly_study_days(records)

    return {
        "daily_statistics": daily_statistics,
        "weekday_average": weekday_average,
        "recent_trend": recent_trend,
        "subject_stats": subject_stats,
        "subject_trends": subject_trends,
        "weekday_study_rate": weekday_study_rate,
        "weekly_study_days": weekly_study_days
    }