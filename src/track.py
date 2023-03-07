from youtube_search import YoutubeSearch
import requests
import json

class Track:
    def __init__(self, query, source='unspecified'):
        self.query = query
        self.source = source
        video_details = self.search()

        
        if self.source == 'youtube':
            self.url = query
        else:
            self.vid = video_details['id']
            self.url = f'https://www.youtube.com/watch?v={self.vid}'
            self.duration = video_details['duration']
            self.title = video_details['title']
            self.channel = video_details['channel']
    
    def search(self):
        if self.source == 'spotify':
            return YoutubeSearch(self.query, max_results=1).to_dict()[0]
        elif self.source == 'youtube':
            return self._parse_html(requests.get(self.query).text)

    def _parse_html(self, response):
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)
        
        self.title = data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]['videoPrimaryInfoRenderer']['title']['runs'][0]['text']
        self.vid = data["contents"]["twoColumnWatchNextResults"]['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultNavigationEndpoint']['modalEndpoint']['modal']['modalWithTitleAndButtonRenderer']['button']['buttonRenderer']['navigationEndpoint']['signInEndpoint']['nextEndpoint']['watchEndpoint']['videoId']

        