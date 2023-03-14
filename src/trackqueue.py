from track import Track
from pathlib import Path
from os import getcwd

class TrackQueue:
    def __init__(self):
        self.items = []
    
    def front(self) -> Track or None:
        if len(self.items) > 0:
            return self.items[0]
        else:
            return None
    
    def back(self) -> Track:
        if len(self.items) > 0:
            return self.items[-1]
        
    def next(self) -> Track or None:
        if len(self.items) >= 2:
            return self.items[1]
    
    def dequeue(self) -> Track or None:
        if len(self.items) > 0:
            track = self.items[0]
            """ print(getcwd() + track.path[1:])
            path = Path(args = f'{getcwd()}{track.path[1:]}')
            path.unlink(missing_ok=True) """
            self.items = self.items[1:]
            return track
        
    def enqueue(self, track: Track):
        self.items.append(track)
        
    def size(self):
        return len(self.items)