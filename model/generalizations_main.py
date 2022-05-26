import pandas as pd 
from tqdm import tqdm
import json 
from multiprocess import Pool
import itertools

from generalizations import generate_rule_bags
from grammar import productions, replacements, rules_dict, ts_rep, ts_rep_new

# data
main_df = pd.read_csv('../data/DATA_NAME.csv')
pp_trials = dict(main_df.groupby('token_id').size())
total_n_trials = sum(list(pp_trials.values()))

# parameters for grid search
out_penalizers = [1, 3, 5, 7, 9] 
cores = ["A"] # can be extended if more than 25 cores to decrease runtime
lambdas = [0.5, 0.75, 1, 3, 10]     

params = list(itertools.product(out_penalizers, lambdas, cores))

n_trials_norm = 1 # specify length of mcmc chain 
n_trials_process = 1 # specify how often an mcmc chain of length k is repeated to get stable results


def get_gen(parameter): 
    out_penalizer = parameter[0]
    lam = parameter[1]
    core = parameter[2]
    generate_rule_bags(main_df,      
                   productions,   
                   replacements,  
                   rules_dict, 
                   ts_rep, 
                   ts_rep_new, 
                   total_n_trials,
                   out_penalizer,
                   lam,
                   n_trials_norm,
                   n_trials_process,
                   core)

if __name__ == '__main__':
    with Pool(25) as p: # 25 cores for 5 * 5 grid; change if needed
        p.map(get_gen, params)