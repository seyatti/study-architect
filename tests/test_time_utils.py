from time_utils import convert_to_minutes

def test_convert_hours_to_minutes():
    assert convert_to_minutes(1.5, "hours") == 90