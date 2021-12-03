import telegramBot.bot.bot
import telegramBot.ftp.ftpserver
import telegramBot.utils.utils
import telegramBot.utils.exceptions

def test_import():

    bot = telegramBot.bot.bot.telegramBot("my-bot", "123efdsa21")
    assert isinstance(bot, telegramBot.bot.bot.telegramBot )