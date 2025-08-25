import json
import yt_dlp

URL = "https://www.youtube.com/watch?v=qmfR2aXHLtg"
URL = "https://www.youtube.com/watch?v=AGglJehON5g"
URL = "https://www.youtube.com/watch?v=AGglJehON5g&t=100s"

ydl_opts = {"quiet": True, "skip_download": True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)


print("Title:", info["title"])
print("Uploader:", info["uploader"])
print("Description:", info["description"])
print("Duration (seconds):", info["duration"])  # seconds
print("Upload date:", info["upload_date"])  # yyyymmdd -> need to convert to datetime


{
    "en": [
        {
            "ext": "json3",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=json3",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "srv1",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=srv1",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "srv2",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=srv2",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "srv3",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=srv3",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "ttml",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=ttml",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "srt",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=srt",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
        {
            "ext": "vtt",
            "url": "https://www.youtube.com/api/timedtext?v=AGglJehON5g&ei=OpCoaK68EeCDp-oPhsmQyAY&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1755902634&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=3AEDFDABF2B8C5F9DD1FD43AEDE9476A1B359E3E.1AEA3580979F73B702D1F1966C4FB3B29FD2901E&key=yt8&lang=en&fmt=vtt",
            "name": "English",
            "impersonate": True,
            "__yt_dlp_client": "tv",
        },
    ]
}
