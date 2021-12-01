from bot import telegramBot

bot_1 = telegramBot.cires_bot()
group_id = -373994761 # grupo prueba 2

while True:
    print('...')
    message  = input('Your Message: ')
    bot_1.send_message(message, group_id)
