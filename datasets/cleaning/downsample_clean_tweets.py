from data_loader import load_clean_tweets, load_params
import sys


def run(clean_tweet_file, downsample_tweet_file, dataset_type, num=10):
    td = load_clean_tweets(clean_tweet_file, dataset_type)
    td.downsample(num)
    td.write_clean_tweets_to_file(downsample_tweet_file)


para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['clean_tweet_file'], p['downsample_tweet_file'], p['dataset_type'], p['downsample_size'])
