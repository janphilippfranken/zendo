import pandas as pd 
from os import getpid
from multiprocessing import Pool
import itertools

from h_rev import ib_results_sampler
from tests import get_tests

from grammar import productions, replacements, rules_dict, ts_rep, ts_rep_new

# data
main_df = pd.read_csv('../data/INSERT_DATA')
pp_trials = dict(main_df.groupby('token_id').size())
total_n_trials = sum(list(pp_trials.values()))
print(total_n_trials)

# parameters 
out_penalizers = [1, 3, 5, 7, 9] 
cores = ["_A"]
lambdas = [0.5, 0.75, 1, 3, 10]     
params = list(itertools.product(out_penalizers, lambdas, cores))

# get 500 test scenes for semantic evaluation
test_scenes = get_tests(n_tests=500)

# number of trials for ibs sampling (for stable results) and number of attemps per trial (epsilon)
n_trials = 100
epsilon = 100

def get_h_rev(params): 
    """
    Calls each ib sampler on a different core for a given parameter setting
    """
    print("process_id: ", getpid())
    out_penalizer = params[0]
    lam = params[1]
    core = params[2]
    ib_results_sampler(main_df,      
                       productions,   
                       replacements,  
                       rules_dict, 
                       ts_rep, 
                       ts_rep_new, 
                       total_n_trials,
                       test_scenes,
                       epsilon,
                       out_penalizer,
                       lam,
                       n_trials,
                       core)

    
if __name__ == '__main__':
    with Pool(25) as p:
        p.map(get_h_rev, params)