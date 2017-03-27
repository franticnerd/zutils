from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.twitter.filters import ContainWordFilter
from zutils.dto.text.word_distribution import WordEntropyProcessor
from zutils.config.param_handler import yaml_loader
import sys


def load_clean_tweets(clean_tweet_file):
    td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    return td


def find_activity_tweets(td, grid_bin_list, word_entropy_file, activity_word_fraction):
    wep = WordEntropyProcessor(td, grid_bin_list)
    wep.calc(word_entropy_file)
    activity_words = wep.select_top_words(activity_word_fraction)
    cwf = ContainWordFilter(activity_words)
    td.apply_one_filter(cwf)


def write_activity_tweets(td, activity_tweet_file):
    td.write_clean_tweets_to_file(activity_tweet_file)


def run(clean_tweet_file, activity_tweet_file, grid_bin_list, word_entropy_file, activity_word_fraction):
    td = load_clean_tweets(clean_tweet_file)
    find_activity_tweets(td, grid_bin_list, word_entropy_file, activity_word_fraction)
    write_activity_tweets(td, activity_tweet_file)

if __name__ == '__main__':
    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    activity_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    word_entropy_file = '/Users/chao/data/source/tweets-dev/clean/word-entropy.txt'
    grid_bin_list = [50, 50, 150]
    activity_word_ratio = 0.2

    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        clean_tweet_file = para['clean_tweet_file']
        activity_tweet_file = para['activity_tweet_file']
        word_entropy_file = para['word_entropy_file']
        grid_bin_list = para['grid_bin_list']
        activity_word_ratio = para['activity_word_ratio']

    run(clean_tweet_file, activity_tweet_file, grid_bin_list, word_entropy_file, activity_word_ratio)
