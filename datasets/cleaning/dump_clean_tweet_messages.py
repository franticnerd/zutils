from data_loader import load_clean_tweets, load_params
import sys

para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
td = load_clean_tweets(p['clean_tweet_file'], p['dataset_type'])
td.dump_messages(p['message_file'])
