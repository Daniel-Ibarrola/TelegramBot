from bot.bot import telegramBot, NoUpdatesError
from utils.exceptions import InvalidBotName


def main():

    bots = telegramBot.get_bot_dictionary()
    names = list(bots.keys())

    while True:
        bot_name = input("Enter bot name: ")
        if bot_name not in bots.keys():
            print(f"Bot invalido. Elegir uno de los sugioentes bots: {names}")
        else:
            break

    try:
        token = bots[bot_name]
    except KeyError:
        raise InvalidBotName(f"{bot_name} no es un nombre de bot valido.")
   
    bot = telegramBot(bot_name,token)

    try:
        bot.get_groups_dictionary()
    except NoUpdatesError:
        print(f"No hay actualizaciones para {bot.name}. Intente otra vez más tarde.")
        return
    
    print(f"Se encontraron actualizaciones para los siguientes grupos:\n")
    with open(f"{bot.name}_grupos.txt", "w") as fp:
        for gr, id in bot.groups.items():
            line = f"Grupo: {gr} ID: {id}\n"
            fp.write(line)
            print(line)
    

if __name__=="__main__":
    main()
