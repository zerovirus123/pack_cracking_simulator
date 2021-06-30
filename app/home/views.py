from flask import Flask, render_template, request, Blueprint
import requests
import time
import ujson

views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)
app = Flask(__name__)

sets = ['STX', 'KHM', 'ZNR', 'M21']
scryfall_API_base = "https://api.scryfall.com"

@home_blueprint.route('/', methods=['GET'])
def dropdown():
    return render_template('home.html', sets=sets)

@home_blueprint.route('/get-set/', methods=['POST'])
def get_set():
	if request.method == "POST":
		selected_set = request.form["set-select"]
		req = scryfall_API_base + "/sets/" + selected_set
		time.sleep(5/1000)
		selected_set = requests.get(req)
		set_json_str = selected_set.content.decode('utf8').replace("'", '"')
		set_json = ujson.loads(set_json_str)
		return render_template("home.html", sets=sets, set_icon=set_json["icon_svg_uri"])

@home_blueprint.route('/generate-pack/', methods=['POST'])
def generate_pack():
	if request.method == "POST":
		
		
		
		pass