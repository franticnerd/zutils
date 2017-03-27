from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.twitter.filters import EmptyMessageFilter
from zutils.config.param_handler import yaml_loader
import sys

'''
1. Load tweets from the raw input file
2. Remove duplicate
3. Transform raw time into timestamps
4. Tokenize the messages and remove infrequent keywords
5. Remove empty-message tweets, sort by timestamp
6. Write clean tweets to file
'''


def load_raw_tweets(raw_tweet_file):
    td = TweetDatabase()
    td.load_raw_tweets_from_file(raw_tweet_file)
    return td

def clean_tweets(td, word_dict_file):
    print 'Number of raw tweets:', td.size()
    td.dedup()
    print 'Number of tweets after deduplication:', td.size()
    td.clean_timestamps()  # start timestamp: '2000-01-03 00:00:00', Monday
    td.tokenize_message()
    td.trim_words_by_frequency(word_dict_file) # default infrequency thresh: 100
    emf = EmptyMessageFilter()
    td.apply_one_filter(emf)
    print 'Number of tweets after empty-message filtering:', td.size()
    td.sort_by_time()


def run(raw_tweet_file, word_dict_file, clean_tweet_file):
    td = load_raw_tweets(raw_tweet_file)
    clean_tweets(td, word_dict_file)
    # td.downsample(100)
    td.write_clean_tweets_to_file(clean_tweet_file)

if __name__ == '__main__':

    raw_tweet_file = '/Users/chao/data/source/tweets-dev/raw/tweets.txt'
    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    word_dict_file = '/Users/chao/data/source/tweets-dev/clean/words.txt'

    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        raw_tweet_file = para['raw_tweet_file']
        clean_tweet_file = para['clean_tweet_file']
        word_dict_file = para['word_dict_file']

    run(raw_tweet_file, word_dict_file, clean_tweet_file)


