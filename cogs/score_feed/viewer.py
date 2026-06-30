import nextcord
from nextcord.ext import commands

import requests

from utils.score_feed import score_parser, embed_builder

class ScoreFeedViewer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = bot.bot_data

    @nextcord.slash_command(name="test_score_embed",description="Send an example of what your scores will look like in score feed!")
    async def test_score_embed(self, interaction: nextcord.Interaction, score: str = nextcord.SlashOption(choices={"Top": "top", "Newest": "recent"})):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.name in self.bot_data.get("disc_to_ss"):
            api_data = requests.get(
                f"https://scoresaber.com/api/v2/players/{self.bot_data["disc_to_ss"][interaction.user.name]}/scores",
                params={
                    "limit": "1",
                    "sort": score,
                }).json()
            score_data = score_parser.parse_score(api_data["data"][0]["score"]["id"], self.bot_data)
            if score_data["stars"] > 0:
                await interaction.followup.send(embed=embed_builder.build_embed(score_data, "scoresaber", self.bot_data),
                                                view=embed_builder.build_view(score_data, "scoresaber", self.bot_data), ephemeral=True)
            if score_data["complexity"] > 0:
                await interaction.followup.send(embed=embed_builder.build_embed(score_data, "accsaber", self.bot_data),
                                                view=embed_builder.build_view(score_data, "accsaber", self.bot_data), ephemeral=True)
        else:
            await interaction.followup.send(
                "You need to link your scoresaber account to your discord account to test your score feed embed!")

    @nextcord.slash_command(name="display_score", description="Display a score using the scorer's score feed embed")
    async def display_score(
            self,
            interaction: nextcord.Interaction,
            score_id: int,
            private: bool = nextcord.SlashOption(choices={"True": True, "False": False}, default=True),
    ):
        await interaction.response.defer(ephemeral=private)
        score_data = score_parser.parse_score(score_id, self.bot_data)
        if score_data["stars"] > 0:
            await interaction.followup.send(embed=embed_builder.build_embed(score_data, "scoresaber", self.bot_data),
                                            view=embed_builder.build_view(score_data, "scoresaber", self.bot_data), ephemeral=private)
        if score_data["complexity"] > 0:
            await interaction.followup.send(embed=embed_builder.build_embed(score_data, "accsaber", self.bot_data),
                                            view=embed_builder.build_view(score_data, "accsaber", self.bot_data), ephemeral=private)