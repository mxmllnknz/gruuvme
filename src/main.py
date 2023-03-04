import discord
from discord.ext import commands
from discord.utils import get
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import downloader
from track import Track
from player import Voice
from discord.utils import get

load_dotenv()


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

# TODO: make a spotify module separately
async def fetchSpotifyTrack(url: str) -> Track:
    # use sp.track or sp.tracks() and a parameter(s) of spotify URL
    track_dict = sp.track(url)
    name = track_dict.get('name')
    album_dict = track_dict.get('album')
    artist = album_dict.get('artists')[0].get('name')
    return Track(f'{artist} {name}', 'spotify')

""" async def fetchYoutubeTrack(url: str) -> Track:
    return  """

""" @client.event
async def on_message(message):
    
    if message.content.startswith('$play'):
        
        argArray = message.content.split()

        if (len(argArray) != 2):
            await message.channel.send(f'Expected one argument, got {len(argArray) - 1}')
            return
        
        
        arg = argArray[1]

        if 'spotify' in message.content:
            track = await fetchSpotifyTrack(arg)
            await downloader.download_video(track.url)
        """
        
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.3.1/lib/libopus.dylib')
    if not discord.opus.is_loaded():
        raise RuntimeError("Opus not loaded")
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Play a song in a voice channel')
async def play(ctx, url: str):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    if not voice_channel:
        join(ctx)
    
    if 'spotify' in ctx.message.content:
        track = await fetchSpotifyTrack(url)
        await downloader.download_video(track.url)
        filename = f'./{track.title} [{track.vid}].m4a'
    
    voice_channel.play(discord.FFmpegPCMAudio(source=filename))
    
    
            
@bot.command(name='ping', help='Pings the bot server to check status')
async def ping(ctx):
    await ctx.send("I'm alive!")


bot.run(os.getenv('DISCORD_TOKEN'))

