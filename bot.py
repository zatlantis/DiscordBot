# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import music

from youtube import YouTubeSource
from youtubesearch import YouTubeSearch

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

Bot = commands.Bot(command_prefix='.', description='Test music bot.')
Bot.add_cog(music.Music(Bot))

@Bot.listen()
async def on_ready():
    print('Logged in as: {0.user}\nUser ID: {0.user.id}'.format(Bot))

    print('Connected to servers:')
    for Guild in Bot.guilds:
        print('\t{0.name}: {0.id}\n'.format(Guild))

@Bot.listen()
async def on_message(message):
    if message.author == Bot.user:
        return
   
    #if util.IsMisplacedBotMessage(message):
        #await message.delete()
        
Bot.run(TOKEN)

#youtube_search = YouTubeSearch('hello').get_first_Result()
#print(youtube_search)

#youtube_source = YouTubeSource(youtube_search)
#stream_url = youtube_source.get_best_stream_link()
#print(youtube_source.video_id)

