
import math
import aiosqlite
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command, has_permissions
from discord.ext.commands import Cog

from ..db import db
# should be fixed


class Leveling(Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.multiplier = 1

    @command()
    async def on_message(self, message):
        if not message.author.bot:
            cursor = await db.field("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1))
            if cursor.rowcount == 0:
                await db.field("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                cur = await db.field("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                data = await cur.fetchone()
                exp = data[0]
                lvl = math.sqrt(exp) / bot.multiplier
                if lvl.is_integer():
                    await message.channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")
            await bot.db.commit()
        await bot.process_commands(message)

    @command()
    async def level(self, ctx, message, member: discord.Member = None):
        if member is None:
            member = ctx.author
        # get user exp
        async with db.field("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)):
            exp = data[0, 0]
            # calculate rank
        async with db.field("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            rank = 1
            async for value in cursor:
                if exp < value[0]:
                    rank += 1
        lvl = int(math.sqrt(exp)//bot.multiplier)
        current_lvl_exp = (bot.multiplier*(lvl))**2
        next_lvl_exp = (bot.multiplier*((lvl+1)))**2
        lvl_percentage = ((exp-current_lvl_exp) /
                          (next_lvl_exp-current_lvl_exp)) * 100
        embed = discord.Embed(
            title=f"Stats for {member.name}", colour=discord.Colour.gold())
        embed.add_field(name="Level", value=str(lvl))
        embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
        embed.add_field(
            name="Rank", value=f"{rank}/{ctx.guild.member_count}")
        embed.add_field(name="Level Progress",
                        value=f"{round(lvl_percentage, 2)}%")
        await ctx.send(embed=embed)

    @command()
    async def leaderboard(self, ctx):
        buttons = {}
        for i in range(1, 6):
            # only show first 5 pages
            buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i
        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10
        embed = discord.Embed(
            title=f"Leaderboard Page {current}", description="", colour=discord.Colour.gold())
        msg = await ctx.bot.send(embed=embed)
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            if current != previous_page:
                embed.title = f"Leaderboard Page {current}"
                embed.description = ""
                async with db.field(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                    index = entries_per_page*(current-1)
                    async for entry in cursor:
                        index += 1
                        member_id, exp = entry
                        member = ctx.guild.get_member(member_id)
                        embed.description += f"{index}) {member.mention} : {exp}\n"
                    await msg.edit(embed=embed)
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()
            else:
                previous_page = current
                await msg.remove_reaction(reaction.emoji, ctx.author)
                current = buttons[reaction.emoji]
                asyncio.run(bot.db.close())

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("leveling")


def setup(bot):
    bot.add_cog(Leveling(bot))
