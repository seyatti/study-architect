import pandas as pd
from analytics import (
    format_minutes,
    format_difference_minutes
)
from datetime import date

weekday_labels = {
    0: "月",
    1: "火",
    2: "水",
    3: "木",
    4: "金",
    5: "土",
    6: "日"
}
trend_labels = {"increase": "増加", "decrease": "減少", "stable": "横ばい"}

def prepare_weekday_data(data, value_colmun):
    weekday_data_display = {
        weekday_labels[weekday]: value
        for weekday, value in data.items()
    }
    weekday_data_df = pd.DataFrame(
        list(weekday_data_display.items()),
        columns=["weekday", value_colmun]
    )

    return weekday_data_df

def prepare_weekly_study_days_data(weekly_study_days):
    weekly_study_days_df = pd.DataFrame(
    list(weekly_study_days.items()),
    columns=["week_start", "study_days"]
    )
    if not weekly_study_days_df.empty:
        weekly_study_days_df["week_start"] = (
            weekly_study_days_df["week_start"]
            .dt.strftime("%Y-%m-%d")
        )

    return weekly_study_days_df

def prepare_subject_stats_data(subject_stats):
    df_subject_stats = pd.DataFrame.from_dict(subject_stats, orient="index").reset_index()
    df_subject_stats = df_subject_stats.rename(
        columns={
            "index": "科目",
            "total_minutes": "合計勉強時間",
            "study_days": "学習日数",
            "average_minutes": "1日平均",
            "last_studied_date": "最終学習日",
            "days_since_last_study": "最終学習からの日数"
        }
    )
    df_subject_stats = df_subject_stats.sort_values(
        by="合計勉強時間",
        ascending=False
    )
    df_subject_stats["合計勉強時間"] = (
        df_subject_stats["合計勉強時間"]
        .apply(format_minutes)
    )
    df_subject_stats["1日平均"] = (
        df_subject_stats["1日平均"]
        .apply(lambda minutes: format_minutes(round(minutes)))
    )

    return df_subject_stats

def prepare_subject_trend_data(subject_trend):
    df_subject_trend = pd.DataFrame.from_dict(subject_trend, orient="index").reset_index()
    df_subject_trend = df_subject_trend.rename(
        columns={
            "index": "科目",
            "recent_total": "直近7日",
            "previous_total": "前の7日",
            "difference": "差分",
            "change_rate": "変化率",
            "trend": "トレンド"
        }
    )
    df_subject_trend["トレンド"] = (
        df_subject_trend["トレンド"]
        .apply(lambda trend: trend_labels[trend])
    )
    df_subject_trend["直近7日"]= (
        df_subject_trend["直近7日"]
        .apply(lambda recent_total: format_minutes(round(recent_total)))
    )
    df_subject_trend["前の7日"] = (
        df_subject_trend["前の7日"]
        .apply(lambda previous_total: format_minutes(round(previous_total)))
    )
    df_subject_trend["差分"] = (
        df_subject_trend["差分"]
        .apply(lambda difference: format_difference_minutes(difference))
    )
    df_subject_trend["変化率"] = (
        df_subject_trend["変化率"]
        .apply(lambda rate:
                "比較不可" if pd.isna(rate)
                else f"+{rate}%" if rate > 0
                else f"{rate}%" if rate < 0
                else "±0%"
                )
    )

    return df_subject_trend

def prepare_recent_trend_data(recent_trend):
            
    trend_display = trend_labels[recent_trend["trend"]]
    difference = recent_trend["difference"]
    if difference > 0:
        difference_display = f"+{difference}分"
    elif difference < 0:
        difference_display = f"{difference}分"
    else:
        difference_display = "±0分"
    change_rate = recent_trend["change_rate"]
    if change_rate is None:
        change_rate_display = "比較不可"
    elif change_rate > 0:
        change_rate_display = f"+{change_rate}%"
    elif change_rate < 0:
        change_rate_display = f"{change_rate}%"
    elif change_rate == 0:
        change_rate_display = "±0%"

    recent_trend_data = {
        "trend_display": trend_display,
        "difference_display": difference_display,
        "change_rate_display": change_rate_display
    }

    return recent_trend_data

def prepare_heatmap_data(heatmap_data):
    heatmap_df = pd.DataFrame(heatmap_data)
    heatmap_df["weekday_name"] = heatmap_df["weekday"].map(weekday_labels)
    month_labels = []
    previous_month = None

    for item in heatmap_data:
        current_date = date.fromisoformat(item["date"])

        if current_date.month != previous_month:
            month_labels.append(
                {
                    "week": item["week"],
                    "month": f"{current_date.month}月"
                }
            )

            previous_month = current_date.month

    month_df = pd.DataFrame(month_labels)

    return heatmap_df, month_df