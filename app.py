import streamlit as st
import json
from datetime import date

def load_records():
    try:
        with open("data/records.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return []  

def load_settings():
    try:
        with open("data/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "time_step": 1,
            "time_input_unit": "minutes"
        }

def save_records():
    with open("data/records.json", "w", encoding="utf-8") as f:
       json.dump(
           st.session_state["records"],
           f,
           ensure_ascii=False,
           indent=2
       )

def save_settings():
    with open("data/settings.json", "w", encoding="utf-8") as f:
        json.dump(
            st.session_state["settings"],
            f,
            ensure_ascii=False,
            indent=2
        )

def update_edit_fields():
    selected = st.session_state["edit_record"]

    edit_number = selected[0]
    edit_record = st.session_state["records"][edit_number]

    st.session_state["edit_date"] = date.fromisoformat(
        edit_record["date"]
    )
    st.session_state["edit_subject"] = edit_record["subject"]
    st.session_state["edit_minutes"] = edit_record["minutes"]

def calculate_subject_totals():
    totals = {}

    for record in st.session_state["records"]:
        if record["subject"] in totals:
            totals[record["subject"]] += record["minutes"]
        else:
            totals[record["subject"]] = record["minutes"]

    return totals

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

    subject = st.text_input("科目名")

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
                    "subject":subject.strip(),
                    "minutes":minutes
                }
            )
            save_records()
            st.success("記録が完了しました")

with view_tab:
    if st.button("記録の確認"):
        for record in st.session_state["records"]:
            st.write(f"{record["date"]}:{record["subject"]}を{record["minutes"]}分勉強しました")
        subject_totals = calculate_subject_totals()
        for key, value in subject_totals.items():
            st.write(f"{key}: {value}分")
        st.bar_chart(subject_totals)

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
            save_records()
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

        edit_study_date = st.date_input(
            "編集後の日付",
            value=date.fromisoformat(edit_record["date"]),
            key="edit_date"
        )

        edit_subject = st.text_input(
            "編集後の科目名",
            value=edit_record["subject"],
            key="edit_subject"
        )

        edit_minutes = st.number_input(
            "編集後の勉強時間（分）",
            min_value=1,
            step=st.session_state["settings"]["time_step"],
            value=edit_record["minutes"],
            key="edit_minutes"
        )
        if st.button("更新する"):
            if not edit_subject.strip():
                st.warning("科目名を入力してください")
            else:
                st.session_state["records"][edit_number]["date"] = edit_study_date.isoformat()
                st.session_state["records"][edit_number]["subject"] = edit_subject.strip()
                st.session_state["records"][edit_number]["minutes"] = edit_minutes
                save_records()
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
        st.session_state["settings"]["time_step"] = time_step
        st.session_state["settings"]["time_input_unit"] = time_input_unit
        save_settings()
        st.success("設定を保存しました")