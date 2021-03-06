para_file='./checkins-ny.yaml'

# clean tweets
python '../extract_clean_tweets.py' $para_file

# extract messages
python '../dump_clean_tweet_messages.py' $para_file

# extract pos tags
python '../pos-tagging.py' $para_file

# extract trajectories
python '../extract_trajectories.py' $para_file

# extract dense trajectories
python '../extract_dense_trajectories.py' $para_file
