import altair as alt

def create_weekday_average_chart(weekday_average_df):
    weekday_Chart = (
        alt.Chart(weekday_average_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "weekday:N",
                sort=["月", "火", "水", "木", "金", "土", "日"],
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y(
                "average:Q"
            )
        )
    )

    return weekday_Chart

def create_weekday_study_rate_chart(weekday_study_rate_df):
    weekday_study_rate_chart = (
        alt.Chart(weekday_study_rate_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "weekday:N",
                sort=["月", "火", "水", "木", "金", "土", "日"],
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y(
                "rate:Q",
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(title="学習率(%)")
            )
        )
    )

    return weekday_study_rate_chart

def create_weekly_study_days_chart(weekly_study_days_df):
    weekly_chart = (
        alt.Chart(weekly_study_days_df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "week_start:T"
            ),
            y=alt.Y(
                "study_days:Q",
                scale=alt.Scale(domain=[0, 7])
            )
        )
    )

    return weekly_chart

def create_heatmap_chart(heatmap_df, month_df):
    heatmap_chart = alt.Chart(heatmap_df).mark_rect(
        stroke="white",
        strokeWidth=1
    ).encode(
        x=alt.X(
            "week:O",
            axis=alt.Axis(
                labels=False,
                ticks=False,
                title=None
            )
            ),
        y=alt.Y("weekday_name:O",
                sort=["月", "火", "水", "木", "金", "土", "日"],
                title=None
                ),
        color=alt.Color(
            "level:O",
            scale=alt.Scale(
                domain=[0, 1, 2, 3, 4],
                range=[
                "#EBEDF0",
                "#9BE9A8",
                "#40C463",
                "#30A14E",
                "#216E39"
                ]
            ),
            legend=alt.Legend(
                title="勉強レベル"
            )
            ),
        tooltip=[
            alt.Tooltip("date:N", title="日付"),
            alt.Tooltip("minutes:Q", title="勉強時間（分）")
        ]
    ).properties(
        height=120
    )

    month_chart = alt.Chart(month_df).mark_text(
        align="left"
    ).encode(
        x=alt.X("week:O", axis=None),
        text=alt.Text("month:N")
    ).properties(
        height=20
    )

    final_chart = alt.vconcat(
        month_chart,
        heatmap_chart
    ).resolve_scale(
        x="shared"
    )

    return final_chart