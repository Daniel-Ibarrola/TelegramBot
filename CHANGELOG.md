# Changelog

## v0.2.4

1. TelegramBot encodes text messages to prevent data loss.
2. Url is a parameter with default value for TelegramBot.
3. Formatted code with black.


## v0.2.3
`TestBot.send_photo` does not open files.

## v0.2.2
Added build to dependencies, for CD action.

## v0.2.1
Fixed script error on pyproject.toml

## v0.2.0
Project name is ciresbot on pypi. Import works as usual.
Can install from pip.

## v0.1.2
TestBot stores responses 

## v0.1.1
- Fixed bugs in tests in TestGetChatID. 
- Dev requirements includes common as well.

## v0.1.0

Initial release. Can send messages and photos through Telegram.

### Features

#### Python module
- Python module has its main class `TelegramBot`, that implements the interaction
with the Telegram Bot API.
- Util functions to read bot tokens, and Telegram chat ids from files.

#### Command line tool
- Can send messages, and photos with through the command line, as well as get
the latest bot updates.
