import streamlit as st
from analytics import (
    calculate_total_minutes,
    format_minutes,
    calculate_daily_average,
    calculate_daily_totals,
    fill_missing_dates,
    filtered_previous_records_by_period,
    create_heatmap_data,
    format_difference_minutes,
    calculate_top_subject,
    calculate_subject_totals,
    calculate_study_streak,
    filtered_records_by_period
    )
from dashboard_data import (
    prepare_heatmap_data
)
from ui.charts import (
    create_heatmap_chart
)

def render_overview_tab(records, selected_period):
    filtered_records = filtered_records_by_period(
        records,
        selected_period
        )

    total_minutes = calculate_total_minutes(filtered_records)
    formatted_total = format_minutes(total_minutes)
    average_minutes = calculate_daily_average(filtered_records,selected_period)
    formatted_average = format_minutes(average_minutes)
    daily_totals = calculate_daily_totals(filtered_records)
    completed_totals = fill_missing_dates(daily_totals, selected_period)
    previous_records = filtered_previous_records_by_period(records,selected_period)
    previous_total_minutes = calculate_total_minutes(previous_records)
    difference_minutes = total_minutes - previous_total_minutes
    formatted_difference = format_difference_minutes(difference_minutes)
    previous_average_minutes = calculate_daily_average(previous_records, selected_period)
    average_difference = average_minutes - previous_average_minutes
    formatted_average_difference = format_difference_minutes(average_difference)
    heatmap_data = create_heatmap_data(records)
    
    heatmap_df, month_df = prepare_heatmap_data(heatmap_data)

    col1, col2 = st.columns(2)

    with col1:
        if selected_period == "全期間" or not previous_records:
            st.metric(
                "総勉強時間",
                formatted_total,
                delta="比較データなし"
            )
        else:
            st.metric(
                "総勉強時間",
                formatted_total,
                delta=formatted_difference
            )

    with col2:
        if selected_period == "全期間" or not previous_records:
            st.metric(
                "1日の平均勉強時間",
                formatted_average,
                delta="比較データなし"
            )
        else:
            st.metric(
                "1日の平均勉強時間",
                formatted_average,
                delta=formatted_average_difference
            )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "最も勉強した科目",
            calculate_top_subject(filtered_records)
        )

    with col4:
        st.metric(
            "連続勉強日数",
            f"{calculate_study_streak(records)}日"
        )

    subject_totals = calculate_subject_totals(filtered_records)

    st.bar_chart(subject_totals)
    st.line_chart(completed_totals)

    final_chart = create_heatmap_chart(
        heatmap_df,
        month_df
    )

    st.altair_chart(
        final_chart,
        use_container_width=True
    )

    with st.expander("記録一覧"):
        for record in filtered_records:
            st.write(f"{record["date"]}:{record["subject"]}を{record["minutes"]}分勉強しました")