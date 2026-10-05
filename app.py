import streamlit as st
from datetime import date
import pandas as pd
import altair as alt
from analytics import (
    filtered_records_by_period,
    calculate_subject_totals,
    calculate_total_minutes,
    format_minutes,calculate_daily_average,
    calculate_top_subject,
    calculate_study_streak,
    calculate_daily_totals,
    fill_missing_dates,
    filtered_previous_records_by_period,
    format_difference_minutes,
    create_heatmap_data,
    create_analysis_summary
)
from database import (
    initialize_database,
    add_record,
    get_records,
    update_record,
    delete_record,
    get_settings,
    save_setting
)
from subjects import (
    get_subject_options,
    find_existing_subject
)

initialize_database()

def update_edit_fields():
    selected = st.session_state["edit_record"]
    selected_id = selected[0]

    for record in st.session_state["records"]:
        if record["id"] == selected_id:
            edit_record = record
            break

    st.session_state["edit_date"] = date.fromisoformat(
        edit_record["date"]
    )
    st.session_state["edit_subject"] = edit_record["subject"]
    time_input_unit = st.session_state["settings"]["time_input_unit"]
    if time_input_unit == "hours":
        st.session_state["edit_study_time"] = edit_record["minutes"] / 60
    else:
        st.session_state["edit_study_time"] = edit_record["minutes"]

def create_record_options():
    options = []

    for record in st.session_state["records"]:
        options.append(
            (
                record["id"],
                f"{record['date']} : {record['subject']} : {record['minutes']}"
            )
        )

    return options

def convert_to_minutes(value, unit):
    if unit == "hours":
        return int(round(value * 60))
    else:
        return int(value)

if "records" not in st.session_state:
    st.session_state["records"] = get_records()

if "settings" not in st.session_state:
    st.session_state["settings"] = get_settings()

st.session_state["settings"].setdefault(
"time_input_unit",
"minutes"
)



st.title("Study Architect")
st.write("学習を記録・分析するアプリ")

record_tab, view_tab, edit_tab, settings_tab = st.tabs(
    [
        "📝 記録",
        "📊 閲覧",
        "✏️ 編集・削除",
        "⚙️ 設定"
    ]
)



with record_tab:
    study_date = st.date_input("勉強した日")

    subject_options = get_subject_options(st.session_state["records"])
    subject_choices = ["新しい科目"] + subject_options
    selected_subject = st.selectbox(
        "科目を選択",
        subject_choices
    )

    if selected_subject == "新しい科目":
        subject = st.text_input(
            "科目名を入力"
        )
    else:
        subject = selected_subject

    time_input_unit = st.session_state["settings"]["time_input_unit"]
    if time_input_unit == "hours":
        study_time = st.number_input(
            "勉強時間（時）",
            min_value=st.session_state["settings"]["time_step"] / 60,
            step=st.session_state["settings"]["time_step"] / 60
        )
        minutes = convert_to_minutes(study_time, time_input_unit)
    else:
        study_time = st.number_input(
            "勉強時間（分）",
            min_value=st.session_state["settings"]["time_step"],
            step=st.session_state["settings"]["time_step"]
        )
        minutes = convert_to_minutes(study_time, time_input_unit)

    if st.button("記録する"):
        if not subject.strip():
            st.warning("科目名を入力してください")
        else:
            add_record(
                study_date.isoformat(),
                find_existing_subject(
                    subject.strip(),
                    st.session_state["records"]
                ),
                minutes
            )
            st.session_state["reocrds"] = get_records()
            st.success("記録が完了しました")



with view_tab:

    period_options = [
        "1週間",
        "1か月",
        "1年",
        "全期間"
    ]

    selected_period = st.selectbox(
        "表示期間",
        period_options
    )

    overview_tab, detail_tab, goal_tab = st.tabs(
        ["概要", "詳細分析", "目標"]
    )

    with overview_tab:

        filtered_records = filtered_records_by_period(
            st.session_state["records"],
            selected_period
            )

        total_minutes = calculate_total_minutes(filtered_records)
        formatted_total = format_minutes(total_minutes)
        average_minutes = calculate_daily_average(filtered_records,selected_period)
        formatted_average = format_minutes(average_minutes)
        daily_totals = calculate_daily_totals(filtered_records)
        completed_totals = fill_missing_dates(daily_totals, selected_period)
        previous_records = filtered_previous_records_by_period(st.session_state["records"],selected_period)
        previous_total_minutes = calculate_total_minutes(previous_records)
        difference_minutes = total_minutes - previous_total_minutes
        formatted_difference = format_difference_minutes(difference_minutes)
        previous_average_minutes = calculate_daily_average(previous_records, selected_period)
        average_difference = average_minutes - previous_average_minutes
        formatted_average_difference = format_difference_minutes(average_difference)
        heatmap_data = create_heatmap_data(st.session_state["records"])
        heatmap_df = pd.DataFrame(heatmap_data)
        weekday_labels = {0: "月",1: "火",2: "水",3: "木",4: "金",5: "土",6: "日"}
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
                f"{calculate_study_streak(st.session_state["records"])}日"
            )

        subject_totals = calculate_subject_totals(filtered_records)

        st.bar_chart(subject_totals)
        st.line_chart(completed_totals)

        heatmap_chart = alt.Chart(heatmap_df).mark_rect(
            stroke="white",
            strokeWidth=1
        ).encode(
            x=alt.X(
                "week:O",
                axis=alt.Axis(
                    labels=False,
                    ticks=False,
                    title=None
                )
                ),
            y=alt.Y("weekday_name:O",
                    sort=["月", "火", "水", "木", "金", "土", "日"],
                    title=None
                    ),
            color=alt.Color(
                "level:O",
                scale=alt.Scale(
                    domain=[0, 1, 2, 3, 4],
                    range=[
                    "#EBEDF0",
                    "#9BE9A8",
                    "#40C463",
                    "#30A14E",
                    "#216E39"
                    ]
                ),
                legend=alt.Legend(
                    title="勉強レベル"
                )
                ),
            tooltip=[
                alt.Tooltip("date:N", title="日付"),
                alt.Tooltip("minutes:Q", title="勉強時間（分）")
            ]
        ).properties(
            height=120
        )

        month_chart = alt.Chart(month_df).mark_text(
            align="left"
        ).encode(
            x=alt.X("week:O", axis=None),
            text=alt.Text("month:N")
        ).properties(
            height=20
        )

        final_chart = alt.vconcat(
            month_chart,
            heatmap_chart
        ).resolve_scale(
            x="shared"
        )

        st.altair_chart(
            final_chart,
            use_container_width=True
        )

        with st.expander("記録一覧"):
            for record in filtered_records:
                st.write(f"{record["date"]}:{record["subject"]}を{record["minutes"]}分勉強しました")


    with detail_tab:

        analysis_summary = create_analysis_summary(
            st.session_state["records"],
            today=date.today()
        )
        daily_statistics = analysis_summary["daily_statistics"]
        weekday_average = analysis_summary["weekday_average"]
        weekday_average_display = {
            weekday_labels[weekday]: average
            for weekday, average in weekday_average.items()
        }
        weekday_average_df = pd.DataFrame(
            list(weekday_average_display.items()),
            columns=["weekday", "average"]
        )
        recent_trend = analysis_summary["recent_trend"]
        trend_labels = {"increase": "増加", "decrease": "減少", "stable": "横ばい"}
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
        subject_stats = analysis_summary["subject_stats"]


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
            weekday_Chart = (
                alt.Chart(weekday_average_df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "weekday:N",
                        sort=["月", "火", "水", "木", "金", "土", "日"],
                        axis=alt.Axis(labelAngle=0)
                    ),
                    y=alt.Y(
                        "average:Q"
                    )
                )
            )
            st.altair_chart(
                weekday_Chart,
                use_container_width=True
            )

        trend_col1, trend_col2 = st.columns(2)

        with trend_col1:
            st.metric(
                "直近7日間の勉強時間",
                f"{recent_trend["recent_total"]}分",
                delta=difference_display
            )

        with trend_col2:
            st.metric(
                "学習トレンド",
                trend_display,
                delta=change_rate_display
            )

        if subject_stats:
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
            st.dataframe(df_subject_stats)

    with goal_tab:
        pass



with edit_tab:
    delete_options = create_record_options()

    if st.session_state["records"]:
        selected = st.selectbox(
            "削除する記録を選んでください",
            delete_options,
            format_func=lambda option: option[1]
        )

        if st.button("削除する"):
            delete_id = selected[0]

            delete_record(
                delete_id
            )

            st.session_state["records"] = get_records()
            st.success("記録を削除しました")
    else:
        st.write("削除できる記録がありません")

    edit_options = create_record_options()

    if st.session_state["records"]:
        edit_selected = st.selectbox(
            "編集する記録を選んでください",
            edit_options,
            format_func=lambda option: option[1],
            key="edit_record",
            on_change=update_edit_fields
        )
        edit_id = edit_selected[0]
        for record in st.session_state["records"]:
            if record["id"] == edit_id:
                edit_record = record
                break

        time_input_unit = st.session_state["settings"]["time_input_unit"]

        if st.session_state.pop("reset_edit_study_time", False):
            st.session_state.pop("edit_study_time", None)

        if "edit_date" not in st.session_state:
            st.session_state["edit_date"] = date.fromisoformat(edit_record["date"])

        if "edit_subject" not in st.session_state:
            st.session_state["edit_subject"] = edit_record["subject"]

        if "edit_study_time" not in st.session_state:
            if time_input_unit == "hours":
                st.session_state["edit_study_time"] = edit_record["minutes"] / 60
            else:
                st.session_state["edit_study_time"] = edit_record["minutes"]

        edit_study_date = st.date_input(
            "編集後の日付",
            key="edit_date"
        )

        edit_subject = st.text_input(
            "編集後の科目名",
            key="edit_subject"
        )

        if time_input_unit == "hours":
            edit_study_time = st.number_input(
                "編集後の勉強時間（時）",
                min_value=st.session_state["settings"]["time_step"] / 60,
                step=st.session_state["settings"]["time_step"] / 60,
                key="edit_study_time"
            )
        else:
            edit_study_time = st.number_input(
                "編集後の勉強時間（分）",
                min_value=st.session_state["settings"]["time_step"],
                step=st.session_state["settings"]["time_step"],
                key="edit_study_time"
            )

        edit_minutes = convert_to_minutes(edit_study_time, time_input_unit)
        if st.button("更新する"):
            if not edit_subject.strip():
                st.warning("科目名を入力してください")
            else:
                update_record(
                    edit_id,
                    edit_study_date.isoformat(),
                    find_existing_subject(
                        edit_subject.strip(),
                        st.session_state["records"]
                    ),
                    edit_minutes
                )
                st.session_state["records"] = get_records()
                st.success("記録を編集しました")




with settings_tab:
    time_step_options = [1, 5, 10, 15, 30, 60]
    time_unit_options = ["minutes", "hours"]

    time_step = st.selectbox(
        "勉強時間の入力間隔",
        time_step_options,
        index=time_step_options.index(
            st.session_state["settings"]["time_step"]
            )
    )

    time_input_unit = st.selectbox(
        "勉強時間の入力単位",
        time_unit_options,
        index=time_unit_options.index(
            st.session_state["settings"]["time_input_unit"]
            ),
        format_func=lambda unit: "分" if unit == "minutes" else "時間"
    )

    if st.button("設定を保存"):
        old_unit = st.session_state["settings"]["time_input_unit"]

        st.session_state["settings"]["time_step"] = time_step
        st.session_state["settings"]["time_input_unit"] = time_input_unit

        if old_unit != time_input_unit:
                st.session_state["reset_edit_study_time"] = True

        save_setting(
            "time_step",
            st.session_state["settings"]["time_step"]
        )
        save_setting(
            "time_input_unit",
            st.session_state["settings"]["time_input_unit"]
        )
        st.rerun()