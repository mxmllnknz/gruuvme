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

discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.3.1/lib/libopus.dylib')
if not discord.opus.is_loaded():
    raise RuntimeError("Opus not loaded")

# TODO: make a spotify module separately
async def fetchSpotifyTrack(url: str) -> Track:
    # use sp.track or sp.tracks() and a parameter(s) of spotify URL
    track_dict = sp.track(url)
    name = track_dict.get('name')
    album_dict = track_dict.get('album')
    artist = album_dict.get('artists')[0].get('name')
    return Track(f'{artist} {name}', 'spotify')
        
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
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
async def play(ctx, url=""):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    if not voice_channel:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel. Please join one before playing music.")
        else:
            voice_channel = await channel.connect()
    
    if not url:
        if voice_channel.is_paused():
            voice_channel.resume()
            return
        else:
            ctx.send("Nothing is currently in queue.")
        return   
    
    if 'spotify' in ctx.message.content:
        track = await fetchSpotifyTrack(url)
        await downloader.download_video(track.url)
        filename = f'./tracks/{track.title} [{track.vid}].m4a'
    
    voice_channel.play(discord.FFmpegPCMAudio(source=filename))
    
@bot.command(name='pause', help='Pause the current song playing')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    voice_channel.pause()
    
@bot.command(name='stop', help='Stops the playlist from playing')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    voice_channel.stop()
            
@bot.command(name='ping', help='Pings the bot server to check status')
async def ping(ctx):
    await ctx.send("I'm alive!")


bot.run(os.getenv('DISCORD_TOKEN'))

