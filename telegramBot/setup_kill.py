## Setup file to create an executable for the kill.py program using py2exe.

from distutils.core import setup
import py2exe

setup_dict = dict(
    windows = [{'script': "kill.py"}],
)

setup(**setup_dict)