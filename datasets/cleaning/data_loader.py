from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.foursquare.checkin_database import CheckinDatabase
from zutils.datasets.foursquare.venue_database import VenueDatabase
from zutils.datasets.twitter.trajectory_database import TrajectoryDatabase
from zutils.config.param_handler import yaml_loader


def load_raw_tweets(raw_tweet_file, dataset_type='tweet'):
    if dataset_type == 'checkin':
        td = CheckinDatabase()
    else:
        td = TweetDatabase()
    td.load_raw_tweets_from_file(raw_tweet_file)
    return td


def load_clean_tweets(clean_tweet_file, dataset_type='tweet'):
    if dataset_type == 'checkin':
        td = CheckinDatabase()
    else:
        td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    return td


def load_trajectories(trajectory_file, dataset_type='tweet'):
    tra_db = TrajectoryDatabase()
    tra_db.load_from_file(trajectory_file, dataset_type)
    return tra_db


def load_venues(raw_venue_file):
    vd = VenueDatabase()
    vd.load_raw_from_file(raw_venue_file)
    return vd


def load_params(para_file):
    if para_file is None:
        return set_default_params()
    para = yaml_loader().load(para_file)
    return para


def set_default_params():
    para = {}
    para['dataset_type'] = 'tweet'
    para['raw_tweet_file'] = '/Users/chao/data/source/tweets-dev/raw/tweets.txt'
    para['raw_venue_file'] = None
    para['clean_tweet_file'] = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    para['word_dict_file'] = '/Users/chao/data/source/tweets-dev/clean/words.txt'
    para['downsample_tweet_file'] = '/Users/chao/data/source/tweets-dev/clean/tweets-downsample.txt'
    para['downsample_size'] = 10
    para['message_file'] = '/Users/chao/data/source/tweets-dev/clean/messages.txt'
    para['pos_tag_file'] = '/Users/chao/data/source/tweets-dev/clean/pos-tags.txt'
    para['ark_run_cmd'] = 'java -XX:ParallelGCThreads=2 -Xmx2G -jar /Users/chao/Dropbox/code/lib/ark-tweet-nlp-0.3.2.jar'
    para['activity_tweet_file'] = '/Users/chao/data/source/tweets-dev/clean/tweets-activity.txt'
    para['word_entropy_file'] = '/Users/chao/data/source/tweets-dev/clean/word-entropy.txt'
    para['grid_bin_list'] = [50, 50, 150]
    para['activity_word_ratio'] = 0.2
    para['trajectory_file'] = '/Users/chao/data/source/tweets-dev/clean/trajectories.txt'
    para['dense_trajectory_file'] = '/Users/chao/data/source/tweets-dev/clean/trajectories-dense.txt'
    para['max_gap'] = 3600
    return para

