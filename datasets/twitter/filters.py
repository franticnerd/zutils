

# return true if the message is not empty
class EmptyMessageFilter:
    def verify(self, tweet):
        if len(tweet.message.words) > 0:
            return True
        else:
            return False


# return true if the category is not empty
class EmptyCategoryFilter:
    def verify(self, tweet):
        if tweet.category is not None:
            return True
        else:
            return False


# return true if the tweet contains at least one of the target words
class ContainWordFilter:
    def __init__(self, target_words):
        self.target_words = target_words

    def verify(self, tweet):
        for word in tweet.message.words:
            if word in self.target_words:
                return True
        return False


# return true if the tweet id is in the given tweet id set.
class TweetIdContainFilter:
    def __init__(self, tweet_id_set):
        self.tweet_id_set = tweet_id_set

    def verify(self, tweet):
        if tweet.tid in self.tweet_id_set:
            return True
        else:
            return False




# return true if the tweet falls in the bounding box
class LocationFilter:
    def __init__(self, min_lat, max_lat, min_lng, max_lng):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lng = min_lng
        self.max_lng = max_lng
    def verify(self, tweet):
        l = tweet.location
        if l.lat >= self.min_lat and l.lat <= self.max_lat and \
           l.lng >= self.min_lng and l.lng <= self.max_lng:
            return True
        else:
            return False
