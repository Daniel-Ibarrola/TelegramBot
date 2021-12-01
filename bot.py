import requests
import json

class telegramBot():

    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.groups = {}
        
    @classmethod
    def cires_bot(cls, token_file="./tokens.txt"):
        name, token = telegramBot.read_token("cires_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def test_bot(cls, token_file="./tokens.txt"):
        name, token = telegramBot.read_token("test_bot", token_file)
        return cls(name, token)
    
    @classmethod
    def myassistant_bot(cls, token_file="./tokens.txt"):
        name, token = telegramBot.read_token("PulpoalaDiabla_bot", token_file)
        return cls(name, token)
    
    @staticmethod
    def read_token(bot_name, token_file="./tokens.txt"):
        """ Read a token from a text file.
            
        """
        with open(token_file, "r") as fh:
            for line in fh:
                if line.startswith(bot_name):
                    pieces = line.split(" ")
                    name = pieces[0].rstrip()
                    token = pieces[-1].rstrip()
                    return name, token
    
    def get_updates(self, offset=None):
        url = self.base_url + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        res = requests.get(url)
        if res.status_code != 200:
            raise IOError("Couldn't get updates")
        
        return json.loads(res.content)

    def get_groups_dictionary(self):
        updates = self.get_updates()
        for update in updates["result"]:
            try:
                group_name = update["message"]["chat"]["title"]
                group_id = update["message"]["chat"]["id"]
                self.groups[group_name] = group_id
            except:
                pass

    def get_bot_info(self):
        url = self.base_url + "getMe"
        res = requests.get(url)
        return json.loads(res.content)
            
    def send_message(self, msg, chat_id):
        if not isinstance(msg, str):
            raise TypeError("Mesage must be of type string")
        if not msg:
            raise ValueError("Message must not be an empty string")
    
        url = self.base_url + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        res = requests.get(url)
        
        if res.status_code != 200:
            print(f"Failed to send message. Status code: {res.status_code}")

    def send_photo(self, photo_path, chat_id, caption=None):
        url = self.base_url + "sendPhoto?chat_id={}".format(chat_id)
        if caption:
            if not isinstance(caption, str):
                raise TypeError("Caption must be of type str")
            url += "&caption={}".format(caption)
        photo = {'photo': open(photo_path, 'rb')}
        res = requests.post(url, files=photo)
        
        if res.status_code != 200:
            print(f"Failed to send photo. Status code: {res.status_code}")

    def send_document(self, doc_path, chat_id, caption=None):
        url = self.base_url + "sendDocument?chat_id={}".format(chat_id)
        if caption:
            if not isinstance(caption, str):
                raise TypeError("Caption must be of type str")
            url += "&caption={}".format(caption)
        files = {'document': open(doc_path, 'rb')}
        res = requests.post(url, files=files)
        
        if res.status_code != 200:
            print(f"Failed to send document. Status code: {res.status_code}")
    