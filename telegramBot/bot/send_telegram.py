from bot import telegramBot
import os

bot_1 = telegramBot.cires_bot()
group_id = -373994761 # grupo prueba 2
channel_id = -1001129788700 # TestChannel

while True:
    print('...')
    message  = input('Your Message: ')
    bot_1.send_message(message, channel_id)
    
    while True:
        send_photo = input("Do you want to sent a photo (y/n): ")
        if send_photo == "y":
            path = input("Enter photo path: ")
            if not os.path.isfile(path):
                print("Invalid photo path.")
                continue
            else:
                bot_1.send_photo(path, channel_id)
        elif send_photo == "n":
            break
        else:
            print("Invalid answer. Please enter y or n")
            
    send_msg = input("Do you want to sent another message (y/n): ")
    if send_msg == "y":
        continue
    elif send_msg == "n":
        break
    
print("Goodbye!")