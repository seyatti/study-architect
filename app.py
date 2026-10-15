import streamlit as st
from datetime import date, timedelta
from database import (
    initialize_database,
    get_records,
    get_settings,
    get_goal
)
from ui.overview_tab import render_overview_tab
from ui.detail_tab import render_detail_tab
from ui.goal_tab import render_goal_tab
from ui.record_tab import render_record_tab
from ui.edit_tab import render_edit_tab
from ui.settings_tab import render_settings_tab

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

    new_settings = render_settings_tab(
        st.session_state["settings"]
    )

    if new_settings is not None:
        old_unit = st.session_state["settings"]["time_input_unit"]

        if old_unit != new_settings["time_input_unit"]:
            st.session_state["reset_edit_study_time"] = True

        st.session_state["settings"].update(new_settings)

        st.rerun()