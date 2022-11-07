import asyncio
import os

import pycord
import discord
import random
import nacl

from discord.ext import commands, tasks
from dotenv import load_dotenv
import youtube_dl

import ctypes
import ctypes.util

if not discord.opus.is_loaded():
    discord.opus.load_opus('/Users/tyarpornsuksant/swe/coldbrew-coders/ty_testing/bot_dev/opus/1.3.1/lib/libopus.0.dylib')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
brewbot = commands.Bot(intents=intents, command_prefix="!")


@brewbot.event
async def on_ready():
    for guild in brewbot.guilds:
        print(
            f'{brewbot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )


@brewbot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Coldbrew Cafe!'
    )


@brewbot.event
async def on_message(ctx):
    print("On_message detected")
    
    if ctx.author == brewbot.user:  # check if sender is bot itself (avoids recursion)
        return
    if ctx.content == 'Hi' or ctx.content == 'hi':
        response = "Hello, welcome to the Coldbrew Cafe!"
        await ctx.channel.send(response)
        
    await brewbot.process_commands(ctx) # need this to check commands afterwards


@brewbot.command(name='test', help='Test command functionality')
async def test(ctx):
    print("Test command executed successfully!")
    await ctx.send("Test successful!")

@brewbot.command(name='join', help='Tells the bot to join the voice channel')
async def join(message):
    if not message.message.author.voice:
        await message.send("{} is not connected to a voice channel".format(message.message.author.name))
        return
    else:
        channel = message.message.author.voice.channel
    await channel.connect()

@brewbot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await message.send("The bot is not connected to a voice channel.")


@brewbot.command(name='play_song', help='To play song')
async def play(message, url):
    # try:
        server = message.message.guild
        voice_channel = server.voice_client

        async with message.typing():
            filename = await YTDLSource.from_url(url, loop=brewbot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="/Users/tyarpornsuksant/swe/coldbrew-coders/ty_testing/ffmpeg", source=filename))
        await message.send('**Now playing:** {}'.format(filename))
    # except:
        # await message.send("The bot is not connected to a voice channel.")

@brewbot.command(name='pause', help='This command pauses the song')
async def pause(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await message.send("The bot is not playing anything at the moment.")


@brewbot.command(name='resume', help='Resumes the song')
async def resume(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await message.send("The bot was not playing anything before this. Use play_song command")


@brewbot.command(name='stop', help='Stops the song')
async def stop(message):
    voice_client = message.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await message.send("The bot is not playing anything at the moment.")
youtube_dl.utils.bug_reports_message = lambda: ''
#
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

if __name__ == "__main__":
    brewbot.run(TOKEN)
