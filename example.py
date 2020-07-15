import json

from TwitterCloud.TwitterCloud import TwitterCloud

keys = json.load(open('keys.json'))

client = TwitterCloud(keys)

client.get_tweets()

client.generate_word_cloud()