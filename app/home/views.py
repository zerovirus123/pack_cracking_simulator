from flask import Flask, render_template, request, Blueprint
views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)

selected_set = None

@home_blueprint.route('/', methods=['GET'])
def dropdown():
    sets = ['STX', 'KHM', 'ZNR', 'M21']
    return render_template('home.html', sets=sets)

@views.route('/generate-pack/<set>', methods=['GET', 'POST'])
def generate_pack():

    if request.method == 'POST':
        print(set)