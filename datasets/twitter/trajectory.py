from tweet import Tweet
import sys

class Trajectory:

    def __init__(self):
        self.tweets = []

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def size(self):
        return len(self.tweets)

    def sort_by_time(self):
        self.tweets.sort(key=lambda x: x.timestamp.timestamp, reverse=False)

    def print_tweets(self):
        for t in self.tweets:
            print t.to_string(',')

    # extract dense sub-trajectories from this trajectory
    def extract_dense(self, max_gap):
        ret = []
        trajectory = Trajectory()
        previous_timestamp = float('-inf')
        for t in self.tweets:
            current_ts = t.timestamp.timestamp
            if current_ts - previous_timestamp <= max_gap:
                trajectory.add_tweet(t)
            else:
                if trajectory.size() >= 2:
                    ret.append(trajectory)
                trajectory = Trajectory()
                trajectory.add_tweet(t)
            previous_timestamp = current_ts
        if trajectory.size() >= 2:
            ret.append(trajectory)
        return ret
