import oauth2
import urllib2
import json
import handler 

class YelpAPIHandler(handler.Handler):
	def get(self):
		# Fill in these values
		consumer_key = 'utGz8uCHzsk3UQBt1HHgNQ'
		consumer_secret = 'ClR4PUFKwIyH-VGhaxVzVsFL5PY'
		token = 'wZuclqDFn7yRxZ3peQv6Gc9qcfXaJKF8'
		token_secret = 'm2yXkpO5i2Teip1GnnldjFX3czI'
		consumer = oauth2.Consumer(consumer_key, consumer_secret)
		url = 'http://api.yelp.com/v2/search?term=bars&location=sf'
		oauth_request = oauth2.Request('GET', url, {})
		oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
							  'oauth_timestamp': oauth2.generate_timestamp(),
							  'oauth_token': token,
							  'oauth_consumer_key': consumer_key})
		token = oauth2.Token(token, token_secret)
		oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
		signed_url = oauth_request.to_url()
		
		try:
			conn = urllib2.urlopen(signed_url, None)
			try:
			  response = json.loads(conn.read())
			finally:
			  conn.close()
		except urllib2.HTTPError, error:
			response = json.loads(error.read())
		self.response.out.write(response)