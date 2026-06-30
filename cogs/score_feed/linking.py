import nextcord
from nextcord.ext import commands, application_checks

from utils import logger, save_data

class ScoreFeedLinking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = bot.bot_data

    @nextcord.slash_command(name="unregister", description="Unregister a user from the score feed")
    @application_checks.has_role(1451663801534517318)
    async def unregister(self, interaction: nextcord.Interaction, scoresaber_id: str = nextcord.SlashOption(
        description="The scoresaber id of the user you're unregistering")):
        while scoresaber_id in self.bot_data["registered"]:
            self.bot_data["registered"].pop(scoresaber_id)
        if scoresaber_id in self.bot_data["user_data"]:
            del self.bot_data["user_data"][scoresaber_id]
        save_data.save_data(self.bot_data)
        await interaction.response.send_message(f"User `{int(scoresaber_id)}` has been unregistered successfully!",
                                                ephemeral=True)
        await logger.log(self.bot,f"{interaction.user.name} unregistered `{scoresaber_id}` (https://scoresaber.com/u/{scoresaber_id}) in channel {interaction.channel.name} in server {interaction.guild.name} (<#{interaction.channel.id}>)")

    @nextcord.slash_command(name="link",description="Link your scoresaber account to your discord account (requires admin verification)")
    async def link(self, interaction: nextcord.Interaction,
                   scoresaber_id: str = nextcord.SlashOption(description="Your scoresaber id")):
        self.bot_data["link_requests"][interaction.user.name] = scoresaber_id
        save_data.save_data(self.bot_data)
        await interaction.response.send_message(
            f"Your link request went through successfully. Please wait for admin approval.", ephemeral=True)
        await logger.log(self.bot,f"<@&1514820851093078096> {interaction.user.name} wants to link https://scoresaber.com/u/{scoresaber_id} with their discord account. Run `/approve_link {interaction.user.name}` if this is correct (or `/deny_link {interaction.user.name}` if it isn't).")

    @nextcord.slash_command(name="approve_link", description="Approve a user's link request")
    @application_checks.has_role(1451663801534517318)
    async def approve_link(self, interaction: nextcord.Interaction, username: str = nextcord.SlashOption(
        description="The discord username to accept the link request of")):
        scoresaberid = self.bot_data["link_requests"][username]
        self.bot_data["user_data"][scoresaberid] = {}
        self.bot_data["disc_to_ss"][username] = scoresaberid
        self.bot_data["link_requests"].pop(username)
        save_data.save_data(self.bot_data)
        await interaction.response.send_message(f"User link approved successfully!", ephemeral=True)
        await logger.log(self.bot, f"User {username} linked to https://scoresaber.com/u/{scoresaberid} successfully.")

        member = nextcord.utils.get(interaction.guild.members, name=username)
        await self.bot.get_channel(1503853324154437733).send(
            f"<@{member.id}>, your scoresaber profile has been linked to your profile successfully!")

    @nextcord.slash_command(name="deny_link", description="Deny a user's link request")
    @application_checks.has_role(1451663801534517318)
    async def deny_link(self, interaction: nextcord.Interaction, username: str = nextcord.SlashOption(
        description="The discord username to deny the link request of"),
                        reason: str = nextcord.SlashOption(description="The reason to deny the link request")):
        scoresaberid = self.bot_data["link_requests"][username]
        self.bot_data["link_requests"].pop(username)
        save_data.save_data(self.bot_data)
        await interaction.response.send_message(f"User link denied successfully.", ephemeral=True)
        await logger.log(self.bot, f"User {username} link to https://scoresaber.com/u/{scoresaberid} denied.")

        member = nextcord.utils.get(interaction.guild.members, name=username)
        await self.bot.get_channel(1503853324154437733).send(f"<@{member.id}>, your scoresaber profile link request has been denied with reason: {reason}.")

    @nextcord.slash_command(name="get_user_status", description="Get the link status of a specific user")
    async def get_user_status(self, interaction: nextcord.Interaction, scoresaber_id: str):
        if scoresaber_id in self.bot_data["user_data"]:
            status = "linked"
        elif scoresaber_id in self.bot_data["link_requests"]:
            status = "pending"
        elif scoresaber_id in self.bot_data["legacyRegistered"]:
            status = "legacyRegistered"
        else:
            status = "unlinked"

        await interaction.response.send_message(f"User data for {scoresaber_id}:\nStatus: {status}")