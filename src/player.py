import discord
from trackqueue import TrackQueue
from time import sleep
import threading

class Player:
    def play(self, queue: TrackQueue):
        '''
            Plays head of queue in current voice channel and starts thread to check if track is finished playing
            
            Params:
                queue - TrackQueue from which to play
        '''
        self.queue = queue
        try: 
            self.voice_channel.play(discord.FFmpegPCMAudio(source=queue.front().path))
        except:
            # TODO: Better Exception handling based on what failed (e.g. no voice_channel, no path, no front)
            raise RuntimeError('Could not play to current voice_channel')
        
        # We don't want to create infinite threads so only create a new thread if we're executing from the main thread
        if not isinstance(threading.current_thread(), threading._MainThread):
            self.next(3, queue)
        else:
            self.track_thread = threading.Thread(name='trackListener', target=self.next, args=(5, queue))
            self.track_thread.start()
            
    def next(self, seconds: float, queue: TrackQueue) -> None:
        '''
            Checks to see if the voicechannel is done playing audio
            
            Params:
                vc (VoiceChannel)   - the current bot connection to a voice channel
                seconds (float)     - period of how often we should check the channel

            Return:
                None
        '''
        current = queue.front()
        while self.voice_channel.is_playing():
            sleep(seconds)

        # TODO: I don't like this kind of check. It feels sloppy and a result of bad code design
        # Maybe we need a threading.Lock on the TrackQueue object 
        if queue.front() == current:
            queue.dequeue()
        else:
            # We have dequeued from somewhere else and we should kill this thread
            return
        
        if queue.size() > 0:
            self.play(queue)