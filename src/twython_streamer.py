from twython import TwythonStreamer
import credentials
import json

#Twitter Keys
consumer_key = credentials.twitter['consumer_key']
consumer_secret = credentials.twitter['consumer_secret']
access_token = credentials.twitter['access_token']
access_token_secret = credentials.twitter['access_token_secret']

# list of tweets collected since start
collectedTweets = []


class TweetStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			collectedTweets.append(data)
			print(data['text'].encode('utf-8'), '\n')
			if data['coordinates'] is not None:
				print(data['coordinates'])
			
	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()

		
def saveTweets():
	pass
		
		
def getTweets():
	try:
		while True:
			streamer = TweetStreamer(consumer_key, consumer_secret,
							access_token, access_token_secret)
			streamer.statuses.filter(track="trump")
	# Break by CTRL-C 
	except KeyboardInterrupt:
		print("{} tweets collected in list".format(len(collectedTweets)))
		
		# Save tweets locally or on S3
		pass
	
getTweets()

	


		
