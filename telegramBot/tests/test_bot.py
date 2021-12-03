from telegramBot.bot.bot import telegramBot

def test_read_token():
    name, token = telegramBot.read_token("cires_bot", token_file="./tests/data/mock-tokens.txt")
    assert name == "cires_bot"
    assert token == "1234567:ABCdefghijk"
    
    name, token = telegramBot.read_token("my_assistant", token_file="./tests/data/mock-tokens.txt")
    assert name == "my_assistant"
    assert token == "89101112:LMNopqrst"
    
    name, token = telegramBot.read_token("test_bot", token_file="./tests/data/mock-tokens.txt")
    assert name == "test_bot"
    assert token == "13141516:VWXyzabcd" 

def test_bot_constructors():
    
    bot = telegramBot.cires_bot(token_file="./tests/data/mock-tokens.txt")
    assert bot.name == "cires_bot"
    assert bot.base_url == "https://api.telegram.org/bot1234567:ABCdefghijk/"
    
    bot = telegramBot.test_bot(token_file="./tests/data/mock-tokens.txt")
    assert bot.name == "test_bot"
    assert bot.base_url == "https://api.telegram.org/bot13141516:VWXyzabcd/"
    
    bot = telegramBot.myassistant_bot(token_file="./tests/data/mock-tokens.txt")
    assert bot.name == "my_assistant"
    assert bot.base_url == "https://api.telegram.org/bot89101112:LMNopqrst/"
    

