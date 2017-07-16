para_file='./sample-tweets-1m.yaml'

# clean tweets
python '../extract_clean_tweets.py' $para_file

# extract pos tags
python '../pos-tagging.py' $para_file

