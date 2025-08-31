from yt_summary.utils.misc import convert_to_readable_time



def test_convert_to_readable_time_less_than_an_hour():
    assert convert_to_readable_time(45) == "00:45"


def test_convert_to_readable_time_more_than_an_hour():
    assert convert_to_readable_time(3665) == "01:01:05"
