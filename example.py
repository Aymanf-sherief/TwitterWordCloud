import json

from TwitterCloud.TwitterCloud import TwitterCloud

keys = json.load(open('keys.json'))

client = TwitterCloud(keys)

client.get_tweets()
print(client.tweets)
client.generate_word_cloud()