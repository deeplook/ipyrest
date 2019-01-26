# -*- coding: utf-8 -*-

"""
Tools for ipyrest.
"""

import time
from threading import Thread
from contextlib import closing
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from ipywidgets import Tab, HBox, VBox, Accordion
from flask import Flask


# Only used only during development.
def tree(widget, level=0):
    "Show widget hiararchy as nested tree."

    indent = level * '  '
    klass = widget.__class__
    class_name = klass.__name__
    print(f'{indent}{class_name}')
    if klass in (Tab, HBox, VBox, Accordion):
        for child in widget.children:
            tree(child, level + 1)

            
def find_free_port() -> int:
    "Return a free network port."

    with closing(socket(AF_INET, SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s.getsockname()[1]


def run_flask_app(app: Flask, kwargs: dict, daemon: bool=True) -> None:
    "Run a flask server app inside a thread."

    t = Thread(target=app.run, kwargs=kwargs)
    if daemon:
        t.daemon = True
    t.start()
    time.sleep(1)
