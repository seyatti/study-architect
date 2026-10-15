import streamlit as st
from datetime import date, timedelta
from database import (
    initialize_database,
    get_records,
    get_settings,
    save_setting,
    get_goal
)
from ui.overview_tab import render_overview_tab
from ui.detail_tab import render_detail_tab
from ui.goal_tab import render_goal_tab
from ui.record_tab import render_record_tab
from ui.edit_tab import render_edit_tab

initialize_database()

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
    saved = render_record_tab(
        st.session_state["records"],
        st.session_state["settings"]
    )

    if saved:
        st.session_state["records"] = get_records()

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

    changed = render_edit_tab(
        st.session_state["records"],
        st.session_state["settings"]
    )

    if changed:
        st.session_state["records"] = get_records()
        st.rerun()



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