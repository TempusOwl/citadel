
from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(798324364301959169)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title=":page_facing_up: Username Change",
                          colour=9807270,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(description=f":page_facing_up: {after.mention} **ID ( {after.id} )**",
                          colour=612934,
                          timestamp=datetime.utcnow())

            embed.set_author(
                name=f"Nickname Updated", icon_url=f"{after.avatar_url}")

            namemessage = before.display_name + " :arrow_right:  " + after.name

            fields = [
                ("New Name ", namemessage, False)]
            # , ("Joined", after.JoinedAt, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.roles != after.roles:

            before_set = set(before.roles)
            after_set = set(after.roles)

            difference = set(before.roles)-set(after.roles)

            isEmpty = (len(difference) == {})
            print(difference)

            if not isEmpty:
                embed = Embed(title="Role Updates",
                              colour=9807270,
                              timestamp=datetime.utcnow())

                fields = [("Removed", ", ".join(
                    [r.mention for r in difference]), False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

            else:

                embed = Embed(title="Role Updates",
                              colour=9807270,
                              timestamp=datetime.utcnow())

                fields = [("Added", ", ".join(
                    [r.mention for r in difference]), False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content and not before.author.bot:
            acontent_clamp = after.content
            bcontent_clamp = before.content
            embed = Embed(description=f":page_facing_up: {after.author.mention} **ID (**{after.author.id}**)**",
                          colour=0xFFE4AF,
                          timestamp=datetime.utcnow())

            fields = [("Before", bcontent_clamp[:750], False),
                      ("After", acontent_clamp[:750], False)]

            embed.set_author(
                name=f"Edited By {after.author.name}", icon_url=f"{after.author.avatar_url}")
           # embed.set_footer(text=f"Message ID {before.author.message.id}")

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            msg_clamp = message.content
            embed = Embed(description=f":warning: {message.author.mention} **ID (*{message.author.id}*)**",
                          colour=15158332,
                          footer=f"UserID {message.author.id}.",
                          timestamp=datetime.utcnow())
            embed.set_author(
                name=f"Deletion By {message.author.name}", icon_url=f"{message.author.avatar_url}")
            embed.set_footer(text=f"Deleted Message ID = {message.id}")
            fields = [("Message Content", msg_clamp[:950], False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))
