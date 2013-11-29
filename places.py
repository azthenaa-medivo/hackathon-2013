
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
		elif self.request.get('page'):
			self.render_page(self.request.get('page'))
		else:
			self.render_all()
		
	def post(self):
		if self.request.get('citySearch'):
			self.render_city(self.request.get('citySearch'))


	def render_all(self):
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))
		self.render("places_list.html", places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])

	def render_city(self, city):
		url = self.url_places + "?city=" + city.replace(' ', '+').replace('	', '+')
		plain = self.process(self.url_places)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))
		self.render("places_list.html", city=city, places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])

	def render_page(self, page_s):
		page = int(page_s)

		url = self.url_places + "?page=" + str(page)
		plain = self.process(url)
		jSon = json.loads(plain)
		places_list = []
		for item in jSon["items"]:
			places_list.append(self.jSonToPlace(item))

		maxPage = int(jSon["totalPages"])
		page_links = ""

		if page > 1:
			page_links += " <a href='/_places?page=1' >1</a> "
		if page > 3:
			page_links += " ... <a href='/_places?page="+ str(page-2) +"' >"+ str(page-2) +"</a> "
		if page > 2:
			page_links += " <a href='/_places?page="+ str(page-1) +"' >"+ str(page-1) +"</a> "
		page_links += " " + str(page) + " "
		if page < (maxPage - 1) :
			page_links += " <a href='/_places?page="+ str(page+1) +"' >"+ str(page+1) +"</a> "
		if page < (maxPage - 2) :
			page_links += " <a href='/_places?page="+ str(page+2) +"' >"+ str(page+2) +"</a> "
		if page < (maxPage - 3) :
			page_links += " <a href='/_places?page="+ str(page+3) +"' >"+ str(page+3) +"</a> "
		if page < (maxPage - 10) :
			page_links += " ... <a href='/_places?page="+ str(page+10) +"' >"+ str(page+10) +"</a> "
		if page < (maxPage - 20) :
			page_links += " ... <a href='/_places?page="+ str(page+20) +"' >"+ str(page+20) +"</a> "
		if page < (maxPage - 50) :
			page_links += " ... <a href='/_places?page="+ str(page+50) +"' >"+ str(page+50) +"</a> "
		page_links += " ... <a href='/_places?page="+ str(maxPage) +"' >"+ str(maxPage) +"</a> "
		
		self.render("places_list.html", pageLinks=page_links, places_list=places_list, page=jSon["page"], total_pages=jSon["totalPages"], total_results=jSon["totalResults"])


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
		if "origin" in item : myPlace.origin = item["origin"]
		if "minimumStayNight"  in item : myPlace.minimum_stay_night = item["minimumStayNight"]
		if "pricePer"  in item : myPlace.price_per = item["pricePer"]
		if "bedCount"  in item : myPlace.bed_count = item["bedCount"]
		if "occupancy"  in item : myPlace.occupancy = item["occupancy"]
		if "provider"  in item : myPlace.provider = item["provider"]
		if "description"  in item : myPlace.description = item["description"]
		if "pid"  in item : myPlace.pid = item["pid"]
		if "price"  in item : myPlace.price = item["price"]
		if "link"  in item : myPlace.link = item["link"]
		if "country" in item : myPlace.country = item["country"]
		if "nid"  in item : myPlace.nid = item["nid"]
		if "bathroomCount"  in item : myPlace.bathroomcount = item["bathroomCount"]
		if "bedroomCount"  in item : myPlace.bedroomcount = item["bedroomCount"]
		if "heading"  in item : myPlace.heading = item["heading"]
		if "type"  in item : 
			if "roomType" in item["type"] : myPlace.room_type = item["type"]["roomType"]
			if "propType" in item["type"] : myPlace.prop_type = item["type"]["propType"]
		if "typeAlias"  in item : 
			if "roomType" in item["typeAlias"] : myPlace.room_type_alias = item["typeAlias"]["roomType"]
			if "propType" in item["typeAlias"] : myPlace.prop_type_alias = item["typeAlias"]["propType"]
		if "latLng"  in item : myPlace.latitude = item["latLng"][0]
		if "latLng"  in item : myPlace.longitude = item["latLng"][1]
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

