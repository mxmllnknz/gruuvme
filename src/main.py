import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

client = discord.Client()

async def fetchSpotifyAudio(url):
    # use sp.track or sp.tracks() and a parameter(s) of spotify URL
    track_dict = sp.track(url)
    name = track_dict.get('name')
    album_dict = track_dict.get('album')
    artist = album_dict.get('artists')[0].get('name')
    return name, artist

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$play') and 'spotify' in message.content:
        argArray = message.content.split()
        arg = argArray[1]

        if (len(argArray) > 2):
            await message.channel.send('Expected one argument, got {num}', len(argArray))
        
        audio =  await fetchSpotifyAudio(arg)

client.run(os.getenv('TOKEN'))
