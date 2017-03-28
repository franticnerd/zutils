from data_loader import load_trajectories, load_params
import sys


def run(trajectory_file, max_gap, dense_trajectory_file, dataset_type):
    tra_db = load_trajectories(trajectory_file, dataset_type)
    tra_db.extract_dense(max_gap)
    print 'Number of dense trajectories:', tra_db.size()
    tra_db.write_to_file(dense_trajectory_file)


para_file = None if len(sys.argv) <= 1 else sys.argv[1]
p = load_params(para_file)
run(p['trajectory_file'], p['max_gap'], p['dense_trajectory_file'], p['dataset_type'])
