from zutils.algo.utils import format_list_to_string
from collections import Counter

counter = Counter()

# format the tweets that are separated by '\t' phrases
def format_old_www_tweets(old_format_file, new_format_file):
    with open(old_format_file, 'r') as fin, open(new_format_file, 'w') as fout:
        for line in fin:
            formatted_line = format_line(line)
            fout.write(formatted_line + '\n')

def format_line(line):
    items = line.strip().split('\x01')
    words = items[6]
    words = words.replace(' ', '_').split('\t')
    words = [w for w in words if len(w) > 0]
    items[6] = words
    items = [e for e in items if len(e) > 0]
    counter.update([len(items)])
    return format_list_to_string(items, '\x01')

# input_file = '/Users/chao/data/source/tweets-www/clean/t.txt'
input_file = '/Users/chao/data/source/tweets-www/raw/tweets.txt'
output_file = '/Users/chao/data/source/tweets-www/clean/tweets.txt'
format_old_www_tweets(input_file, output_file)
print counter

# input_file_a = '/Users/chao/data/source/tweets-www/clean/tweets.txt'
# input_file_b = '/Users/chao/data/source/tweets-www/clean/tweets-no-poi-info.txt'
# list_a = []
# with open(input_file_a) as fin:
#     for line in fin:
#         words = line.strip().split('\x01')[6]
#         list_a.append(words)
# list_b = []
# with open(input_file_b) as fin:
#     for line in fin:
#         words = line.strip().split('\x01')[6]
#         list_b.append(words)
# for a, b in zip(list_a, list_b):
#     if a != b:
#         print 'error'
#         print a
