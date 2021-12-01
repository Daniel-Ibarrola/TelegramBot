from bot import telegramBot

name, token = telegramBot.read_token("cires_bot")
print(f"{name} : {token}")

name, token = telegramBot.read_token("test_bot")
print(f"{name} : {token}")

name, token = telegramBot.read_token("PulpoalaDiabla_bot")
print(f"{name} : {token}")