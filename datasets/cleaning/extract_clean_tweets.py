from zutils.datasets.twitter.filters import EmptyCategoryFilter
from zutils.datasets.twitter.filters import EmptyMessageFilter
from data_loader import load_raw_tweets, load_venues, load_params
import sys

'''
1. Load tweets from the raw input file
2. Remove duplicate
3. Transform raw time into timestamps
4. Tokenize the messages and remove infrequent keywords
5. Remove empty-message tweets, sort by timestamp
6. Write clean tweets to file
'''


def clean_tweets(td, word_dict_file, freq_thresh, infreq_thresh):
    print 'Number of raw tweets:', td.size()
    td.dedup()
    print 'Number of tweets after deduplication:', td.size()
    td.clean_timestamps()  # start timestamp: '2000-01-03 00:00:00', Monday
    td.tokenize_message()
    td.trim_words_by_frequency(word_dict_file, freq_thresh, infreq_thresh) # default infrequency thresh: 100
    emf = EmptyMessageFilter()
    td.apply_one_filter(emf)
    print 'Number of tweets after empty-message filtering:', td.size()
    td.sort_by_time()

def join_with_venues(td, vd):
    # for checkin datasets: join with the venue database to clean category information
    td.join_venue_database(vd)
    ecf = EmptyCategoryFilter()
    td.apply_one_filter(ecf)



def run(raw_tweet_file, word_dict_file, clean_tweet_file, dataset_type, raw_venue_file, freq_thresh, infreq_thresh, clean_venue_file=None):
    td = load_raw_tweets(raw_tweet_file, dataset_type)
    clean_tweets(td, word_dict_file, freq_thresh, infreq_thresh)
    if dataset_type == 'checkin':
        vd = load_venues(raw_venue_file)
        vd.write_clean_venues_to_file(clean_venue_file)
        join_with_venues(td, vd)
    td.write_clean_tweets_to_file(clean_tweet_file)



# para_file = '/Users/chao/Dropbox/Code/zutils/datasets/cleaning/scripts/checkins-dev.yaml'
para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['raw_tweet_file'], p['word_dict_file'], p['clean_tweet_file'], p['dataset_type'], p['raw_venue_file'], \
    p['freq_thresh'], p['infreq_thresh'], p['clean_venue_file'])

