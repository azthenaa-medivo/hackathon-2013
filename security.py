﻿import re
import cgi
import string

USER_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
TRIP_NAME_REGEX = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\s]{3,200}$")
HUB_ID_REGEX = re.compile(r"^[0-9]{1,500}$")

def valid_user_name(user_name):
	return USER_NAME_REGEX.match(user_name)

def valid_trip_name(trip_name):
	return TRIP_NAME_REGEX.match(trip_name)
	
def valid_hub_id(hub_id):
	return HUB_ID_REGEX.match(hub_id)
	
def escape_html(s):
	return cgi.escape(s, quote = True)
