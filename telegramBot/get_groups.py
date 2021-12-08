from bot.bot import telegramBot, NoUpdatesError
from utils.exceptions import InvalidBotName


def main():
    bot_name = input("Enter bot name: ")
    bot_dict = telegramBot.get_bot_dictionary()
    try:
        bot = telegramBot(bot_name, bot_dict[bot_name])
    except KeyError:
        raise InvalidBotName(f"{bot_name} is not a valid bot name")

    #print(bot.base_url)
    try:
        bot.get_groups_dictionary()
    except NoUpdatesError:
        print(f"No updates for {bot.name}. Cannot get groups id's. Try again later")
        return
    
    print(f"{bot.name} belongs to the following groups:\n")
    for gr, id in bot.groups.items():
        print(f"Grupo: {gr} ID: {id}")
    

if __name__=="__main__":
    main()
