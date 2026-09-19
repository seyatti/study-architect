import streamlit as st
from datetime import date
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
    format_difference_minutes
    )
from storage import load_records, load_settings, save_records, save_settings
from subjects import get_subject_options, find_existing_subject

def update_edit_fields():
    selected = st.session_state["edit_record"]

    edit_number = selected[0]
    edit_record = st.session_state["records"][edit_number]

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

    for index, record in enumerate(st.session_state["records"]):
        options.append(
            (
                index,
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
    st.session_state["records"] = load_records()

if "settings" not in st.session_state:
    st.session_state["settings"] = load_settings()

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
            st.session_state["records"].append(
                {   
                    "date":study_date.isoformat(),
                    "subject": find_existing_subject(subject.strip(), st.session_state["records"]),
                    "minutes":minutes
                }
            )
            save_records(st.session_state["records"])
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

    st.line_chart(completed_totals)

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

    with st.expander("記録一覧"):
        for record in filtered_records:
            st.write(f"{record["date"]}:{record["subject"]}を{record["minutes"]}分勉強しました")



with edit_tab:
    delete_options = create_record_options()

    if st.session_state["records"]:
        selected = st.selectbox(
            "削除する記録を選んでください",
            delete_options,
            format_func=lambda option: option[1]
        )

        if st.button("削除する"):
            delete_number = selected[0]

            st.session_state["records"].pop(
                delete_number
            )
            save_records(st.session_state["records"])
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
        edit_number = edit_selected[0]
        edit_record = st.session_state["records"][edit_number]

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
                st.session_state["records"][edit_number]["date"] = edit_study_date.isoformat()
                st.session_state["records"][edit_number]["subject"] = find_existing_subject(edit_subject.strip(), st.session_state["records"])
                st.session_state["records"][edit_number]["minutes"] = edit_minutes
                save_records(st.session_state["records"])
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

        save_settings(st.session_state["settings"])
        st.rerun()