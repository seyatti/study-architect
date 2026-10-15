import streamlit as st
from database import save_setting

def render_settings_tab(settings):
    time_step_options = [1, 5, 10, 15, 30, 60]
    time_unit_options = ["minutes", "hours"]

    time_step = st.selectbox(
        "勉強時間の入力間隔",
        time_step_options,
        index=time_step_options.index(
            settings["time_step"]
            )
    )

    time_input_unit = st.selectbox(
        "勉強時間の入力単位",
        time_unit_options,
        index=time_unit_options.index(
            settings["time_input_unit"]
            ),
        format_func=lambda unit: "分" if unit == "minutes" else "時間"
    )

    if st.button("設定を保存"):
        save_setting("time_step", time_step)
        save_setting("time_input_unit", time_input_unit)

        return {
             "time_step": time_step,
             "time_input_unit": time_input_unit
        }

    return None