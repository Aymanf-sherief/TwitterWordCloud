import json

from twitter_word_cloud import TwitterCloud

keys = json.load(open('keys.json'))

client = TwitterCloud(keys)

client.get_tweets()

client.generate_word_cloud()