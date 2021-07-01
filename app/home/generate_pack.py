import requests
import time
import ujson
import random

class PackGenerator():

	def __init__(self, set_code):
		self.set_code = set_code
		self.scryfall_API_base = "https://api.scryfall.com"
		self.mythics = []
		self.rares = []
		self.uncommons = []
		self.commons = []
		self.tokens = []
		self.snow_sets = ["khm", "mh1", "c19", "fut", "csp", "ice"]
		self.common_lands = {}

	def reset_fields(self):
		self.set_code = None
		self.mythics = []
		self.rares = []
		self.uncommons = []
		self.commons = []
		self.tokens = []
		self.common_lands = {}
		
	def set_request(self, set_name):
		req = self.scryfall_API_base + "/sets/" + set_name
		time.sleep(5/1000)
		selected_set = requests.get(req)
		set_json_str = selected_set.content.decode('utf8').replace("'", '"')
		set_json = ujson.loads(set_json_str)
		return set_json

	def cards_request(self, set_json):
		has_more = True
		card_jsons = []
		cards_req = set_json["search_uri"]

		while has_more:	
			time.sleep(5/1000)
			response = requests.get(cards_req)
			cards_json_str = response.content.decode('utf8') 
			cards_json = ujson.loads(cards_json_str)
			card_jsons.append(cards_json)

			if not ("has_more" in cards_json):
				has_more = False
			elif "next_page" in cards_json:
				cards_req = cards_json["next_page"]
			else:
				break

		return card_jsons

	def tokens_request(self, set_json):
		cards_req = set_json["search_uri"]
		time.sleep(5/1000)
		cards = requests.get(cards_req)
		cards_json_str = cards.content.decode('utf8')
		cards = ujson.loads(cards_json_str)
		return cards

	def get_common_lands(self, set_code):
		if set_code in self.snow_sets:
			req_uri = self.scryfall_API_base + "/cards/search?q=s%3A{}+t%3Asnow+r%3Acommon+t%3Aland".format(set_code)
		else:
			req_uri = self.scryfall_API_base + "/cards/search?q=s%3A{}+r%3Acommon+t%3Aland".format(set_code)

		response = requests.get(req_uri)
		json_str = response.content.decode('utf8')
		cards = ujson.loads(json_str)
		return cards

	def select_cards(self):
		selected_cards = []
		isMythic = 7

		if isMythic == random.choice([0,1,2,3,4,5,6,7]):
			rare_card = random.choice(self.mythics)
		else:
			rare_card = random.choice(self.rares)

		selected_uncommons = random.sample(self.uncommons, k=3)
		selected_commons = random.sample(self.commons, k=10)
		selected_lands = random.choice(list(self.common_lands.values()))

		selected_cards.append(rare_card)
		selected_cards.extend(selected_uncommons)
		selected_cards.extend(selected_commons)
		selected_cards.extend(selected_lands)

		return selected_cards

	def print_pack(self, pack):
		rares = []
		uncommons = []
		commons = []
		for card in pack:
			if card["rarity"] == "rare" or card["rarity"] == "mythic":
				rares.append(card["name"])
			elif card["rarity"] == "uncommon":
				uncommons.append(card["name"])
			elif card["rarity"] == "common":
				commons.append(card["name"])

		print("Rares: {}\n".format(rares))
		print("Uncommons: {}\n".format(uncommons))
		print("Commons: {}\n".format(commons))

	def get_image_uris(self, pack):
		uri_list = []
		for card in pack:
			if "image_uris" in card.keys():
				uri = card["image_uris"]["normal"]
				uri_list.append(uri)
			elif "card_faces" in card.keys():
				uri = card["card_faces"][0]["image_uris"]["normal"]
				uri_list.append(uri)

		return uri_list

	def print_cards_in_set(self):
		mythic_names = []
		rare_names = []
		uncommon_names = []
		common_names = []
		land_names = []

		for card in self.mythics:
			mythic_names.append(card["name"])
		for card in self.rares:
			rare_names.append(card["name"])
		for card in self.uncommons:
			uncommon_names.append(card["name"])
		for card in self.commons:
			common_names.append(card["name"])

		for card in self.common_lands.keys():
			land_names.append(card)
	
		print("Mythics: {}\n".format(mythic_names))
		print("Rares: {}\n".format(rare_names))
		print("Uncommons: {}\n".format(uncommon_names))
		print("Commons: {}\n".format(common_names))
		print("Common Lands: {}\n".format(land_names))

	def sort_cards(self, card_jsons, lands, token_cards):

		def append_lands(card):
			if card["name"] not in self.common_lands:
				self.common_lands[card["name"]] = [card]
			else:
				self.common_lands[card["name"]].append(card)

		for cards in card_jsons:
			for card in cards["data"]:
				if card["rarity"] == "common" and "land" not in card["type_line"].lower():
					self.commons.append(card)
				elif card["rarity"] == "uncommon":
					self.uncommons.append(card)
				elif card["rarity"] == "rare":
					self.rares.append(card)
				elif card["rarity"] == "mythic":
					self.mythics.append(card)
		
		for card in token_cards:
			self.tokens.append(card)

		for card in lands["data"]:
			if self.set_code.lower() in self.snow_sets and "snow" in card["type_line"].lower():
				append_lands(card)
			else:
				append_lands(card)

	def generate_pack(self, set_code):
		self.set_code = set_code
		set_json = self.set_request(set_code)
		card_jsons = self.cards_request(set_json)
		token_metadata = self.set_request("t" + set_code)
		token_cards = self.cards_request(token_metadata)
		lands = self.get_common_lands(set_code)
		self.sort_cards(card_jsons, lands, token_cards)
		selected_cards = self.select_cards()

		return selected_cards