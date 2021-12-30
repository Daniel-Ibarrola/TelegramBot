from bot.bot import telegramBot
import utils.utils as utils
import os
import sys

class MissingParametersError(ValueError):
    pass

def main():

    if len(sys.argv) < 3:
        raise MissingParametersError(f"The file path and the group name must be passed") 

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File with path {file_path} couldn't be found")
    
    valid_groups = utils.get_valid_groups()
    group_name = utils.validate_group(sys.argv[2], list(valid_groups.keys()))
    
    group_id = valid_groups[group_name].group_id
    bot_name = valid_groups[group_name].bot_name

    _, token = telegramBot.read_token(bot_name)

    bot = telegramBot(bot_name, token)
    bot.send_photo(file_path, group_id, print_res=True)

if __name__=="__main__":
    main()