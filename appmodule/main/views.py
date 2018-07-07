from . import main


@main.route('/', methods=['GET'])
def index():
	return 'Just the basic structure for the first commit'