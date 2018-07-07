from flask import Flask
from flask.ext.script import Manager, Shell
from appmodule import create_app

app = create_app()

manager = Manager(app)


if __name__ == '__main__':
	manager.run()