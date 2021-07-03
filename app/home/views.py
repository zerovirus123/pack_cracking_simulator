from flask import Flask, render_template, request, Blueprint
import requests
import time
from .generate_pack import PackGenerator

views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)

sets = ['STX', 'KHM', 'ZNR', 'M21', 'ISD']
set_code = None
image_uris = []
scryfall_API_base = "https://api.scryfall.com"

@home_blueprint.route('/', methods=['GET'])
def dropdown():
    return render_template('home.html', sets=sets)

@home_blueprint.route('/get-set/', methods=['POST'])
def get_set():
	if request.method == "POST":
		image_uris = []
		set_code = request.form["set-select"]
		req = scryfall_API_base + "/sets/" + set_code
		time.sleep(5/1000)
		response = requests.get(req)
		set_json = response.json()
		generator = PackGenerator(set_code)
		pack = generator.generate_pack()
		image_uris = generator.get_image_uris(pack)
		return render_template("home.html", sets=sets, set_icon=set_json["icon_svg_uri"], image_uris=image_uris, selected_set=set_code)
