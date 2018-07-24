from flask import Flask, session, render_template
from flask.ext.script import Manager, Shell
from appmodule import create_app
from threading import Lock
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import json
import flask
import time
import os 
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from os.path import abspath, dirname

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = create_app()
app.config['SECRET_KEY'] = 'secret!'
manager = Manager(app)



#manager = Manager(app


if __name__ == '__main__':
	manager.run()