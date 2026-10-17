import streamlit as st
from time_utils import convert_to_minutes
from subjects import (
    get_subject_options,
    find_existing_subject
    )

def render_record_tab(records, settings, save_disabled=False):
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

    if save_disabled:
        st.info("ブラウザへの保存完了を待っています")

    if st.button("記録する", disabled=save_disabled):
        if not subject.strip():
            st.warning("科目名を入力してください")
        else:
            return {
                "date": study_date.isoformat(),
                "subject": find_existing_subject(subject.strip(), records),
                "minutes": minutes,
            }

    return None