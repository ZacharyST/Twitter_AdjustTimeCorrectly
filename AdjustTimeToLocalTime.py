'''
The purpose of this script is to convert a tweet's timestamp to local time, as Twitter gives the UTC time of a stamp.

It is designed to work in Python 3.5.

The script assumes each tweet is its own line and saved as a string.

The try-except wrapper is because some tweets (.8% in my experience) come malformed.  The number is low enough, and the malformations appear random, so I ignore them.
'''

import json
from timezonefinder import TimezoneFinder
import pytz
import datetime as dt

# Files to read in
readin = ['/path/to/raw/tweet/file1', '/path/to/raw/tweet/file2']


for item in readin:
	with open(item, 'r') as f:
		for line in f:  # Read each tweet
				try:
					# Make string a dictionary
					tweet = line.replace('\n', '')  # Replace any newline characters
					tweet = line.replace('\r', '')  # Replace any carriage return characters
					tweet = json.loads(tweet)  # Add the tweet

					# Get GPS pair, SW corner of bounding box from Twitter
					longitude = tweet['place']['bounding_box']['coordinates'][0][0][0]
					latitude = tweet['place']['bounding_box']['coordinates'][0][0][1]

					# Get timezones
					tf = TimezoneFinder()
					zone = tf.timezone_at(lng=longitude, lat=latitude)  # Gives string of name of timezone
					timezone = pytz.timezone(zone)  # Convert string to pytz format

					# Make local time
					utc_time = dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)  # Convert tweet timestamp to datetime object
					local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)  # Get local time as datetime object

					tweet['local_time_twitterStyle'] = local_time.strftime(format='%a %b %d %H:%M:%S +0000 %Y')
					tweet['local_time_nice'] = local_time.strftime('%Y-%m-%d %H:%M:%S')

					outpath = item.replace('.txt', '_CorrectLocalTime.txt')  # File to write out.  Modify as needed; mine end in .txt.
					with open(outpath, 'a') as outfile:
						json.dump(tweet, outfile)
						outfile.write('\n')
				except:
					pass

