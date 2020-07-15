import math
import os
import re
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import tweepy
from wordcloud import WordCloud, STOPWORDS


class TwitterCloud:
    """
    A class That Uses Twitter API Keys for a specific user to generate WordCloud charts for that user
    Based on their tweets And/Or DMs
    """

    def __init__(self, credentials):
        """
        :param credentials: A python dictionary containing twitter API keys
        credentials['CONSUMER_KEY'] = ...
        credentials['CONSUMER_SECRET'] = ...
        credentials['ACCESS_TOKEN'] = ...
        credentials['ACCESS_SECRET'] = ...
        """
        self.credentials = credentials
        self.API, self.user = self.auth(credentials)
        self.tweets = []
        self.dms = []
        self.word_counts = {}
        self.stopwords = set(STOPWORDS)

    def auth(self, credentials):
        """
        re-authenticate the API with new credentials
        (if you don't want to re-instantiate the object but want to change user for example)
        :param credentials: A python dictionary containing twitter API keys
                credentials['CONSUMER_KEY'] = ...
                credentials['CONSUMER_SECRET'] = ...
                credentials['ACCESS_TOKEN'] = ...
                credentials['ACCESS_SECRET'] = ...
        :return: a tweepy.API object authenticated with the new credentials
        """
        self.credentials = credentials
        auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
        auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

        new_api = tweepy.API(auth)
        user = new_api.me()

        return new_api, user

    def get_tweets(self, screen_name=None, n_max_tweets=20, overwrite=True):
        """
        read the authenticated user's Tweets.
        :param screen_name: String, optional, screen name of account to get tweets from
        :param n_max_tweets: Integer, optional, Maximum number of tweets to read.
        :param overwrite: Bool, optional, whether to overwrite old tweets if exist, default: True
        :return: List of tweets
        """
        if screen_name is None:
            screen_name = self.user.screen_name
            tmp_tweets = self.API.user_timeline(count=n_max_tweets)
        else:
            tmp_tweets = self.API.user_timeline(screen_name=screen_name, count=n_max_tweets)

        tweets = [tweet.text for tweet in tmp_tweets
                  if tweet.user.screen_name == screen_name and not tweet.text.startswith('RT')]
        print('tweets', tweets)
        if overwrite:
            self.tweets = tweets
        else:
            self.tweets.append(tweets)

        return tweets

    def get_dms(self, n_max_messages=20, overwrite=True):
        """
        read the authenticated user's sent DMS.
        :param n_max_messages: optional, Maximum number of messages to read.
        :param overwrite: Bool, optional, whether to overwrite old messages if exist, default: True
        :return: List of messages.
        """
        tmp_messages = self.API.sent_direct_messages(count=n_max_messages)
        dms = [message.text for message in tmp_messages]

        if overwrite:
            self.dms = dms
        else:
            self.dms.append(dms)

        return dms

    def count_words(self, list_to_use='both', n_max_words=20):
        """
        generates
        :param list_to_use: String, optional, name of list to use [tweets, dms, both]
        :param n_max_words: Int, optional, maximum number of words to include
        :return: a defaultdict instance containing words and their respective counts
        """
        if list_to_use == 'tweets':
            text_list = self.tweets
        elif list_to_use == 'dms':
            text_list = self.dms
        else:
            text_list = self.tweets + self.dms

        word_counts = defaultdict(int)
        for text in text_list:
            for word in text.split():
                if word.lower() not in self.stopwords:
                    # using the square root of the word as count to slightly favor longer words
                    word_counts[word.lower()] += math.sqrt(len(word))
        # sort the words by count then take first n_max_words only
        self.word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1])[:n_max_words]}

        return word_counts

    def generate_word_cloud(self, list_to_use='both', n_max_words=50,
                            filename=f"plot-{datetime.now().split('.')[0]}.png", show=True):
        """
        generate the word cloud plot and saves it to a .png image
        :param list_to_use: String, optional, name of list to use [tweets, dms, both]
        :param n_max_words: Int, optional, maximum number of words to include
        :param filename: string, the filename to save the plot
        :param show: bool, whether to show the plot.
        """
        if list_to_use == 'tweets':
            text_list = self.tweets
        elif list_to_use == 'dms':
            text_list = self.dms
        else:
            text_list = self.tweets + self.dms

        text = " ".join(text_list).lower()
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        font_path = os.path.join(os.path.dirname(__file__), "fonts/arabic-english.ttf")

        wordcloud = WordCloud(font_path=font_path,
                              width=800, height=800,
                              background_color='white',
                              stopwords=self.stopwords,
                              min_font_size=10,
                              max_words=n_max_words).generate(text)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        if show:
            plt.show()
        plt.savefig(filename, dpi=600)
