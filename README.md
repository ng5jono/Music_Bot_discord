# Discord Music Bot 🎶

A Discord bot that streams YouTube audio to voice channels!

## Features
- Joins voice channel
- Plays YouTube audio links
- Queue system
- Pause, resume, skip
- Autoplay next song

## Commands
- `!join` — Join the voice channel
- `!play [url]` — Play or queue a song
- `!skip` — Skip current song
- `!pause` — Pause song
- `!resume` — Resume song
- `!queue` — Show current queue
- `!leave` — Leave channel and clear queue

## Setup
1. Install dependencies:
```
pip install discord.py yt-dlp
```
2. Install FFmpeg and add to your PATH.
3. Replace `YOUR_DISCORD_BOT_TOKEN` in `main.py`.
4. Run the bot:
```
python main.py
```

Happy listening! 🎧
