import discord
import os

client = discord.Client()

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
        arg = argArry[1]

        if (len(argArray) > 2):
            await message.channel.send('Expected one argument, got {num}', len(argArray))
        
        #audio =  await fetchSpotifyAudio(arg)

client.run(os.getenv('TOKEN'))
