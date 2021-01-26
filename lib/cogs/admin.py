from discord import Embed

import datetime as dt
import typing as t
from os import name
from platform import python_version
from time import time

from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions

from ..db import db


class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can not be more than 5 characters in length.")

        else:
            db.execute(
                "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefix set to {new}.")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("admin")

    @commands.command(name="guildicon", help="Displays the icon of your server.")
    async def icon_command(self, ctx):
        embed = Embed(description=f"**Displaying icon for {ctx.guild.name}.**",
                      ctx=ctx,
                      header="Information",
                      url_image=f"{ctx.guild.icon_url}",
                      )

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(admin(bot))
