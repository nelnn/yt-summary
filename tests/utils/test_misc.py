import pytest

from yt_summary.utils.misc import convert_to_readable_time, parse_youtube_video_id


def test_convert_to_readable_time_less_than_an_hour():
    assert convert_to_readable_time(45) == "00:45"


def test_convert_to_readable_time_more_than_an_hour():
    assert convert_to_readable_time(3665) == "01:01:05"


@pytest.mark.parametrize("url", ["dQw4w9W", "https://www.youtube.com/watch?v=dQw4w9W", "https://youtu.be/dQw4w9W"])
def test_parse_youtube_video_id(url):
    assert parse_youtube_video_id(url) == "dQw4w9W"
