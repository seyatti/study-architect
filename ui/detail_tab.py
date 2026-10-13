import streamlit as st
from datetime import date

from analytics import create_analysis_summary

from dashboard_data import (
    prepare_weekday_data,
    prepare_weekly_study_days_data,
    prepare_subject_stats_data,
    prepare_subject_trend_data,
    prepare_recent_trend_data
)

from ui.charts import (
    create_weekday_average_chart,
    create_weekday_study_rate_chart,
    create_weekly_study_days_chart
)

def render_detail_tab(records):
    analysis_summary = create_analysis_summary(
        records,
        today=date.today()
    )
    daily_statistics = analysis_summary["daily_statistics"]
    weekday_average = analysis_summary["weekday_average"]
    weekday_average_df = prepare_weekday_data(
        weekday_average,
        "average"
    )
    recent_trend = analysis_summary["recent_trend"]
    trend_display = prepare_recent_trend_data(recent_trend)
    subject_stats = analysis_summary["subject_stats"]
    subject_trend = analysis_summary["subject_trends"]
    weekday_study_rate = analysis_summary["weekday_study_rate"]
    weekday_study_rate_df = prepare_weekday_data(
        weekday_study_rate,
        "rate"
        )
    weekly_study_days = analysis_summary["weekly_study_days"]
    weekly_study_days_df = prepare_weekly_study_days_data(weekly_study_days)

    if daily_statistics:
        cols1, cols2, cols3 = st.columns(3)

        with cols1:
            st.metric(
                "1日の平均勉強時間",
                f"{round(daily_statistics["mean"], 1)}分"
            )

        with cols2:
            st.metric(
                "1日の勉強時間の中央値",
                f"{daily_statistics["median"]}分"
            )

        with cols3:
            st.metric(
                "勉強時間の標準偏差",
                f"{round(daily_statistics["std"], 1)}分"
            )
    else:
        st.info("まだ分析できる学習記録がありません")

    if not weekday_average_df.empty:
        weekday_chart = create_weekday_average_chart(
            weekday_average_df
        )

        st.altair_chart(
            weekday_chart,
            use_container_width=True
        )

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.metric(
            "直近7日間の勉強時間",
            f"{recent_trend["recent_total"]}分",
            delta=trend_display["difference_display"]
        )

    with trend_col2:
        st.metric(
            "学習トレンド",
            trend_display["trend_display"],
            delta=trend_display["change_rate_display"]
        )
    if subject_stats:
        df_subject_stats = prepare_subject_stats_data(subject_stats)
        st.dataframe(df_subject_stats)

    if subject_trend:
        df_subject_trend = prepare_subject_trend_data(subject_trend)
        st.dataframe(df_subject_trend)

    if not weekday_study_rate_df.empty:
        weekday_study_rate_chart = create_weekday_study_rate_chart(
            weekday_study_rate_df
        )

        st.altair_chart(
            weekday_study_rate_chart,
            use_container_width=True
        )

    if not weekly_study_days_df.empty:
        weekly_chart = create_weekly_study_days_chart(
            weekly_study_days_df
        )
        st.altair_chart(
            weekly_chart,
            use_container_width=True
        )