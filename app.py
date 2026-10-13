import streamlit as st
from datetime import date, timedelta
from database import (
    initialize_database,
    add_record,
    get_records,
    update_record,
    delete_record,
    get_settings,
    save_setting,
    get_goal
)
from subjects import (
    get_subject_options,
    find_existing_subject
)
from ui.overview_tab import render_overview_tab
from ui.detail_tab import render_detail_tab
from ui.goal_tab import render_goal_tab

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

saved_goal = get_goal()

if "options_goal" not in st.session_state:
    st.session_state["options_goal"] = {}

    if saved_goal is None:
        st.session_state["options_goal"]["study_time"] = 420
        st.session_state["options_goal"]["study_start_date"] = date.today()
        st.session_state["options_goal"]["study_end_date"] = date.today() + timedelta(days=6)
    else:
        st.session_state["options_goal"]["study_time"] = saved_goal["target_minutes"]
        st.session_state["options_goal"]["study_start_date"] = date.fromisoformat(saved_goal["start_date"])
        st.session_state["options_goal"]["study_end_date"] = date.fromisoformat(saved_goal["end_date"])

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
            st.session_state["records"] = get_records()
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

        render_overview_tab(
            st.session_state["records"],
            selected_period
        )


    with detail_tab:

        render_detail_tab(st.session_state["records"])

    with goal_tab:
        render_goal_tab(
            st.session_state["records"],
            saved_goal
        )


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