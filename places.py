
import handler
import urllib2
import jinja2
import json

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

			
class placesHandler(handler.Handler):

	url_places = "http://api.outpost.travel/placeRentals"

	def get(self):
		if self.request.get('id'):
			self.render_id(self.request.get('id'))
		elif self.request.get('city'):
			self.render_city(self.request.get('city'))
		elif self.request.get('sort'):
			self.render_sort(self.request.get('sort'))
		else:
			self.render_all()
			


	def render_all(self):
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))
		self.render("places_list.html", places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])

	def render_city(self, city):
		url = self.url_places + "?city=" + city
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))
		self.render("places_list.html", city=city, places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])

	def render_sort(self, sort):
		if self.request.get('sortMethod'):
			sortMethod = self.request.get('sortMethod')
		else:
			sortMethod = 'ascending'
		url = self.url_places + "?sort=" + sort + "?sortMethod=" + sortMethod
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))
		self.render("places_list.html", sort=sort, places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])


	def render_id(self, place_id):
		url = self.url_places + "?pid=" + place_id
		plain = self.process(url)
		jSon = json.loads(plain)
		if len(jSon["items"]) > 0:
			self.render("place.html", place=self.jSonToPlace(jSon["items"][0]))
		else:
			self.render("place.html", error="Cet ID est introuvable")

	def process(self, url):
		req = urllib2.urlopen(url)
		return req.read()

	def jSonToPlace(self, item):
		myPlace = place()
		myPlace.photos = []
		myPlace.amenities = []
		myPlace.unavailable = []
		myPlace.origin = item["origin"]
		myPlace.minimum_stay_night = item["minimumStayNight"]
		myPlace.price_per = item["pricePer"]
		myPlace.bed_count = item["bedCount"]
		myPlace.occupancy = item["occupancy"]
		myPlace.provider = item["provider"]
		myPlace.description = item["description"]
		myPlace.pid = item["pid"]
		myPlace.price = item["price"]
		myPlace.link = item["link"]
		myPlace.country = item["country"]
		myPlace.nid = item["nid"]
		myPlace.bathroomcount = item["bathroomCount"]
		myPlace.bedroomcount = item["bedroomCount"]
		myPlace.heading = item["heading"]
		myPlace.room_type = item["type"]["roomType"]
		myPlace.room_type_alias = item["typeAlias"]["roomType"]
		myPlace.prop_type = item["type"]["propType"]
		myPlace.prop_type_alias = item["typeAlias"]["propType"]
		myPlace.latitude = item["latLng"][0]
		myPlace.longitude = item["latLng"][1]
		for amenity in item["amenities"]:
			myPlace.amenities.append(amenity)
		for unavlbl in item["unavailable"]:
			myPlace.unavailable.append(unavlbl)
		for photo in item["photos"]:
			myPlace.photos.append(photo["url"])
		return myPlace



class place:
	origin=""
	minimum_stay_night=""
	price_per=""
	bed_count=""
	occupancy=""
	provider=""
	description=""
	country=""
	link=""
	pid=""
	price=""
	nid=""
	bathroomcount=""
	bedroomcount=""
	heading=""
	room_type=""
	room_type_alias=""
	prop_type=""
	prop_type_alias=""
	latitude=""
	longitude=""
	unavailable=[]
	amenities=[]
	photos=[]
	



