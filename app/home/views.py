from flask import Flask, render_template, request, Blueprint
import requests
import time
import ujson
from .generate_pack import PackGenerator

views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)
app = Flask(__name__)

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
		selected_set = set_code
		req = scryfall_API_base + "/sets/" + selected_set
		time.sleep(5/1000)
		selected_set = requests.get(req)
		set_json_str = selected_set.content.decode('utf8').replace("'", '"')
		set_json = ujson.loads(set_json_str)
		generator = PackGenerator()
		pack = generator.generate_pack(set_code)
		# generator.print_pack(pack)
		image_uris = generator.get_image_uris(pack)
		return render_template("home.html", sets=sets, set_icon=set_json["icon_svg_uri"], image_uris=image_uris)

@home_blueprint.route('/generate-pack/', methods=['GET', 'POST'])
def generate_pack():
	generator = PackGenerator()
	pack = generator.generate_packs(set_code)
	print(pack)
	return pack