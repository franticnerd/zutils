para_file='./sample-tweets-100k.yaml'

# clean tweets
python '../extract_clean_tweets.py' $para_file

# downsample tweets
python '../downsample_clean_tweets.py' $para_file

# extract messages
python '../dump_clean_tweet_messages.py' $para_file

# extract pos tags
python '../pos-tagging.py' $para_file

# extract activity tweets
python '../extract_activity_tweets.py' $para_file

# extract trajectories
python '../extract_trajectories.py' $para_file

# extract dense trajectories
python '../extract_dense_trajectories.py' $para_file
