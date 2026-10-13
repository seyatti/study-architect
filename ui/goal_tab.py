import streamlit as st
import math
from database import save_goal
from analytics import (
    calculate_goal_progress,
    format_minutes
)
from datetime import date

def render_goal_tab(records, saved_goal):
    st.session_state["options_goal"]["study_time"] = st.number_input(
        "目標勉強時間（分）",
        value = st.session_state["options_goal"]["study_time"],
        min_value = 1,
        step=1
    )
    st.session_state["options_goal"]["study_start_date"] = st.date_input(
        "開始日",
        value = st.session_state["options_goal"]["study_start_date"]
        )
    st.session_state["options_goal"]["study_end_date"] = st.date_input(
        "終了日",
        value = st.session_state["options_goal"]["study_end_date"]
        )

    if st.session_state["options_goal"]["study_start_date"] > st.session_state["options_goal"]["study_end_date"]:
        st.error("開始日が終了日より大きいです")

    else:
        if st.button("目標に設定"):
            save_goal(
                st.session_state["options_goal"]["study_time"],
                st.session_state["options_goal"]["study_start_date"].isoformat(),
                st.session_state["options_goal"]["study_end_date"].isoformat(),
            )
            st.rerun()

    if saved_goal is None:
        st.info("目標がまだ設定されていません")
    else:
        goal_progress = calculate_goal_progress(
            records,
            saved_goal["target_minutes"],
            date.fromisoformat(saved_goal["start_date"]),
            date.fromisoformat(saved_goal["end_date"]),
            date.today()
        )

        goal_col1, goal_col2 = st.columns(2)

        with goal_col1:
            st.metric(
                "実際の勉強時間",
                format_minutes(goal_progress["actual_minutes"])
            )

        with goal_col2:
            st.progress(
                min(goal_progress["achievement_rate"] / 100, 1.0),
                text="目標達成率"
            )
            st.caption(f"{goal_progress["achievement_rate"]}%")

        goal_col3, goal_col4, goal_col5 = st.columns(3)

        with goal_col3:
            st.metric(
                "残りの勉強時間",
                format_minutes(goal_progress["remaining_minutes"])
            )

        with goal_col4:
            st.metric(
                "残りの日数",
                f"{goal_progress["remaining_days"]}日"
            )

        with goal_col5:
            st.metric(
                "1日に必要な勉強時間",
                format_minutes(math.ceil(goal_progress["required_daily_minutes"]))
            )