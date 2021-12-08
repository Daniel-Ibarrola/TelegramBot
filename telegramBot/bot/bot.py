import requests
import json

class NoUpdatesError(ValueError):
    pass

class telegramBot():
    """ Class to work with Telegram bots.
    
        Parameters
        ----------
        name : str
            The username of the bot.
        
        token : str
            The token of the bot assigned by Telegram. 
            
        Variables
        ---------
        name : str
            The username of the bot.
        
        token : str
            The token of the bot assigned by Telegram. 
        
        base_url : str
            The url of the telegram bot api including the bot token.
            
        groups : dict
            A dictionary with the name an ids of the groups which the bot is part of.
        
    """
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.groups = {}
        
    @classmethod
    def cires_bot(cls, token_file="./data/tokens.txt"):
        """ Class method to create a bot with the username ciresBot.
        
            Parameters
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
        """
        name, token = telegramBot.read_token("cires_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def cires_bot_2(cls, token_file="./data/tokens.txt"):
        """ Class method to create a bot with the username CiresBot2.
        
            Parameters
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
        """
        name, token = telegramBot.read_token("cires_2_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def cires_bot_3(cls, token_file="./data/tokens.txt"):
        """ Class method to create a bot with the username CiresBot3.
        
            Parameters
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
        """
        name, token = telegramBot.read_token("cires_3_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def test_bot(cls, token_file="./data/tokens.txt"):
        """ Class method to create a bot with the usernmae Testbot.
        
            Parameters
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
        """
        name, token = telegramBot.read_token("test_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def myassistant_bot(cls, token_file="./data/tokens.txt"):
        """ Class method to create a bot with the username MyAssistant.
            
            Parameters  
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
        """
        name, token = telegramBot.read_token("my_assistant", token_file)
        return cls(name, token)
    
    @staticmethod
    def read_token(bot_name, token_file="./data/tokens.txt"):
        """ Read a token from a text file.
            
            Parameters
            ----------
            bot_name : str
                The name of the bot in the token file.
            
            token_file : str
                Path to the file containing the bots and tokens names.
                
            Returns
            -------
            name : str
                The name of the bot
            
            token : str
                The bot token.    
        """
        with open(token_file, "r") as fh:
            for line in fh:
                if line.startswith(bot_name):
                    pieces = line.split(" ")
                    name = pieces[0].rstrip()
                    token = pieces[-1].rstrip()
                    return name, token
    
    @staticmethod
    def get_bot_dictionary(token_file="./data/tokens.txt"):
        """ Get a dictionary with valid bot names and its tokens.
        
            Parameters
            ----------
            token_file : str
                Path to the file containing the bots and tokens names.
                
            Returns
            -------
            bots : dict
                Dictionary with bot names ans keys and tokens as values.

        """
        bots = {}
        with open(token_file, "r") as fh:
            for line in fh:
                name_and_token = line.split()
                bots[name_and_token[0]] = name_and_token[1]
        return bots

    def get_updates(self, offset=None):
        """ Get updates for the current bot. 
        
        """
        url = self.base_url + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        res = requests.get(url)
        if res.status_code != 200:
            raise IOError("Couldn't get updates")

        return json.loads(res.content)

    def get_groups_dictionary(self):
        """ Get a dictionary with the names and ids of the groups to which this bot belongs to.
        """
        updates = self.get_updates()
        if len(updates["result"]) == 0:
            raise NoUpdatesError()
        for update in updates["result"]:
            try:
                group_name = update["message"]["chat"]["title"]
                group_id = update["message"]["chat"]["id"]
                self.groups[group_name] = group_id
            except:
                pass

    def get_bot_info(self):
        """ Get basic info of the current bot.
        
            Returns
            -------
            dict
                Dictionary with bot info.
        """
        url = self.base_url + "getMe"
        res = requests.get(url)
        return json.loads(res.content)
            
    def send_message(self, msg, chat_id):
        """ Send a message with the bot.

            Parameters
            ----------
            msg : str
                The message that will be send.
            
            chat_id : int or str
                The id of the chat where the message will be send-
            
        """
        if not isinstance(msg, str):
            raise TypeError("Mesage must be of type string")
        if not msg:
            raise ValueError("Message must not be an empty string")
    
        url = self.base_url + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        res = requests.get(url)
        
        if res.status_code != 200:
            print(f"Failed to send message. Status code: {res.status_code}")

    def send_photo(self, photo_path, chat_id, caption=""):
        """ Send a photo with the bot.

            Parameters
            ----------
            photo_path : str
                Path to the photo that will be send.
            
            chat_id : int or str
                The id of the chat where the message will be send.
            
            caption : str, optional
                The caption of the photo.
            
        """
        url = self.base_url + "sendPhoto?chat_id={}".format(chat_id)
        if caption:
            if not isinstance(caption, str):
                raise TypeError("Caption must be of type str")
            url += "&caption={}".format(caption)
        photo = {'photo': open(photo_path, 'rb')}
        res = requests.post(url, files=photo)
        
        if res.status_code != 200:
            print(f"Failed to send photo. Status code: {res.status_code}")

    def send_document(self, doc_path, chat_id, caption=""):
        """ Send a document with the bot.

            Parameters
            ----------
            doc_path : str
                Path to the document that will be send.
            
            chat_id : int or str
                The id of the chat where the message will be send.
            
            caption : str, optional
                The caption of the document.
            
        """
        url = self.base_url + "sendDocument?chat_id={}".format(chat_id)
        if caption:
            if not isinstance(caption, str):
                raise TypeError("Caption must be of type str")
            url += "&caption={}".format(caption)
        files = {'document': open(doc_path, 'rb')}
        res = requests.post(url, files=files)
        
        if res.status_code != 200:
            print(f"Failed to send document. Status code: {res.status_code}")
    