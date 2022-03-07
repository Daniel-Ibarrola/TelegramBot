from bot import telegramBot
import os

bot_1 = telegramBot.test_bot()
bot_1.load_all_groups()
group_id = bot_1.groups["grupo_prueba2"]
# channel_id = -1001129788700 # TestChannel

while True:
    print('...')
    message  = input('Your Message: ')
    bot_1.send_message(message, group_id)
    
    while True:
        send_photo = input("Do you want to sent a photo (y/n): ")
        if send_photo == "y":
            path = input("Enter photo path: ")
            if not os.path.isfile(path):
                print("Invalid photo path.")
                continue
            else:
                bot_1.send_photo(path, group_id)
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