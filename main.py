import discord
from discord.ext import commands
from discord import option
from dotenv import load_dotenv
import os
import random
import datetime
import time

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

meows = ["meow","mrrp","mrrrow","mraow","miau","mew","prrt","prrp","prrrt","prrrp","purr","mrrow","mrrrrow","mreeeooow","mlem"]

memory = {}

@bot.slash_command(description = "Make Latte speak!")
async def meow(ctx):
    await ctx.response.send_message(random.choice(meows))

@bot.slash_command(description = "Make Latte eat a specific user!")
async def chomp(ctx,user: discord.User):
    global memory
    guild = ctx.guild.id
    if not guild in memory:
        memory[guild] = {}
    if not "last_chomped_user" in memory[guild]:
        memory[guild]["last_chomped_user"] = 0
    if not "chomp_user_cooldown" in memory[guild]:
        memory[guild]["chomp_user_cooldown"] = 0

    if memory[guild]["last_chomped_user"] + memory[guild]["chomp_user_cooldown"] <= time.time():
        duration = datetime.timedelta(minutes=2)
        try:
            await user.timeout_for(duration, reason="Eaten by Latte")
            await ctx.response.send_message(f"{user.mention} was chomped by Latte!")
            memory[guild]["last_chomped_user"] = time.time()
            memory[guild]["chomp_user_cooldown"] = 600
            memory[guild]["user_cooldown_cause"] = "chomp"
        except discord.Forbidden:
            await ctx.response.send_message(f"Latte tried to chomp {user.mention}, but they were too powerful.")
            memory[guild]["last_chomped_user"] = time.time()
            memory[guild]["chomp_user_cooldown"] = 30
            memory[guild]["user_cooldown_cause"] = "chomp"
        except AttributeError:
            await ctx.response.send_message(f"I looked all over for {user} but couldn't find them. Did you give me the right name?")
    else:
        timestamp = memory[guild]["last_chomped_user"] + memory[guild]["chomp_user_cooldown"]
        if memory[guild]["user_cooldown_cause"] == "chomp":
            await ctx.response.send_message(f"My jaw is tired :( I can chomp again <t:{int(round(timestamp, 0))}:R>.")
        elif memory[guild]["user_cooldown_cause"] == "string":
            await ctx.response.send_message(f"I'm playing right now! I can chomp again <t:{int(round(timestamp, 0))}:R>.")

@bot.slash_command(description = "Make Latte eat a random user!")
async def random_chomp(ctx):
    global memory
    guild = ctx.guild.id
    if not guild in memory:
        memory[guild] = {}
    if not "last_chomped" in memory[guild]:
        memory[guild]["last_chomped"] = 0
    if not "chomp_cooldown" in memory[guild]:
        memory[guild]["chomp_cooldown"] = 0

    if memory[guild]["last_chomped"] + memory[guild]["chomp_cooldown"] <= time.time():
        random_user = random.choice(ctx.guild.members)
        duration = datetime.timedelta(minutes=1)
        try:
            await random_user.timeout_for(duration, reason="Eaten by Latte")
            await ctx.response.send_message(f"{random_user.mention} was randomly chomped by Latte!")
            memory[guild]["last_chomped"] = time.time()
            memory[guild]["chomp_cooldown"] = 180
            memory[guild]["cooldown_cause"] = "chomp"
        except discord.Forbidden:
            await ctx.response.send_message(f"Latte tried to chomp {random_user.mention}, but they were too powerful.")
            memory[guild]["last_chomped"] = time.time()
            memory[guild]["chomp_cooldown"] = 30
            memory[guild]["cooldown_cause"] = "chomp"
    else:
        timestamp = memory[guild]["last_chomped"] + memory[guild]["chomp_cooldown"]
        if memory[guild]["cooldown_cause"] == "chomp":
            await ctx.response.send_message(f"My jaw is tired :( I can randomly chomp again <t:{int(round(timestamp, 0))}:R>.")
        elif memory[guild]["cooldown_cause"] == "string":
            await ctx.response.send_message(f"I'm playing right now! I can randomly chomp again <t:{int(round(timestamp, 0))}:R>.")

@bot.slash_command(description = "Give Latte a string to play with to distract her from chomping for a few minutes!")
async def string(ctx):
    global memory
    guild = ctx.guild.id
    if not guild in memory:
        memory[guild] = {}
    if not "last_distracted" in memory[guild]:
        memory[guild]["last_distracted"] = 0
    if not "distract_cooldown" in memory[guild]:
        memory[guild]["distract_cooldown"] = 0
    if not "last_chomped" in memory[guild]:
        memory[guild]["last_chomped"] = 0
    if not "chomp_cooldown" in memory[guild]:
        memory[guild]["chomp_cooldown"] = 0
    if memory[guild]["last_chomped"] + memory[guild]["chomp_cooldown"] <= time.time():
        memory[guild]["last_chomped_user"] = time.time()
        memory[guild]["last_chomped"] = time.time()
        memory[guild]["last_distracted"] = time.time()
        memory[guild]["chomp_user_cooldown"] = 900
        memory[guild]["chomp_cooldown"] = 900
        memory[guild]["distract_cooldown"] = 1800
        memory[guild]["user_cooldown_cause"] = "string"
        memory[guild]["cooldown_cause"] = "string"
        timestamp = memory[guild]["last_chomped"] + memory[guild]["chomp_cooldown"]
        await ctx.response.send_message(f"Latte is now distracted! She can chomp again <t:{int(round(timestamp, 0))}:R>.")
    else:
        timestamp = memory[guild]["last_distracted"] + memory[guild]["distract_cooldown"]
        if memory[guild]["last_chomped"] + memory[guild]["chomp_cooldown"] <= time.time():
            await ctx.response.send_message(f"I'm tired of playing! I'll play with you again <t:{int(round(timestamp, 0))}:R>.")
        else:
            await ctx.response.send_message(
                f"I'm already playing! I'll play with you again <t:{int(round(timestamp, 0))}:R>.")

@bot.slash_command(description = "Make Latte send a cute pic!")
async def selfie(ctx):
    await ctx.response.send_message(file=discord.File(f"C:.\\selfies\\{random.choice(os.listdir("C:.\\selfies"))}", f"latte_pic.jpg"))

@bot.slash_command(description = "Info about this bot!")
async def about(ctx):
    await ctx.response.send_message("I am a bot inspired by Norlore's cat Latte and I was developed by amthyst_. Run /help to learn about my commands!")

@bot.slash_command(description = "Descriptions of all the commands that you can use with this bot!",name="help")
async def latte_help(ctx):
    await ctx.response.send_message("/meow - Displays a random cat noise!\n/chomp - Times out a user of your choice for 2 minutes! Has a cooldown of 10 minutes.\n/random_chomp - Times out a random user for a minute! Has a cooldown of 3 minutes.\n/selfie - Displays a random picture of Latte the cat!\n/string - Distracts Latte from chomping people for 15 minutes! Has a cooldown of 30 minutes.\n/about - Displays some basic info about the Latte bot.\n/help - Displays short descriptions of all of this bot's commands.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)