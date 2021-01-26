import discord
from asyncio import sleep
from datetime import datetime
from glob import glob
from ..cogs.utils import checks, cache

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, Intents
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (
    CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)

from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db

OWNER_IDS = [134118092082118657]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
    prefix = db.field(
        "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send("Remember to adhere to the rules!")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("Try again in a few seconds.")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        print("An error occured.")  # Catches any error.
        raise  # type: ignore

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):  # Hides any error
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Command is on cooldown, try again in {exc.retry_after:,.2f} seconds ( {str(exc.cooldown.type).split('.')[-1]} cooldown )")

        elif isinstance(exc, HTTPException):
            await ctx.send("Unable to send message")

        elif isinstance(exc.original, Forbidden):
            await ctx.send("I do not have permission to do that.")

        else:
            raise exc  # Potential Multi Server Problem

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(663234840530780170)
            self.stdout = self.get_channel(796934983049543691)
            self.scheduler.add_job(
                self.rules_reminder,
                CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Now online!")
            self.ready = True

            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Guard'))
            print("bot ready")

        else:
            print("bot reconnected")

        async def on_message(self, message):
            if not message.author.bot:
                await self.process_command(message)


bot = Bot()
