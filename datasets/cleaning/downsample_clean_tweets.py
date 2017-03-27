from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.config.param_handler import yaml_loader
import sys

def load_clean_tweets(clean_tweet_file):
    td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    return td

def run(clean_tweet_file, downsample_tweet_file, num=10):
    td = load_clean_tweets(clean_tweet_file)
    td.downsample(num)
    td.write_clean_tweets_to_file(downsample_tweet_file)

if __name__ == '__main__':

    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    downsample_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-downsample.txt'
    num = 10

    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        clean_tweet_file = para['clean_tweet_file']
        downsample_tweet_file = para['downsample_tweet_file']
        num = para['downsample_size']

    run(clean_tweet_file, downsample_tweet_file, num)

