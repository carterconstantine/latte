async def log(bot, log_text: str):
    print(log_text)
    with open("log.txt", "a") as file:
        file.write(f"{log_text}\n")
    await bot.get_channel(1512894508931616768).send(log_text)