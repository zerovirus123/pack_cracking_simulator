from flask import Flask, render_template, request, Blueprint
import requests_cache
import time
from .generate_pack import PackGenerator
from datetime import timedelta

views = Flask(__name__)
views.debug = True

home_blueprint = Blueprint('home', __name__)

sets = []
scryfall_API_base = "https://api.scryfall.com"

@home_blueprint.route('/', methods=['GET'])
def dropdown():
	global sets
	request_session = requests_cache.CachedSession('session_cache', expire_after=timedelta(days=1))
	req = scryfall_API_base + "/sets/"
	time.sleep(5/1000)
	response = request_session.get(req)
	set_json = response.json()

	for set in set_json["data"]:
		if set["set_type"] == "expansion" or set["set_type"] == "draft_innovation" or set["set_type"] == "masters":
			sets.append(set["code"])

	return render_template('home.html', sets=sets)

@home_blueprint.route('/get-set/', methods=['POST'])
def get_set():
	if request.method == "POST":
		image_uris = []
		set_code = request.form["set-select"]
		time.sleep(5/1000)
		generator = PackGenerator(set_code)
		pack = generator.generate_pack()
		image_uris = generator.get_image_uris(pack)
		set_json = generator.set_request(set_code)
		return render_template("home.html", sets=sets, set_icon=set_json["icon_svg_uri"], image_uris=image_uris, selected_set="Select a Set")
