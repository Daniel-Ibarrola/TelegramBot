import bot.bot as telbot
import ftp.ftpserver
import utils.utils
import utils.exceptions

def test_import():

    bot = telbot.telegramBot("my-bot", "123efdsa21")
    assert isinstance(bot, bot.bot.telegramBot )