import time
import os
import platform
import re
import asyncio
import inspect
import textwrap
from datetime import datetime, timedelta
from collections import Counter
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Greedy
#from PIL import Image, ImageDraw, ImageFont


class utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @staticmethod
    def _newImage(width, height, color):
        return Image.new("L", (width, height), color)

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string == '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string == '':
            return 'None'
        else:
            # The maximum allowed charcter amount for embed fields
            return string[:1000]

    @commands.command(pass_context=True, aliases=['serverinfo', 'guild', 'membercount'])
    async def server(self, ctx):
        emojis = self._getEmojis(ctx.guild.emojis)
        # print (emojis)
        roles = self._getRoles(ctx.guild.roles)
        embed = discord.Embed(color=0xf1c40f)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Name', value=ctx.guild.name, inline=True)
        embed.add_field(name='ID', value=ctx.guild.id, inline=True)
        embed.add_field(name='Guild Owner',
                        value=ctx.guild.owner, inline=True)
        embed.add_field(name='Region', value=ctx.guild.region, inline=True)
        embed.add_field(name='Member Count',
                        value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Creation', value=ctx.guild.created_at.strftime(
            '%d.%m.%Y'), inline=True)
        if ctx.guild.system_channel:
            embed.add_field(name='Standard Channel',
                            value=f'#{ctx.guild.system_channel}', inline=True)
        embed.add_field(name='AFK Voice Timeout',
                        value=f'{int(ctx.guild.afk_timeout / 60)} min', inline=True)
        embed.add_field(name='Guild Shard',
                        value=ctx.guild.shard_id, inline=True)
        # embed.add_field(name='Role List', value=roles[10::-1] , inline=True) Too Much Spam
        embed.add_field(name='Custom Emojis', value=emojis, inline=True)
        #embed.set_footer(text='Guild ID', inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['rolelist', 'rlist', 'roles'])
    async def listroles(self, ctx):
        # print (emojis)
        roles = self._getRoles(ctx.guild.roles)
        embed = discord.Embed(color=0xf1c40f)
        embed.add_field(name='Role List', value=roles[50::1], inline=True)
        #embed.set_footer(text='Guild ID', inline=False)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("utility")


def setup(bot):
    bot.add_cog(utility(bot))
