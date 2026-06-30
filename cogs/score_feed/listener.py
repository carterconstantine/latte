from nextcord.ext import commands, tasks

import websockets
import asyncio
import json

from utils import logger
from utils.score_feed import score_parser, embed_builder

class ScoreFeedListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = bot.bot_data
        self.listener.start()

    @tasks.loop(seconds=0)
    async def listener(self):
        await logger.log(self.bot, "Connecting to the ScoreSaber WSS...")
        while True:
            try:
                async with websockets.connect("wss://scoresaber.com/ws") as websocket:
                    while True:
                        try:
                            score = await websocket.recv()
                            score_data = {}
                            if score == "Connected to the ScoreSaber WSS":
                                await logger.log(self.bot, "Connected to the ScoreSaber WSS")
                            else:
                                score = json.loads(score)
                                if score["commandName"] == "score":
                                    if score["commandData"]["score"]["leaderboardPlayerInfo"]["id"] in self.bot_data["legacyRegistered"] or score["commandData"]["score"]["leaderboardPlayerInfo"]["id"] in self.bot_data["user_data"]:
                                        score_data = score_parser.parse_score(score["commandData"]["score"]["id"], self.bot_data)

                            channel = self.bot.get_channel(1503853324154437733)
                            if score_data != {}:
                                if score_data["stars"] > 0:
                                    await channel.send(embed=embed_builder.build_embed(score_data, "scoresaber", self.bot_data),view=embed_builder.build_view(score_data, "scoresaber", self.bot_data))
                                    await logger.log(self.bot,f"Posted {score_data['pp']}pp score by {score_data['name']} on {score_data['songName']} {score_data['difficulty']}")
                                if score_data["complexity"] > 0:
                                    await channel.send(embed=embed_builder.build_embed(score_data, "accsaber", self.bot_data),view=embed_builder.build_view(score_data, "accsaber", self.bot_data))
                                    await logger.log(self.bot,f"Posted {score_data['ap']}ap score by {score_data['name']} on {score_data['songName']} {score_data['difficulty']}")

                        except websockets.ConnectionClosed:
                            await logger.log(self.bot, "Websocket closed, reconnecting...")
                            break

            except Exception as e:
                await logger.log(self.bot, f"Websocket error: {e}")

            await asyncio.sleep(3)