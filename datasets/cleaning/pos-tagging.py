from data_loader import load_clean_tweets, load_params
import sys

def tokenize(td, ark_run_cmd, pos_tag_file):
    pos_tag_lists = td.get_pos_tags(ark_run_cmd)
    with open(pos_tag_file, 'w') as fout:
        for (tweet, l) in zip(td.tweets, pos_tag_lists):
            elements = [str(tweet.tid)]
            elements.extend([str(e) for e in l])
            # fout.write(str(tweet.tid) + ' ' + str(l) + '\n')
            fout.write('\x01'.join(elements) + '\n')


def run(clean_tweet_file, ark_run_cmd, pos_tag_file, dataset_type, entity_file):
    td = load_clean_tweets(clean_tweet_file, dataset_type)
    tokenize(td, ark_run_cmd, pos_tag_file)


para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['clean_tweet_file'], p['ark_run_cmd'], p['pos_tag_file'], p['dataset_type'],\
    p['clean_entity_file'])


