import nextcord
from nextcord.ext import commands

from utils import save_data
from utils.score_feed import customizations
from utils.score_feed import score_parser

class ScoreFeedConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = bot.bot_data

    @nextcord.slash_command(name="get_available_stats", description="List all the stats that you can display in your score feed embed")
    async def get_available_stats(self, interaction: nextcord.Interaction, private: bool = nextcord.SlashOption(choices={"True": True, "False": False}, default=True)):
        await interaction.response.defer(ephemeral=private)
        data = score_parser.parse_score(91902339, self.bot_data)
        message = ""
        for i in data:
            message += f"{i}\n"
        await interaction.followup.send(message, ephemeral=private)

    @nextcord.slash_command(name="customize_score_feed_other",description="Customize other elements of your score feed embed!")
    async def customize_score_feed_other(
        self,
        interaction: nextcord.Interaction,
        element: str = nextcord.SlashOption(choices={
            "Emoji": "emoji",
            "Separator": "separator"}),
        text: str = "",
        exclusive_leaderboard: str = nextcord.SlashOption(
            choices={
                "ScoreSaber": "scoresaber",
                "AccSaber": "accsaber",
            },
            required= False
        ),
    ):

        leaderboard = exclusive_leaderboard or "common"

        if interaction.user.name not in self.bot_data.get("disc_to_ss", {}):
            await interaction.response.send_message(
                "You cannot edit your score feed config because you are not linked. Run /link with your scoresaber id!",
                ephemeral=True
            )
            return

        ss_id = self.bot_data["disc_to_ss"][interaction.user.name]

        user_data = self.bot_data.setdefault("user_data", {})
        user_entry = user_data.setdefault(ss_id, {})
        custom_elements = user_entry.setdefault("score_feed_custom_elements", {})
        leaderboard_elements = custom_elements.setdefault(leaderboard, {})

        if element not in leaderboard_elements:
            leaderboard_elements[element] = {
                "text": text.replace("\\s", " ")
            }
        else:
            if text:
                leaderboard_elements[element]["text"] = text.replace("\\s", " ")
            else:
                leaderboard_elements[element]["text"] = ""

        self.bot_data["user_data"][ss_id]["score_feed_custom_elements"][leaderboard] = leaderboard_elements
        save_data.save_data(self.bot_data)

        await interaction.response.send_message(
            "Your score feed config has been updated successfully!",
            ephemeral=True
        )

    @nextcord.slash_command(name="customize_score_feed_stats",description="Customize the stats elements of your score feed embed!")
    async def customize_score_feed_stats(
            self,
            interaction: nextcord.Interaction,
            element: str = nextcord.SlashOption(choices={
                "Slot 1": "slot1",
                "Slot 2": "slot2",
                "Slot 3": "slot3",
                "Slot 4": "slot4",
                "Slot 5": "slot5",
                "Slot 6": "slot6",
                "Slot 7": "slot7",
                "Slot 8": "slot8",
                "Slot 9": "slot9",
            }),
            template_string: str = "",
            exclusive_leaderboard: str = nextcord.SlashOption(
                choices={
                    "ScoreSaber": "scoresaber",
                    "AccSaber": "accsaber"
                },
                required=False
            ),
    ):

        leaderboard = exclusive_leaderboard or "common"

        if interaction.user.name not in self.bot_data.get("disc_to_ss", {}):
            await interaction.response.send_message(
                "You cannot edit your score feed config because you are not linked. Run /link with your scoresaber id!",
                ephemeral=True
            )
            return

        ss_id = self.bot_data["disc_to_ss"][interaction.user.name]

        user_data = self.bot_data.setdefault("user_data", {})
        user_entry = user_data.setdefault(ss_id, {})
        custom_elements = user_entry.setdefault("score_feed_custom_elements", {})
        leaderboard_elements = custom_elements.setdefault(leaderboard, {})

        prefix, data, suffix = customizations.parse_user_input(template_string)

        if element not in leaderboard_elements:
            leaderboard_elements[element] = {
                "prefix": prefix.replace("\\s", " "),
                "data": data,
                "suffix": suffix.replace("\\s", " ")
            }
        else:
            if prefix:
                leaderboard_elements[element]["prefix"] = prefix.replace("\\s", " ")
            else:
                leaderboard_elements[element]["prefix"] = ""
            leaderboard_elements[element]["data"] = data
            if suffix:
                leaderboard_elements[element]["suffix"] = suffix.replace("\\s", " ")
            else:
                leaderboard_elements[element]["suffix"] = ""

        self.bot_data["user_data"][ss_id]["score_feed_custom_elements"][leaderboard] = leaderboard_elements
        save_data.save_data(self.bot_data)

        await interaction.response.send_message(
            "Your score feed config has been updated successfully!",
            ephemeral=True
        )

    @nextcord.slash_command(name="set_replay_colors", description="Set your saber colors in score feed replay links!")
    async def set_replay_colors(
            self,
            interaction: nextcord.Interaction,
            color: str = nextcord.SlashOption(choices={
                "Left Saber Color": "left_note_color",
                "Right Saber Color": "right_note_color"
            }),
            r: float = nextcord.SlashOption(required=True),
            g: float = nextcord.SlashOption(required=True),
            b: float = nextcord.SlashOption(required=True),
    ):
        if interaction.user.name not in self.bot_data.get("disc_to_ss", {}):
            await interaction.response.send_message(
                "You cannot edit your score feed config because you are not linked. Run /link with your scoresaber id!",
                ephemeral=True
            )
            return

        ss_id = self.bot_data["disc_to_ss"][interaction.user.name]

        user_data = self.bot_data.setdefault("user_data", {})
        user_entry = user_data.setdefault(ss_id, {})
        replay_settings = user_entry.setdefault("score_feed_replay_settings", {})

        replay_settings[color] = {
            "r": r,
            "g": g,
            "b": b,
        }

        self.bot_data["user_data"][ss_id]["score_feed_replay_settings"] = replay_settings
        save_data.save_data(self.bot_data)

        await interaction.response.send_message(
            "Your score feed config has been updated successfully!",
            ephemeral=True
        )

    @nextcord.slash_command(name="reset_score_feed_element", description="Reset an element of your score feed embed")
    async def reset_score_feed_element(
            self,
            interaction: nextcord.Interaction,
            element: str = nextcord.SlashOption(choices={
                "Slot 1": "slot1",
                "Slot 2": "slot2",
                "Slot 3": "slot3",
                "Slot 4": "slot4",
                "Slot 5": "slot5",
                "Slot 6": "slot6",
                "Slot 7": "slot7",
                "Slot 8": "slot8",
                "Slot 9": "slot9",
                "Emoji": "emoji",
                "Separator": "separator"}),
            exclusive_leaderboard: str = nextcord.SlashOption(
                choices={
                    "ScoreSaber": "scoresaber",
                    "AccSaber": "accsaber"
                },
                required=False
            ),
    ):

        leaderboard = exclusive_leaderboard or "common"
        if interaction.user.name not in self.bot_data.get("disc_to_ss", {}):
            await interaction.response.send_message(
                "You cannot edit your score feed config because you are not linked. Run /link with your scoresaber id!",
                ephemeral=True
            )
            return

        ss_id = self.bot_data["disc_to_ss"][interaction.user.name]

        user_data = self.bot_data.setdefault("user_data", {})
        user_entry = user_data.setdefault(ss_id, {})
        custom_elements = user_entry.setdefault("score_feed_custom_elements", {})
        leaderboard_elements = custom_elements.setdefault(leaderboard, {})

        leaderboard_elements.pop(element)

        self.bot_data["user_data"][ss_id]["score_feed_custom_elements"][leaderboard] = leaderboard_elements
        save_data.save_data(self.bot_data)

        await interaction.response.send_message(
            "Your score feed config has been updated successfully!",
            ephemeral=True
        )