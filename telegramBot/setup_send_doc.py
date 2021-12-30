## Setup file to create an executable for the send_doc.py program using py2exe.

from distutils.core import setup
import py2exe

setup_dict = dict(
    windows = [{'script': "send_doc.py"}],
)

setup(**setup_dict)

