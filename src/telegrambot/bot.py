import abc


class AbstractBot(abc.ABC):
    pass


class TelegramBot(AbstractBot):
    """ Class to interact with the telegram bot API.
    """
    pass


class TestBot(AbstractBot):
    """ Class used for testing purposes. Doesn't send requests
        to telegram API.
    """
    pass
