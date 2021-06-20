from flask import Flask, render_template, request, Blueprint
views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/', methods=['GET'])
def dropdown():
    sets = ['STX', 'KHM', 'ZNR', 'M21']
    return render_template('home.html', sets=sets)
