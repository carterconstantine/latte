import nextcord
from nextcord.ext import commands

from utils import logger

class TwitchNotifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        def is_streaming(member: nextcord.Member) -> bool:
            return any(
                activity.type == nextcord.ActivityType.streaming
                for activity in (member.activities or [])
            )

        before_streaming = is_streaming(before)
        after_streaming = is_streaming(after)

        if not before_streaming and after_streaming:
            stream = next(
                activity for activity in after.activities
                if activity.type == nextcord.ActivityType.streaming
            )
            await self.bot.get_channel(1451663905683406950).send(
                f"<@&1473824951604613273> {after.display_name} is now live! {stream.url}")

        if before_streaming and not after_streaming:
            await self.bot.get_channel(1451663905683406950).send(f"{after.display_name} is no longer live.")

def setup(bot):
    bot.add_cog(TwitchNotifs(bot))