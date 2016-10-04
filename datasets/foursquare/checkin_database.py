from checkin import Checkin
import codecs
from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.twitter.filters import EmptyMessageFilter

class CheckinDatabase(TweetDatabase):

    def load_raw_tweets_from_file(self, input_file):
        self.tweets = []
        cnt = 0
        with codecs.open(input_file, 'r', 'utf-8') as fin:
            for line in fin:
                cnt += 1
                if cnt % 10000 == 0:
                    print 'Lines:', cnt, ' Tweets:', len(self.tweets)
                tweet = Checkin()
                try:
                    tweet.load_raw(line)
                    self.tweets.append(tweet)
                except:
                    # print line.encode('utf-8')
                    continue


    def load_clean_tweets_from_file(self, input_file):
        self.tweets = []
        with codecs.open(input_file, 'r', 'utf-8') as fin:
            for line in fin:
                tweet = Checkin()
                tweet.load_clean(line)
                self.tweets.append(tweet)


    def join_venue_database(self, vd):
        for tweet in self.tweets:
            tweet.join_with_venue(vd)


if __name__ == '__main__':
    input_dir = '/Users/chao/Dropbox/data/raw/4sq/'
    checkin_file = input_dir + 'nyc_checkins.csv'
    td = CheckinDatabase()
    td.load_raw_tweets_from_file(checkin_file)
