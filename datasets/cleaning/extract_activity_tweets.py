from zutils.datasets.twitter.filters import ContainWordFilter
from zutils.dto.text.word_distribution import WordEntropyProcessor
from data_loader import load_clean_tweets, load_params
import sys


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


para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['clean_tweet_file'], p['activity_tweet_file'], p['grid_bin_list'], p['word_entropy_file'], p['activity_word_ratio'])
