import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import downloader

load_dotenv()


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

client = discord.Client(intents=discord.Intents(3156992, messages=True, message_content=True))

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
    
    if message.content.startswith('$play'):
        argArray = message.content.split()

        if (len(argArray) != 2):
            await message.channel.send(f'Expected one argument, got {len(argArray) - 1}')
            return
        
        
        arg = argArray[1]

        if 'spotify' in message.content:
            audio =  await fetchSpotifyAudio(arg)
            result = await downloader.download_video("")


""" @client.event
async def on_error(event):
    print(event) """

client.run(os.getenv('DISCORD_TOKEN'))

