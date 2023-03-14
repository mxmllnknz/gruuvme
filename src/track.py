from youtube_search import YoutubeSearch
import requests
import json
import downloader

class Track:
    def __init__(self, query, source='unspecified'):
        self.query = query
        self.source = source
        self.path = ''
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
        
    async def download(self) -> None:
        await downloader.download_video(self.url)
        self.path = f'./tracks/{self.title} [{self.vid}].m4a'

    def _parse_html(self, response):
        '''
            This helper is specific to extracting important Track fields from a basic URL request to Youtube.com
            It's gross and I'm sure there must be a better way to get this info
        '''
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

        