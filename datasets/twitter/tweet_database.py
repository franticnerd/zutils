from zutils.dto.text.text_parser import TextParser
from zutils.dto.text.word_dict import WordDict
from tweet import Tweet
from filters import EmptyMessageFilter
import codecs
from random import shuffle
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

class TweetDatabase:

    def __init__(self):
        self.tweets = []

    def load_raw_tweets_from_file(self, input_file):
        cnt = 0
        with codecs.open(input_file, 'r', 'utf-8') as fin:
            for line in fin:
                cnt += 1
                if cnt % 20000 == 0:
                    print 'Lines:', cnt, ' Tweets:', len(self.tweets)
                try:
                    tweet = Tweet()
                    tweet.load_raw(line)
                    self.tweets.append(tweet)
                except:
                    continue

    def load_clean_tweets_from_file(self, input_file):
        self.tweets = []
        with codecs.open(input_file, 'r', 'utf-8') as fin:
            for line in fin:
                tweet = Tweet()
                tweet.load_clean(line)
                self.tweets.append(tweet)

    def get_tweet_ids(self):
        return [tweet.tid for tweet in self.tweets]

    def set_tweets(self, tweets):
        self.tweets = tweets

    def shuffle_tweets(self):
        shuffle(self.tweets)

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def size(self):
        return len(self.tweets)

    def index(self):
        self.indexed_tweets = {}
        for tweet in self.tweets:
            tweet_id = tweet.tid
            self.indexed_tweets[tweet_id] = tweet

    def get_tweet(self, tweet_id):
        return self.indexed_tweets[tweet_id]


    def dedup(self):
        new_tweets = []
        seen_tweet_ids = set()
        for tweet in self.tweets:
            if tweet.tid not in seen_tweet_ids:
                new_tweets.append(tweet)
                seen_tweet_ids.add(tweet.tid)
        self.tweets = new_tweets

    def sort_by_time(self):
        self.tweets.sort(key=lambda x: x.timestamp.timestamp, reverse=False)


    def clean_timestamps(self):
        for tweet in self.tweets:
            tweet.timestamp.gen_timestamp()


    def tokenize_message(self, preserve_types=None, ark_run_cmd=None, min_length=3):
        print 'Begin tokenizing messages...'
        tp = TextParser(min_length)
        if preserve_types is not None and ark_run_cmd is not None:
            self.tokenize_pos(tp, preserve_types, ark_run_cmd)
        else:
            self.tokenize_plain(tp)
        print 'Tokenization done.'


    # tokenize the message into unigrams
    def tokenize_plain(self, tp):
        for t in self.tweets:
            words = tp.parse_words(t.message.raw_message, stem=True)
            t.message.set_clean_words(words)


    # tokenize the message with the TweetNLP tool
    def tokenize_pos(self, tp, preserve_types, ark_run_cmd):
        message_list = [t.message.raw_message for t in self.tweets]
        word_lists = tp.parse_words_by_ark_nlp_batch(message_list, \
                                                     preserve_types, ark_run_cmd)
        for i, words in enumerate(word_lists):
            self.tweets[i].message.set_clean_words(words)


    def get_pos_tags(self, ark_run_cmd=None, min_length=3):
        print 'Begin pos-tagging messages...'
        tp = TextParser(min_length)
        message_list = [t.message.raw_message for t in self.tweets]
        pos_tag_lists = tp.get_pos_tag_lists(message_list, ark_run_cmd)
        print 'Pos-tagging done.'
        return pos_tag_lists


    def trim_words_by_frequency(self, word_dict_file=None,
            freq_threshold=500000, infreq_threshold=10):
        wd = self.gen_word_dict(word_dict_file)
        freq_words = wd.get_frequent_words(freq_threshold)
        infreq_words = wd.get_infrequent_words(infreq_threshold)
        stopwords = freq_words.union(infreq_words)
        for tweet in self.tweets:
            tweet.message.remove_stopwords(stopwords)


    def gen_word_dict(self, output_file=None):
        wd = WordDict()
        for tweet in self.tweets:
            wd.update_count(tweet.message.words)
        wd.encode_words()
        if output_file is not None:
            wd.write_to_file(output_file)
        return wd


    def apply_filters(self, filters):
        for f in filters:
            self.apply_one_filter(f)

    def apply_one_filter(self, custom_filter):
        print 'Before filtering # tweets:', len(self.tweets)
        filtered_tweets = []
        for tweet in self.tweets:
            if custom_filter.verify(tweet):
                filtered_tweets.append(tweet)
        self.tweets = filtered_tweets
        print 'After filtering # tweets:', len(self.tweets)


    def print_tweets(self):
        for t in self.tweets:
            print t.to_string(',')

    def write_clean_tweets_to_file(self, output_file):
        cnt = 0
        with codecs.open(output_file, 'w', 'utf-8') as fout:
            for tweet in self.tweets:
                fout.write(tweet.to_string() + '\n')
                cnt += 1
                if cnt % 10000 == 0:
                    print 'Finished writing %d clean tweets.' % cnt
        print 'Finished dumping %d clean tweets.' % cnt


    def dump_messages(self, message_file):
        cnt = 0
        with codecs.open(message_file, 'w', 'utf-8') as fout:
            for tweet in self.tweets:
                fout.write(tweet.message.raw_message + '\n')
                cnt += 1
                if cnt % 10000 == 0:
                    print 'Finished dumping messages for %d clean tweets.' % cnt
        print 'Finished dumping messages for %d clean tweets.' % cnt


    def calc_lat_range(self):
        lats = [t.location.lat for t in self.tweets]
        return min(lats), max(lats)


    def calc_lng_range(self):
        lngs = [t.location.lng for t in self.tweets]
        return min(lngs), max(lngs)

    def calc_time_range(self):
        tmps = [t.timestamp.timestamp for t in self.tweets]
        return min(tmps), max(tmps)

    def downsample(self, num=10000):
        random.seed(100)
        l = self.tweets
        limit = min(num, len(l))
        rand_smpl = [l[i] for i in sorted(random.sample(xrange(len(l)), limit))]
        self.tweets = rand_smpl


if __name__ == '__main__':
    input_dir = '/Users/chao/Dropbox/data/raw/'
    output_dir = '/Users/chao/Dropbox/data/activity/'
    raw_tweet_file = input_dir + 'ny_tweet_sample.txt'
    word_dict_file = output_dir + 'word_dict.txt'
    clean_tweet_file = output_dir + 'tweets.txt'
    td = TweetDatabase()
    # 1. load raw tweets
    td.load_raw_tweets_from_file(raw_tweet_file)
    # 2. clean timestamps
    td.clean_timestamps()
    # 3. tokenize messages using ark nlp
    preserve_types = set(['N', '^', 'S', 'Z', 'V', 'A', 'R', '#'])
    ark_run_cmd='java -XX:ParallelGCThreads=2 -Xmx2G -jar /Users/chao/Dropbox/code/lib/ark-tweet-nlp-0.3.2.jar'
    td.tokenize_message(preserve_types, ark_run_cmd)
    # 4. remove frequent and infrequent words
    freq_thresh = 500000
    infreq_thresh = 50
    td.trim_words_by_frequency(word_dict_file, freq_thresh, infreq_thresh)
    # 5. filter tweets
    emf = EmptyMessageFilter()
    td.apply_one_filter(emf)
    # 6. write clean tweets
    td.write_clean_tweets_to_file(clean_tweet_file)
