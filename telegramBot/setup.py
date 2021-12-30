## Setup file to create an executable for the main.py program using py2exe.

from distutils.core import setup
import py2exe

setup_dict = dict(
    windows = [{'script': "main.py",
                "icon_resources": [(1, "bot.ico")]}],
)

setup(**setup_dict)
setup(**setup_dict)
