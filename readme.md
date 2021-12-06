# Telegram ChatBot

Telegram bot to send messages in real time.

## Instalation

First create a conda environment from the requiremnts.yaml file located in telegramBot/devtools:

```bash
cd telegramBot/devtools
conda env create --file requirements.yaml
```
Then download the data files and put them in telegramBot/data (create the directory if necessary). 

Now the program can be run from the command line (first go to the directory where main.py is located):

```bash
python main.py 
```
Alternatively an executable file can be created.

## How to create an executable 

First create a conda environment from the requirements.yaml file. Then go to the folder where 
setup.py is installed and generate the executable with the following command: 

```bash
python setup.py install
```
A build and a dist directory will be created. Delete the build directory. Then, copy the following folders into the dist
directory: bot, ftp, utils, data, as well as the __init__.py located in telegramBot.  

## Passing arguments to the program
The program accepts two arguments which are port number and the name of the telegram group where the 
messages will be send. For example if the program is run from a command line and the desired port is
13385 and the group name is "informacion cires", the following command can be used:

```bash
python main.py 13385 "informacion cires"
```
Alternatively the extra arguments can be passed from a direct access to the executable. The casing of
the group name doesn't matter.

The default port is 13385 and the default group is SASMEX.
