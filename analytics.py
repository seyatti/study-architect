from datetime import date, timedelta

def calculate_subject_totals(records):
    totals = {}

    for record in records:
        if record["subject"] in totals:
            totals[record["subject"]] += record["minutes"]
        else:
            totals[record["subject"]] = record["minutes"]

    return totals

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