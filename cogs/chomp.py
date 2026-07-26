import nextcord
from nextcord.ext import commands

import time
import datetime
import random

from utils import logger

class Chomp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chomp_cooldown_timestamp = 0
        self.random_chomp_cooldown_timestamp = 0
        self.ultimate_chomp_cooldown_timestamp = 0
        self.ultimate_random_chomp_cooldown_timestamp = 0

    def update_chomp_cooldown(self, new_cooldown_timestamp: float, random_chomp: bool = False):
        if random_chomp:
            self.random_chomp_cooldown_timestamp = new_cooldown_timestamp
        else:
            self.chomp_cooldown_timestamp = new_cooldown_timestamp

    def update_ultimate_chomp_cooldown(self, new_cooldown_timestamp: float, random_chomp: bool = False):
        if random_chomp:
            self.ultimate_random_chomp_cooldown_timestamp = new_cooldown_timestamp
        else:
            self.ultimate_chomp_cooldown_timestamp = new_cooldown_timestamp

    @nextcord.slash_command(name="chomp", description="Make Latte eat a specific user!")
    async def chomp(self, interaction: nextcord.Interaction, target: nextcord.Member = None):
        unchompable_role = interaction.guild.get_role(1503897277608235133)
        admin_role = interaction.guild.get_role(1451663804701343816)

        if unchompable_role in interaction.user.roles:
            await interaction.response.send_message(
                "You cannot chomp unless you're chompable. (Remove your anti cat spray role to join the fun!)",
                ephemeral=True)
            return

        now = time.time()

        random_chomp = target is None

        if random_chomp:
            members = [m for m in interaction.guild.members if not m.bot]
            target = random.choice(members)
            chomp_text = "randomly chomp"
            add_cooldown = 300
            cooldown_timestamp = self.random_chomp_cooldown_timestamp
        else:
            chomp_text = "chomp"
            add_cooldown = 600
            cooldown_timestamp = self.chomp_cooldown_timestamp

        if cooldown_timestamp > now:
            print("test")
            await logger.log(self.bot, f"{interaction.user.name} tried to {chomp_text} {target.name}, but the command was on cooldown")
            await interaction.response.send_message(
                f"My jaw is tired :( I can {chomp_text} again <t:{int(round(cooldown_timestamp, 0))}:R>.")
            return

        if admin_role in target.roles:
            self.update_chomp_cooldown(now + 30, random_chomp)
            await logger.log(self.bot,f"{interaction.user.name} tried to {chomp_text} {target.name}, but latte lacked permissions.")
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but they were too powerful.")
            return

        if unchompable_role in target.roles:
            self.update_chomp_cooldown(now + 30, random_chomp)
            await logger.log(self.bot,f"{interaction.user.name} tried to {chomp_text} {target.name}, but they had the anti cat spray role.")
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but they used anti cat spray.")
            return

        chomp_duration = datetime.timedelta(minutes=2)
        backfire = random.randint(1, 10) == 1

        if backfire:
            self.update_chomp_cooldown(now + 30, random_chomp)
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but it backfired and chomped {interaction.user.mention} instead.")
            await logger.log(self.bot,f"{interaction.user.name} tried to {chomp_text} {target.name}, but it backfired.")
            await interaction.user.timeout(chomp_duration, reason="Eaten by Latte")
            return

        self.update_chomp_cooldown(now + add_cooldown, random_chomp)
        await interaction.response.send_message(f"{target.mention} was {chomp_text}ed by Latte!")
        await logger.log(self.bot,f"{interaction.user.name} {chomp_text}ed {target.name}")
        await target.timeout(chomp_duration, reason="Eaten by Latte")

    @nextcord.slash_command(name="chomp", description="Make Latte eat a specific user!")
    async def ultimate_chomp(self, interaction: nextcord.Interaction, target: nextcord.Member = None):
        unchompable_role = interaction.guild.get_role(1503897277608235133)
        admin_role = interaction.guild.get_role(1451663804701343816)

        if unchompable_role in interaction.user.roles:
            await interaction.response.send_message(
                "You cannot chomp unless you're chompable. (Remove your anti cat spray role to join the fun!)",
                ephemeral=True)
            return

        now = time.time()

        random_chomp = target is None

        if random_chomp:
            members = [m for m in interaction.guild.members if not m.bot]
            target = random.choice(members)
            chomp_text = "randomly chomp"
            add_cooldown = 300000
            cooldown_timestamp = self.ultimate_random_chomp_cooldown_timestamp
        else:
            chomp_text = "chomp"
            add_cooldown = 600000
            cooldown_timestamp = self.ultimate_chomp_cooldown_timestamp

        if cooldown_timestamp > now:
            print("test")
            await logger.log(self.bot,
                             f"{interaction.user.name} tried to {chomp_text} {target.name}, but the command was on cooldown")
            await interaction.response.send_message(
                f"My jaw is tired :( I can {chomp_text} again <t:{int(round(cooldown_timestamp, 0))}:R>.")
            return

        if admin_role in target.roles:
            self.update_ultimate_chomp_cooldown(now + 30, random_chomp)
            await logger.log(self.bot,
                             f"{interaction.user.name} tried to {chomp_text} {target.name}, but latte lacked permissions.")
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but they were too powerful.")
            return

        if unchompable_role in target.roles:
            self.update_ultimate_chomp_cooldown(now + 30, random_chomp)
            await logger.log(self.bot,
                             f"{interaction.user.name} tried to {chomp_text} {target.name}, but they had the anti cat spray role.")
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but they used anti cat spray.")
            return

        chomp_duration = datetime.timedelta(minutes=720)
        backfire = random.randint(1, 10) == 1

        if backfire:
            self.update_ultimate_chomp_cooldown(now + 30, random_chomp)
            await interaction.response.send_message(
                f"Latte tried to {chomp_text} {target.mention}, but it backfired and chomped {interaction.user.mention} instead.")
            await logger.log(self.bot,
                             f"{interaction.user.name} tried to {chomp_text} {target.name}, but it backfired.")
            await interaction.user.timeout(chomp_duration, reason="Eaten by Latte")
            return

        self.update_ultimate_chomp_cooldown(now + add_cooldown, random_chomp)
        await interaction.response.send_message(f"{target.mention} was {chomp_text}ed by Latte!")
        await logger.log(self.bot, f"{interaction.user.name} {chomp_text}ed {target.name}")
        await target.timeout(chomp_duration, reason="Eaten by Latte")

def setup(bot):
    bot.add_cog(Chomp(bot))