import nextcord
from nextcord.ext import commands
import asyncio

import random
import os

from utils import logger

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="meow", description="Make Latte speak!")
    async def meow(self, interaction: nextcord.Interaction):
        meows = ["meow", "mrrp", "mrrrow", "mraow", "miau", "mew", "prrt", "prrp", "prrrt", "prrrp", "purr", "mrrow", "mrrrrow", "mreeeooow", "mlem"]
        await interaction.response.send_message(random.choice(meows))

    @nextcord.slash_command(name="selfie", description="Make Latte send a cute pic!")
    async def selfie(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(file=nextcord.File(f"selfies/{random.choice(os.listdir("selfies"))}", f"latte_pic.jpg"))

def setup(bot):
    bot.add_cog(Cat(bot))