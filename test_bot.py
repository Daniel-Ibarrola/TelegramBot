from bot import telegramBot

bots = [telegramBot.cires_bot(),
        telegramBot.test_bot(),
        telegramBot.myassistant_bot()]

for bot in bots:
    print(f"Created bot with name {bot.name} and token {bot.token}")
    print(f"Base url for this bot is {bot.base_url}")
    print(bot.groups())
    print("\n\n")

