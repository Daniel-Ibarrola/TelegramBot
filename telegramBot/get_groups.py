from bot.bot import telegramBot, NoUpdatesError
from utils.exceptions import InvalidBotName
import os
import sys

def main():

    if getattr(sys, "frozen", False):
        this_dir = os.path.dirname(sys.executable)
    else:
        this_dir = os.path.abspath(os.path.dirname(__file__))

    tokens_file = os.path.join(this_dir, "data", "tokens.txt")

    bots = telegramBot.get_bot_dictionary(token_file=tokens_file)
    names = list(bots.keys())

    print("Obtener actualizaciones para bot de telegram.")
    print(f"Se detectaron los siguientes bots: {names}")

    while True:
        bot_name = input("Ingrese nombre del bot: ")
        if bot_name not in bots.keys():
            print(f"Bot invalido. Elegir uno de los siguientes bots: {names}")
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
    file_name = os.path.join(this_dir, f"{bot.name}_grupos.txt")
    with open(file_name, "w") as fp:
        for gr, id in bot.groups.items():
            line = f"Grupo: {gr} ID: {id}\n"
            fp.write(line)
            print(line)
    
    print(f"Grupos guardados en archivo {file_name}")

if __name__=="__main__":
    main()
