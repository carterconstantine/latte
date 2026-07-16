import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

from utils import save_data
from utils import logger

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(intents = nextcord.Intents.all())

bot_data = save_data.load_data()
if not "legacyRegistered" in bot_data:
    bot_data["legacyRegistered"] = []
if not "link_requests" in bot_data:
    bot_data["link_requests"] = {}
if not "user_data" in bot_data:
    bot_data["user_data"] = {}
if not "disc_to_ss" in bot_data:
    bot_data["disc_to_ss"] = {}

bot.bot_data = bot_data

bot.cogs_loaded = False

@bot.event
async def on_ready():
    await logger.log(bot, "Latte started successfully!")

    allowed_guilds = {1451663499959730338}
    for guild in bot.guilds:
        if guild.id not in allowed_guilds:
            await logger.log(
                bot,
                f"Leaving unauthorized guild: {guild.name} ({guild.id})"
            )
            await guild.leave()

    if bot.cogs_loaded:
        return

    bot.cogs_loaded = True

    await logger.log(bot, "Now loading cogs...")

    bot.load_extension("cogs.calculator")
    bot.load_extension("cogs.cat")
    bot.load_extension("cogs.chomp")
    bot.load_extension("cogs.twitch_notifs")

    await logger.log(bot, "All cogs loaded.")

    await logger.log(bot, "Syncing application commands...")
    await bot.sync_application_commands()
    await logger.log(bot, "Application commands synced.")

bot.run(token)