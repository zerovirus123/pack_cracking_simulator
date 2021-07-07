import time
import random
import requests_cache

class PackGenerator():

	def __init__(self, set_code):
		self.set_code = set_code.lower()
		self.scryfall_API_base = "https://api.scryfall.com"
		self.mythics = []
		self.rares = []
		self.uncommons = []
		self.commons = []
		self.tokens = []
		self.snow_sets = ["khm", "mh1", "c19", "fut", "csp", "ice"]
		self.common_lands = {}
		self.request_session = requests_cache.CachedSession('session_cache')
		self.get_set_cards()

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
		response = self.request_session.get(req)
		set_json = response.json()
		return set_json

	def cards_request(self, set_json):
		has_more = True
		card_jsons = []
		req = set_json["search_uri"]

		while has_more:	
			time.sleep(5/1000)
			response = self.request_session.get(req)
			cards_json = response.json() 
			card_jsons.append(cards_json)

			if not ("has_more" in cards_json):
				has_more = False
			elif "next_page" in cards_json:
				req = cards_json["next_page"]
			else:
				break

		return card_jsons

	def tokens_request(self, set_json):
		req = set_json["search_uri"]
		time.sleep(5/1000)
		response = self.request_session.get(req)
		cards = response.json()
		return cards

	def get_common_lands(self):
		if self.set_code in self.snow_sets:
			req = self.scryfall_API_base + "/cards/search?q=s%3A{}+t%3Asnow+r%3Acommon+t%3Aland".format(self.set_code)
		else:
			req = self.scryfall_API_base + "/cards/search?q=s%3A{}+r%3Acommon+t%3Aland".format(self.set_code)

		response = self.request_session.get(req)
		cards = response.json()
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
		selected_tokens = [random.choice(self.tokens)]

		selected_cards.append(rare_card)
		selected_cards.extend(selected_uncommons)
		selected_cards.extend(selected_commons)
		selected_cards.extend(selected_lands)
		selected_cards.extend(selected_tokens)

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
			double_face_uris = {}
			if "image_uris" in card.keys():
				uri = card["image_uris"]["normal"]
				uri_list.append(uri)
			elif "card_faces" in card.keys():
				uri_front = card["card_faces"][0]["image_uris"]["normal"]
				uri_back = card["card_faces"][1]["image_uris"]["normal"]
				double_face_uris["front_uri"] = uri_front
				double_face_uris["back_uri"] = uri_back
				uri_list.append(double_face_uris)

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
				if "promo_types" not in card:
					if card["rarity"] == "common" and "land" not in card["type_line"].lower():
						self.commons.append(card)
					elif card["rarity"] == "uncommon":
						self.uncommons.append(card)
					elif card["rarity"] == "rare":
						self.rares.append(card)
					elif card["rarity"] == "mythic":
						self.mythics.append(card)
		
		for cards in token_cards:
			for card in cards["data"]:
				self.tokens.append(card)

		for card in lands["data"]:
			if self.set_code in self.snow_sets and "snow" in card["type_line"].lower():
				append_lands(card)
			else:
				append_lands(card)

	def get_set_cards(self):
		set_json = self.set_request(self.set_code)
		card_jsons = self.cards_request(set_json)
		token_metadata = self.set_request("t" + self.set_code)
		token_cards = self.cards_request(token_metadata)
		lands = self.get_common_lands()
		self.sort_cards(card_jsons, lands, token_cards)

	def generate_pack(self):
		selected_cards = self.select_cards()
		return selected_cards
