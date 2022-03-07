import os

def send_logs_telegram(bot, error_message, group_id):
    """ Send logs and error messages through telegram. 

        Parameters
        ----------
        bot : bot.telegramBot
            The bot to send messages with
        
        error_message : str
            The error message that will be sent.
        
        group_id : int
            Id of the group that logs and error messages will be sent.

    """

    status_code = bot.send_message(error_message, group_id)
    if status_code != 200:
        print(f"Failed to send error message. Status code {status_code}")

    # Search for log files and send them
    log_files = []
    for file in os.listdir("./"):
        if file.endswith(".log"):
            log_files.append(file)

    if len(log_files) > 0:
        for log in log_files:
            status_code = bot.send_document(log, group_id)
            if status_code != 200:
                print(f"Failed to send log file. Status code {status_code}")