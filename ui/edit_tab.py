from database import (
    delete_record,
    update_record
)
import streamlit as st
from datetime import date
from time_utils import convert_to_minutes
from subjects import find_existing_subject

def create_record_options(records):
    options = []

    for record in records:
        options.append(
            (
                record["id"],
                f"{record['date']} : {record['subject']} : {record['minutes']}"
            )
        )

    return options

def update_edit_fields(records, settings):
    selected = st.session_state["edit_record"]
    selected_id = selected[0]

    for record in records:
        if record["id"] == selected_id:
            edit_record = record
            break

    st.session_state["edit_date"] = date.fromisoformat(
        edit_record["date"]
    )
    st.session_state["edit_subject"] = edit_record["subject"]
    time_input_unit = settings["time_input_unit"]
    if time_input_unit == "hours":
        st.session_state["edit_study_time"] = edit_record["minutes"] / 60
    else:
        st.session_state["edit_study_time"] = edit_record["minutes"]

def render_edit_tab(records, settings):
    delete_options = create_record_options(records)

    if records:
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

            st.success("記録を削除しました")
            for key in (
                "edit_record",
                "edit_date",
                "edit_subject",
                "edit_study_time"
            ):
                st.session_state.pop(key,None)
            return True
    else:
        st.write("削除できる記録がありません")

    edit_options = create_record_options(records)

    if records:
        edit_selected = st.selectbox(
            "編集する記録を選んでください",
            edit_options,
            format_func=lambda option: option[1],
            key="edit_record",
            on_change=update_edit_fields,
            args=(records, settings)
        )
        edit_id = edit_selected[0]
        for record in records:
            if record["id"] == edit_id:
                edit_record = record
                break
        

        time_input_unit = settings["time_input_unit"]

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
                min_value=settings["time_step"] / 60,
                step=settings["time_step"] / 60,
                key="edit_study_time"
            )
        else:
            edit_study_time = st.number_input(
                "編集後の勉強時間（分）",
                min_value=settings["time_step"],
                step=settings["time_step"],
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
                        records
                    ),
                    edit_minutes
                )
                st.success("記録を編集しました")

                return True
    return False