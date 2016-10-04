import pymongo as pm
import sys
from zutils.config.param_handler import yaml_loader
from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.twitter.tweet import Tweet
from zutils.dto.st.location import Location
from zutils.dto.st.timestamp import Timestamp
from zutils.dto.text.message import Message


class TweetMongo:

    # dns: string, port: int
    def __init__(self, dns, port, db_name, tweet_col_name):
        try:
            conn = pm.MongoClient(dns, port)
            self.db = conn[db_name]
            self.tweet_col = self.db[tweet_col_name]
        except:
            print 'Unable to connect to mongoDB.'

    def get_one_tweet(self):
        return self.tweet_col.find_one()


    def get_all_tweets(self, query=None):
        ret = []
        cnt = 0
        for o in self.tweet_col.find(query):
            tweet = self.bson_to_tweet(o)
            ret.append(tweet)
            cnt += 1
            if cnt % 100000 == 0:
                print 'Loaded %d tweets from mongodb.' % cnt
        return ret

    def bson_to_tweet(self, d):
        tweet = Tweet()
        tweet.tid = d['id']
        tweet.uid = d['uid']
        tweet.location = Location(d['lat'], d['lng'])
        tweet.timestamp = Timestamp(d['time'])
        tweet.timestamp.timestamp = d['timestamp']
        tweet.message = Message(d['text'])
        tweet.message.words = d['phrases']
        return tweet


    def num_tweets(self):
        return self.tweet_col.count()

    def remove_all_tweets(self):
        self.tweet_col.drop()


    def write_to_mongo(self, tweet_database):
        insert_cnt, batch = 0, []
        for tweet in tweet_database.tweets:
            mongo_tweet = self.format_tweet_to_bson(tweet)
            batch.append(mongo_tweet)
            insert_cnt += 1
            if insert_cnt % 10000 == 0:
                self.tweet_col.insert(batch)
                batch = []
                print 'Inserted:', insert_cnt, '; Total:', self.tweet_col.count()
        self.tweet_col.insert(batch)
        print 'Total:', self.tweet_col.count()


    def format_tweet_to_bson(self, tweet):
        mongo_tweet = {}
        mongo_tweet['id'] = tweet.tid
        mongo_tweet['uid'] = tweet.uid
        mongo_tweet['time'] = tweet.timestamp.time_string
        mongo_tweet['timestamp'] = tweet.timestamp.timestamp
        mongo_tweet['lat'] = tweet.location.lat
        mongo_tweet['lng'] = tweet.location.lng
        mongo_tweet['text'] = tweet.message.raw_message
        mongo_tweet['phrases'] = tweet.message.words
        return mongo_tweet


if __name__ == "__main__":
    print 'hello'
    tm = TweetMongo('dmserv4.cs.illinois.edu', 11111, 'foursquare', 'checkins')
    print tm.get_one_tweet()
    print tm.num_tweets()
    # tm.remove_all_tweets()
    # td = TweetDatabase()
    # td.load_clean_tweets_from_file('clean.txt')
    # tm.write_to_mongo(td)
