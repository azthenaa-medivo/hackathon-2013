
import handler
import urllib2
import jinja2
import json

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

			
class placesHandler(handler.Handler):

	url_places = "http://api.outpost.travel/placeRentals"

	def get(self):
		self.render_all()

	def render_all(self):
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = self.jSonToList(jSon)
		self.render("places.html", places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])

	def process(self, url):
		req = urllib2.urlopen(url)
		return req.read()

	def jSonToList(self, jSon):
		res = []
		for item in jSon["items"]:
			place = places()
			place.origin = item["origin"]
			place.minimum_stay_night = item["minimumStayNight"]
			place.price_per = item["pricePer"]
			place.bed_count = item["bedCount"]
			place.occupancy = item["occupancy"]
			place.provider = item["provider"]
			place.description = item["description"]
			place.pid = item["pid"]
			place.price = item["price"]
			place.link = item["link"]
			place.country = item["country"]
			place.nid = item["nid"]
			place.bathroomcount = item["bathroomCount"]
			place.bedroomcount = item["bedroomCount"]
			place.heading = item["heading"]
			place.room_type = item["type"]["roomType"]
			place.room_type_alias = item["typeAlias"]["roomType"]
			place.prop_type = item["type"]["propType"]
			place.prop_type_alias = item["typeAlias"]["propType"]
			place.latitude = item["latLng"][0]
			place.longitude = item["latLng"][1]
			for amenity in item["amenities"]:
				place.amenities.append(amenity)
			for unavlbl in item["unavailable"]:
				place.unavailable.append(unavlbl)
			for photo in item["photos"]:
				place.photos.append(photo["url"])
			res.append(place)
		return res



class places:
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
	



