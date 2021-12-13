import discord
from discord.ext import commands

class DiscordUtil:
    
    @staticmethod
    def get_guild_voice_client(ctx) -> discord.VoiceClient:
        return discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)