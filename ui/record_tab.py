import streamlit as st
from time_utils import convert_to_minutes
from subjects import (
    get_subject_options,
    find_existing_subject
    )
from database import (
    add_record,
    get_records
    )

def render_record_tab(records, settings):
    study_date = st.date_input("勉強した日")

    subject_options = get_subject_options(records)
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

    time_input_unit = settings["time_input_unit"]
    if time_input_unit == "hours":
        study_time = st.number_input(
            "勉強時間（時）",
            min_value=settings["time_step"] / 60,
            step=settings["time_step"] / 60
        )
        minutes = convert_to_minutes(study_time, time_input_unit)
    else:
        study_time = st.number_input(
            "勉強時間（分）",
            min_value=settings["time_step"],
            step=settings["time_step"]
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
                    records
                ),
                minutes
            )
            st.success("記録が完了しました")

            return True

    return False