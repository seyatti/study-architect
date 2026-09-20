from datetime import date, timedelta

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

def fill_missing_dates(daily_totals, period):
    completed_totals = {}

    if period == "1週間":
        today = date.today()

        for i in range(7):
            current_date = today - timedelta(days=6 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "1か月":
        today = date.today()

        for i in range(30):
            current_date = today - timedelta(days=29 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "1年":
        today = date.today()

        for i in range(365):
            current_date = today - timedelta(days=364 - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)
    elif period == "全期間":
        if not daily_totals:
            return completed_totals
        today = date.today()
        old_day = date.fromisoformat(min(daily_totals))
        difference_days = (today - old_day).days + 1

        for i in range(difference_days):
            current_date = today - timedelta(days=(difference_days - 1) - i)
            date_key = current_date.isoformat()
            completed_totals[date_key] = daily_totals.get(date_key, 0)

    return completed_totals

def filtered_previous_records_by_period(records, period):
    filtered_records = []
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

def calculate_daily_average(records, period):
    if not records:
        return 0

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
        days = (date.today() - first_date).days + 1

    return round(total_minutes / days)

def calculate_top_subject(records):
    if not records:
        return "記録なし"

    subject_totals = calculate_subject_totals(records)

    top_subject = max(subject_totals, key=subject_totals.get)

    return top_subject

def calculate_study_streak(records):
    study_dates = set()

    for record in records:
        study_dates.add(date.fromisoformat(record["date"]))

    streak = 0
    current_date = date.today()

    while current_date in study_dates:
        streak += 1
        current_date = current_date - timedelta(days=1)

    return streak

def filtered_records_by_period(records, period):
    filtered_records = []
    today = date.today()

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

def create_heatmap_data(records):
    daily_totals = calculate_daily_totals(records)

    heatmap_data = []
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