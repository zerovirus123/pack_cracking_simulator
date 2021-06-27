from flask import Flask, render_template, request, Blueprint
views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)
app = Flask(__name__)

sets = ['STX', 'KHM', 'ZNR', 'M21']

@home_blueprint.route('/', methods=['GET'])
def dropdown():
    
    return render_template('home.html', sets=sets)

@home_blueprint.route('/home/generate-pack/', methods=['POST'])
def generate_pack():
	if request.method == "POST":
		selected_set = request.form["set-select"]

		return selected_set