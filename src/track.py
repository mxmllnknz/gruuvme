from youtube_search import YoutubeSearch

class Track:
    def __init__(self, query, source='unspecified'):
        self.query = query
        video_details = self.search()
        self.source = source
        self.vid = video_details['id']
        self.url = f'https://www.youtube.com/watch?v={self.vid}'
        self.duration = video_details['duration']
        self.title = video_details['title']
        self.channel = video_details['channel']
    
    def search(self):
        return YoutubeSearch(self.query, max_results=1).to_dict()[0]