from zutils.datasets.twitter.tweet_database import TweetDatabase
from zutils.datasets.foursquare.checkin import Checkin
from tweet import Tweet
from trajectory import Trajectory
import codecs

class TrajectoryDatabase:

    def __init__(self):
        self.trajectories = []

    def convert_from_tweet_database(self, td):
        trajectories = {}
        for t in td.tweets:
            user_id = t.uid
            if user_id in trajectories:
                trajectories[user_id].add_tweet(t)
            else:
                trajectory = Trajectory()
                trajectory.add_tweet(t)
                trajectories[user_id] = trajectory
        self.trajectories = trajectories.values()

    def sort_by_time(self):
        for trajectory in self.trajectories:
            trajectory.sort_by_time()


    def write_to_file(self, output_file):
        with codecs.open(output_file, 'w', 'utf-8') as fout:
            for trajectory in self.trajectories:
                elements = [t.to_string() for t in trajectory.tweets]
                fout.write('\x02'.join(elements) + '\n')


    # if the file is checkin file, needs to handle the category information
    def load_from_file(self, input_file, dataset_type='tweet'):
        with codecs.open(input_file, 'r', 'utf-8') as fin:
            for line in fin:
                trajectory = Trajectory()
                elements = line.strip().split('\x02')
                for e in elements:
                    if dataset_type == 'checkin':
                        tweet = Checkin()
                    else:
                        tweet = Tweet()
                    tweet.load_clean(e)
                    trajectory.add_tweet(tweet)
                self.trajectories.append(trajectory)


    def size(self):
        return len(self.trajectories)


    def extract_dense(self, max_gap):
        dense_trajectories = []
        for trajectory in self.trajectories:
            ret = trajectory.extract_dense(max_gap)
            dense_trajectories.extend(ret)
        self.trajectories = dense_trajectories


if __name__ == '__main__':
    clean_tweet_file = '/Users/chao/data/source/tweets-dev/clean/tweets-clean.txt'
    clean_trajectory_file = '/Users/chao/data/source/tweets-dev/clean/trajectories.txt'
    dense_trajectory_file = '/Users/chao/data/source/tweets-dev/clean/trajectories-dense.txt'
    td = TweetDatabase()
    td.load_clean_tweets_from_file(clean_tweet_file)
    print 'Number of tweets:', td.size()
    trd = TrajectoryDatabase()
    trd.convert_from_tweet_database(td)
    trd.write_to_file(clean_trajectory_file)
    print 'Number of trajectories:', trd.size()
    trd = TrajectoryDatabase()
    trd.load_from_file(clean_trajectory_file)
    print 'Number of trajectories:', trd.size()
    trd.extract_dense(3600)
    print 'Number of trajectories:', trd.size()
    trd.write_to_file(dense_trajectory_file)
