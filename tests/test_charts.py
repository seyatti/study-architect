from ui.charts import (
    create_weekday_average_chart
)
import pandas as pd

def test_weekday_average_chart():
    df = pd.DataFrame(
        {
            "weekday": ["月", "火"],
            "average": [60, 120]
        }
    )

    chart = create_weekday_average_chart(df)
    spec = chart.to_dict()

    assert spec["mark"]["type"] == "bar"
    assert spec["encoding"]["y"]["field"] == "average"