from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
	app = Flask(__name__)
	app.config['DEBUG'] = True
	bootstrap = Bootstrap(app)

# Create the main blueprint
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app