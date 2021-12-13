#music.py
import io
from logging import error
import time
import os
import asyncio
import threading

import discord
from discord import client
from discord import VoiceClient
from discord import voice_client
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord import voice_client
from discord import channel
from discord import channel

from youtube import YouTubeSource
from youtubesearch import YouTubeSearch

from discord_util import DiscordUtil as DUtil

FFMPEG_OPTIONS = {'before_options': '-method GET -multiple_requests 1 -reconnect_on_http_error \"3xx\",\"4xx\",\"5xx\" -reconnect_on_network_error 1 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -user_agent \"Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3\"', 'options': '-vn'}
class Music(commands.Cog):            
    def __init__(self, bot: commands.Bot):
        self.bot :commands.Bot = bot
        self.playlists = { 'guild' : 123,  'songs' : [] }

    @commands.command(name='leave', invoke_without_subcommand=True)
    async def _leave(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        destination = ctx.author.voice.channel
        
        if ctx.voice_client and ctx.author.voice.channel:
            await ctx.voice_client.move_to(destination)
            return

        await destination.connect()

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_client:
            await ctx.invoke(self._join)

        async with ctx.typing():                       
            if 'v=' not in search: # Is this a link or a search?
                yt_search = YouTubeSearch(search).get_first_result()
                yt_source = YouTubeSource(yt_search)
            else:                       
                yt_source = YouTubeSource(search)

            stream_url = yt_source.get_best_stream_link()
            print(yt_source.video_title)
            print(yt_source.video_link)
                                                      
        if stream_url:
            ctx.voice_client.play(discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS))
        else:
            await ctx.send("Unable to find what you're looking for. :(")

    @commands.command(name='skip', aliases=['s'])
    async def _skip(self, ctx: commands.Context):
        voice_client = DUtil.get_guild_voice_client(ctx)
        if voice_client == None:
            return
        voice_client.voice_connect()
            
    @commands.command(name='stop', invoke_without_subcommand=True)
    async def _stop(self, ctx: commands.Context):
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()

    @_join.before_invoke
    @_leave.before_invoke
    @_play.before_invoke
    @_stop.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.BadArgument('You are not connected to a voice channel.')

    @_leave.before_invoke
    @_stop.before_invoke
    async def ensure_voice_client(self, ctx: commands.Context):
        if not ctx.voice_client:
            raise commands.BadArgument('Bot not currently connected to a channel.')