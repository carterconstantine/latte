import nextcord
from nextcord.ext import commands
import asyncio

from utils import scoresaber, logger

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="calculate_pp",description="Calculate the amount of PP given for a star rating and accuracy")
    async def calculate_pp(self, interaction: nextcord.Interaction, stars: float, acc: float):
        await interaction.response.send_message(f"```Stars: {stars}\nAcc: {acc}\nPP: {round(scoresaber.calculate_pp(acc, stars), 2)}```")

    @nextcord.slash_command(name="calculate_acc",description="Calculate the acc needed to get an amount of pp on a map with a certain amount of stars")
    async def calculate_acc(self, interaction: nextcord.Interaction, stars: float, pp: float):
        await interaction.response.send_message(f"```Stars: {stars}\nPP: {pp}\nAcc: {scoresaber.calculate_acc(pp, stars)}```")

def setup(bot):
    bot.add_cog(Calculator(bot))
