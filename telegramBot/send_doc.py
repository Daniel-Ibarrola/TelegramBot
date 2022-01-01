from bot.bot import telegramBot
import utils.utils as utils
import os
import sys

class MissingParametersError(ValueError):
    pass

def main():

    if getattr(sys, "frozen", False):
        this_dir = os.path.dirname(sys.executable)
    else:
        this_dir = os.path.abspath(os.path.dirname(__file__))
        
    groups_file = os.path.join(this_dir, "data\chats.txt")
    tokens_file = os.path.join(this_dir, "data", "tokens.txt")

    if len(sys.argv) < 3:
        raise MissingParametersError(f"La ruta de la imagen y el nombre del grupo se deben pasar como argumentos al programa.") 

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo con ruta {file_path} no fue encontrado.")
    
    valid_groups = utils.get_valid_groups(groups_file=groups_file)
    group_name = utils.validate_group(sys.argv[2], list(valid_groups.keys()))
    
    group_id = valid_groups[group_name].group_id
    bot_name = valid_groups[group_name].bot_name

    _, token = telegramBot.read_token(bot_name, token_file=tokens_file)

    bot = telegramBot(bot_name, token)
    bot.send_photo(file_path, group_id, print_res=True)

if __name__=="__main__":
    main()