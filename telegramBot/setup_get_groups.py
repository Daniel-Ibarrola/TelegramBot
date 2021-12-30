## Setup file to create an executable for the main.py program using py2exe.

from distutils.core import setup
import py2exe

setup_dict = dict(
    windows = [{'script': "get_groups.py",}],
)

setup(**setup_dict)

