import sys
import os
import random
import discord
import asyncio
import aiohttp

from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions
from discord.ext import commands

from ..db import db


class owner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def changestatus(self, ctx, status: str):
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus, )
        await ctx.send(f':white_check_mark: Succesfully changed status - **{discordStatus} (Options: offline, dnd, idle or else = online)**')

    @commands.command(hidden=True)
    async def leaveserver(self, ctx, guildid: str):
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Left {guild.name}!'
            else:
                msg = ':x: Unable to find guild with matching ID!'
                await ctx.send(msg)

    # @commands.command(hidden=True)
    # async def botstatus(self, ctx, gameType: str, *, gameName: str):
    #    '''(BOT OWNER ONLY)'''
    #    gameType = gameType.lower()
    #    if gameType == 'guard':
    #        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game("with my source code"))
    #        await ctx.send(f'**:ok:** test: {gameType} **{gameName}**')

    @ Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("owner")


def setup(bot):
    bot.add_cog(owner(bot))
