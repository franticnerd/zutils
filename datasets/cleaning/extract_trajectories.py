from zutils.datasets.twitter.trajectory_database import TrajectoryDatabase
from data_loader import load_clean_tweets, load_params
import sys

def convert_to_traj_db(td):
    tra_db = TrajectoryDatabase()
    tra_db.convert_from_tweet_database(td)
    return tra_db

def run(clean_tweet_file, traj_db_file, dataset_type):
    td = load_clean_tweets(clean_tweet_file, dataset_type)
    traj_db = convert_to_traj_db(td)
    print 'Number of trajectories:', traj_db.size()
    traj_db.write_to_file(traj_db_file)

para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['clean_tweet_file'], p['trajectory_file'], p['dataset_type'])
