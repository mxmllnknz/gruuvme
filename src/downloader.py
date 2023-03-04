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
    'logger': MyLogger(),
    'format': 'm4a/bestaudio/best',
    'concurrent-fragments': '6',
    'hls-use-mpegts': 'true',
    'paths': {
      'home': './tracks'  
    },
    # We use this custom downloader because the native downloader is 6x slower and throttles for some reason
    'external_downloader': {
        'default': 'aria2c'
        },
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}


async def download_video(url):
    with ytdl.YoutubeDL(ydl_opts) as ytd:
        ytd.download([url])