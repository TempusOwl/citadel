from datetime import datetime
from discord import Intents
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "+"
OWNER_IDS = [134118092082118657]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(663234840530780170)
            print("bot ready")

            channel = self.get_channel(796934983049543691)
            await channel.send("Now Online!")

            embed = Embed(title="Now Online!",
                          description="Citadel Is Now Online.", color=0xFF0000, timestamp=datetime.utcnow())
            fields = [("Name", "Value", True),
                      ("and 2", "this field cool", True),
                      ("A non-inline field", "on its own row", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Citadel", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer!")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)

            await channel.send(file=File("./data/images/Mtvoq7M.jpg"))
        else:
            print("bot reconnected")

    async def on_message(self, message):
        pass


bot = Bot()
