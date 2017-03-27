from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.config.param_handler import yaml_loader
import sys

if __name__ == '__main__':

    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    message_file = '/Users/chao/data/source/tweets-dev/clean/messages.txt'

    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        clean_tweet_file = para['clean_tweet_file']
        message_file = para['message_file']

    td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    td.dump_messages(message_file)
