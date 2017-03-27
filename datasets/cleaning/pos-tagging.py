from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.config.param_handler import yaml_loader
import sys


def load_clean_tweets(clean_tweet_file):
    td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    return td


def tokenize(td, ark_run_cmd, pos_tag_file):
    pos_tag_lists = td.get_pos_tags(ark_run_cmd)
    with open(pos_tag_file, 'w') as fout:
        for (tweet, l) in zip(td.tweets, pos_tag_lists):
            fout.write(str(tweet.tid) + ' ' + str(l) + '\n')

def run(clean_tweet_file, ark_run_cmd, pos_tag_file):
    td = load_clean_tweets(clean_tweet_file)
    tokenize(td, ark_run_cmd, pos_tag_file)

if __name__ == '__main__':
    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    pos_tag_file = '/Users/chao/data/source/tweets-dev/clean/pos-tags.txt'
    ark_run_cmd='java -XX:ParallelGCThreads=2 -Xmx2G -jar /Users/chao/Dropbox/code/lib/ark-tweet-nlp-0.3.2.jar'

    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        clean_tweet_file = para['clean_tweet_file']
        pos_tag_file = para['pos_tag_file']
        ark_run_cmd = para['ark_run_cmd']

    run(clean_tweet_file, ark_run_cmd, pos_tag_file)
