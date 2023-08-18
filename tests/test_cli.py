import os
import subprocess


env = os.environ.copy()
env["config"] = "dev"


def test_send_message():
    result = subprocess.run(
        ["telegrambot", "message",
         "-b", "MyTestBot",
         "-c", "MyTestChat",
         "-f", "./bot.csv",
         "-cf", "./chats.csv",
         "-m", "hello world"
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert result.stdout == "Message sent successfully: hello world"


def test_send_photo():
    result = subprocess.run(
        ["telegrambot", "photo",
         "-b", "MyTestBot",
         "-c", "MyTestChat",
         "-f", "./bot.csv",
         "-cf", "./chats.csv",
         "-p", "./dog.jpg",
         "-c", "Cute dog"
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert result.stdout == "Photo sent successfully: ./dog.jpg"


def test_get_updates():
    result = subprocess.run(
        ["telegrambot", "updates",
         "-b", "MyTestBot",
         "-f", "./bot.csv",
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert result.stdout == "Bot updates: "
