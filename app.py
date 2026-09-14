import streamlit as st
import json
from datetime import date

st.title("Study Architect")
st.write("学習を記録・分析するアプリ")

if "records" not in st.session_state:
    try:
        with open("data/records.json", "r", encoding="utf=8") as f:
            st.session_state["records"] = json.load(f)

    except FileNotFoundError:
        st.session_state["records"] = []
delete_options = []
edit_options = []

def save_records():
    with open("data/records.json", "w", encoding="utf-8") as f:
       json.dump(
           st.session_state["records"],
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

study_date = st.date_input("勉強した日")

subject = st.text_input("科目名")

minutes = st.number_input(
    "勉強時間（分）",
    min_value=1,
    step=1
)

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
    

if st.button("記録の確認"):
    for record in st.session_state["records"]:
        st.write(f"{record["date"]}:{record["subject"]}を{record["minutes"]}分勉強しました")
    subject_totals = calculate_subject_totals()
    for key, value in subject_totals.items():
        st.write(f"{key}: {value}分")
    st.bar_chart(subject_totals)

for index, record in enumerate(st.session_state["records"]):
    delete_options.append(
        (
            index,
            f"{record['date']} : {record['subject']} : {record['minutes']}"
        )
    )

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

for index, record in enumerate(st.session_state["records"]):
    edit_options.append(
        (
            index,
            f"{record["date"]} : {record["subject"]} : {record["minutes"]}"
        )
    )

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
        step=1,
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