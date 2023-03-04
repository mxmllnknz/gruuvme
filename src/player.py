import discord

#see discord.VoiceChannel.connect
class Voice:
    def __init__(self, client, channel):
        self.channel = discord.VoiceChannel(channel=channel)
        self.voice_client = self.channel.connect(self_deaf=True)
        
    