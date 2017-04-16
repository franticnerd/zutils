import ast
import sys
from collections import defaultdict
from itertools import groupby

from zutils.datasets.cleaning.data_loader import load_clean_tweets, load_params


class PosDatabase:

    def __init__(self):
        self.wd = defaultdict(lambda: defaultdict(lambda: []))


    # load the pos tags into a dictionary, key: tweet id, value: dict (pos type: value)
    def load_postags(self, pos_tag_file):
        with open(pos_tag_file, 'r') as fin:
            for line in fin:
                fields = line.strip().split('\x01')
                tweet_id = long(fields[0])
                items = [ast.literal_eval(field) for field in fields[1:]]
                items.sort(key=lambda x:x[1])
                groups = groupby(items, key=lambda x:x[1])
                for pos_type, group in groups:
                    keywords = [x[0] for x in list(group)]
                    self.wd[tweet_id][pos_type] = keywords


    # we use 'E' to represent entities
    def load_entities(self, entity_file):
        with open(entity_file, 'r') as fin:
            for line in fin:
                fields = line.strip().split()
                tweet_id, entities = long(fields[0]), fields[1:]
                self.wd[tweet_id]['E'] = entities


    # replace the keywords with the given pos tag types for all the tweets in a database
    def replace_keywords(self, td, pos_types):
        for tweet in td.tweets:
            pos_keywords = self.get_pos_keywords(tweet.tid, pos_types)
            tweet.message.words = pos_keywords
            # print tweet.tid, tweet.message.words


    # get the clean pos keywords after dedup:
    def get_pos_keywords(self, tweet_id, pos_types):
        ret = []
        for t in pos_types:
            ret.extend(self.wd[tweet_id][t])
        lower_words = list(x.lower() for x in ret if len(x) > 2)
        return list(set(lower_words))


if __name__ == '__main__':
    para_file = None if len(sys.argv) <= 1 else sys.argv[1]
    p = load_params(para_file)
    td = load_clean_tweets(p['clean_tweet_file'], p['dataset_type'])
    pd = PosDatabase()
    pd.load_entities(p['clean_entity_file'])
    pd.load_postags(p['pos_tag_file'])
    pd.replace_keywords(td, ['^'])





#
# def load_entities(self, entity_file):
#     with open(entity_file, 'r') as fin:
#         for line in fin:
#             items = line.strip().split()
#             tweet_id = long(items[0])
#             entities = [(item, 'E') for item in items[1:]]
#             self.update_pos_tweets(tweet_id, entities)
#             # for k, v in self.pos_tweets.items():
#             #     print k, v
#
#
# def load_pos_tags(self, input_file):
#     with open(input_file, 'r') as fin:
#         for line in fin:
#             items = line.strip().split('\x01')
#             tweet_id = long(items[0])
#             pos_tags = [ast.literal_eval(item) for item in items[1:]]
#             self.update_pos_tweets(tweet_id, pos_tags)
#             # for k, v in self.pos_tweets.items():
#             #     print k, v
#
#
# def update_pos_tweets(self, tweet_id, pos_tags):
#     groups = defaultdict(lambda: [])
#     for element in pos_tags:
#         pos_tag, pos_type = element[0], element[1]
#         groups[pos_type].append(pos_tag)
#     for t, l in groups.items():
#         self.pos_tweets[t][tweet_id] = l
#
#
# # clean pos tag words for one tweet: lower case, dedup
# def gen_pos_clean_words(self, tweet_id, pos_set):
#     pos_sets = self.gen_pos_tags(tweet_id, pos_set)
#     s = ' '.join(pos_sets)
#     return set(self.tp.parse_words(s))
#
#
# # generate the raw ensemble of pos tags for one tweet
# def gen_pos_tags(self, tweet_id, pos_set):
#     ret = []
#     for e in pos_set:
#         tweets = self.pos_tweets[e]
#         # print tweets
#         if tweet_id in tweets:
#             ret.extend(tweets[tweet_id])
#     return ret

# input_file = '/Users/chao/data/source/tweets-dev/clean/pos-tags.txt'
# pd = PosDatabase()
# pd.load_pos_tags(input_file)
# print 'generating pos done'
# # print pd.gen_pos_clean_words(495071426513489920L, ['#', 'N', 'V'])
# print pd.gen_pos_clean_words(495071508516323328, ['#', 'N', 'V'])
# print pd.gen_pos_clean_words(495071468041289728, ['#', 'N', 'V'])
