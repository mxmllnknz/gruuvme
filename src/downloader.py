import yt_dlp as ytdl
""" def search(query): 
    with ytdl.YoutubeDL([ydl_opts]) as ytd: """

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'concurrent-fragments': '4',
    'hls-use-mpegts': 'true',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}


async def download_video(url):
    url = 'https://www.youtube.com/watch?v=kTyP0-Zaz0I&ab_channel=WeAreScientists'
    with ytdl.YoutubeDL(ydl_opts) as ytd:
        ytd.download([url])