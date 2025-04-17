import discord
from discord.ext import commands
import yt_dlp
import asyncio

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

queues = {}

@bot.event
async def on_ready():
    print(f"🎶 Music Bot is online as {bot.user}")

def play_next(ctx):
    guild_id = ctx.guild.id
    if queues.get(guild_id):
        url = queues[guild_id].pop(0)

        ydl_opts = {'format': 'bestaudio', 'quiet': True, 'no_warnings': True}
        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            vc.play(discord.FFmpegPCMAudio(url2), after=lambda e: play_next(ctx))

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Joined {channel}")
    else:
        await ctx.send("Join a voice channel first!")

@bot.command()
async def play(ctx, url):
    guild_id = ctx.guild.id
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You're not in a voice channel!")
            return

    if guild_id in queues:
        queues[guild_id].append(url)
        await ctx.send("🎵 Added to queue!")
    else:
        queues[guild_id] = []
        queues[guild_id].append(url)

        ydl_opts = {'format': 'bestaudio', 'quiet': True, 'no_warnings': True}
        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            vc.play(discord.FFmpegPCMAudio(url2), after=lambda e: play_next(ctx))

        await ctx.send(f"▶️ Now playing: {info['title']}")

@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped to next song.")
    else:
        await ctx.send("Nothing to skip!")

@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed.")
    else:
        await ctx.send("It's not paused.")

@bot.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if queues.get(guild_id):
        song_list = "\n".join([f"{idx + 1}. {url}" for idx, url in enumerate(queues[guild_id])])
        await ctx.send(f"🎶 Queue:\n{song_list}")
    else:
        await ctx.send("Queue is empty!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queues.pop(ctx.guild.id, None)
        await ctx.send("👋 Left the voice channel and cleared the queue.")
    else:
        await ctx.send("I'm not even in a channel!")

bot.run(TOKEN)
