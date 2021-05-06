import sys
import os
import random
import discord
import asyncio
import aiohttp

from datetime import datetime, timedelta
from platform import python_version
from time import time
from psutil import Process, virtual_memory

from apscheduler.triggers.cron import CronTrigger

from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog, Greedy
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

    @command(name="ping")
    async def ping(self, ctx):
        start = time()
        message = await ctx.send(f"Pong!  Discord Latency: {self.bot.latency*1000:,.0f} ms.")
        end = time()
        await message.edit(content=f"Pong! Discord Latency: {self.bot.latency*1000:,.0f} ms. Response Achieved In: {(end-start)*1000:,.0f} ms.")

    @command(name="stats")
    async def show_bot_stats(self, ctx):
        embed = Embed(title="Bot stats",
                      colour=ctx.author.colour,
                      thumbnail=self.bot.user.avatar_url,
                      timestamp=datetime.utcnow())

        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(
                seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            ("Bot version", self.bot.VERSION, True),
            ("Python version", python_version(), True),
            ("Discord.py version", discord_version, True),
            ("Uptime", uptime, True),
            ("CPU time", cpu_time, True),
            ("Memory usage",
             f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
            ("Users", f"{self.bot.guild.member_count:,}", True),
            ("Developer", "TempusOwl#0001", False)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("owner")


def setup(bot):
    bot.add_cog(owner(bot))
