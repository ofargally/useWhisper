from __future__ import unicode_literals
import yt_dlp
import os
from dotenv import load_dotenv
load_dotenv()

link = os.getenv('YOUTUBE_LINK')

print("Youtube Link: ", link)
if link == "":
    print("Please add a link to the .env file")
    exit()
print("Downloading...")


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(
        [link])
