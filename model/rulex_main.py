import pandas as pd 
import numpy as np
from tqdm import tqdm
import json 
from multiprocessing import Pool
import itertools

from model_classes.pcfg_generator import PCFG
from ib_sampler import IBSSampler
from grammar import productions, replacements, rules_dict, ts_rep, ts_rep_new


# data
main_df = pd.read_csv('../data/INSERT_DATA')
pp_trials = dict(main_df.groupby('token_id').size())
n = sum(list(pp_trials.values()))


Z = PCFG()
ib = IBSSampler()

def generate_simple(n):
    simple_bag = []
    for i in range(n):
        simple = False
        while simple is not True:
            t = Z.generate_res(productions,bound_vars=[])
            if list(t['prec']['to']).count('J(B,B)') == 0:
                if list(t['prec']['to']).count('S') == 0:
                    if list(t['prec']['to']).count('Z.not_operator(B)') <= 1:
                        simple = True
        simple_bag.append(t['rule'])
    return simple_bag

def generate_conjunctive(n):
    conjunctive_bag = []
    for i in range(n):
        conjunct = False
        while conjunct is not True:
            t = Z.generate_res(productions,bound_vars=[])
            if list(t['prec']['to']).count('J(B,B)') == 1:
                conjunct = True   
        conjunctive_bag.append(t['rule'])
    return conjunctive_bag

first_bag = []

with open('rulex_rule_bags/first_bag.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        current_place = line[:-1]
        first_bag.append(current_place)

with open('rulex_rule_bags/first_bag_neg.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        current_place = line[:-1]
        first_bag.append(current_place)
        

def generate_rules_rulex(params):

    lam = params[0]
    n_sim = params[1]
    core = params[2]


    h_init_search = {}
    exact_search = {}
    imperfect_search = {}
    conjunct_search = {}

    for trial in tqdm(range(n)):
        # all pp trials 
        h_init_search[trial] = {}
        exact_search[trial] = {}
        imperfect_search[trial] = {}
        conjunct_search[trial] = {}

        init_trials = eval(main_df['data_prior'][trial])[:8]
        rev_trials =  eval(main_df['data_posterior'][trial])[:8]
        data = init_trials + rev_trials

        h_init = {'rule': main_df['prior_resp'][trial]}
        h_init_out = ib.get_outlier(rev_trials, h_init, h_init)[0]
        h_rev = {'rule': main_df['post_resp'][trial]}

        if h_init_out == 0: 
            h_init_search[trial] = h_init
        else:
            for sim in range(n_sim):
                # number of simulations to get stable estimate simulations 
                exact_search[trial][sim] = None
                imperfect_search[trial][sim] = None
                conjunct_search[trial][sim] = None

                # rule bags 
                k = np.random.poisson(lam=lam) + 1 # search steps (fit this one)
                simple_rules = np.random.choice(first_bag, k) # sampled uniformly in analysis as simple rules could be enumerated 
                # simple_rules = generate_simple(k)
                conjunct_rules = generate_conjunctive(k) # sampled randomly from prior for conjunctive / disjunctive rules as this bag could not be enumerated
                imperfect = False
                conjunct = False
                exact = False
                for out in range(len(data) + 1):
                    for rule, conjunct_rule in zip(simple_rules, conjunct_rules):   
                        rule = {'rule': rule}
                        rule_out = ib.get_outlier(data, rule, rule)[0]
                        if not exact and rule_out == out == 0:
                            exact_search[trial][sim] = rule['rule']
                            exact = True
                            break
                        else:
                            conjunct_rule = {'rule': conjunct_rule}
                            conjunct_rule_out = ib.get_outlier(data, conjunct_rule, conjunct_rule)[0]
                            if not conjunct and conjunct_rule_out == out:
                                conjunct_search[trial][sim] = {str(out): conjunct_rule['rule']}
                                conjunct = True 
                            if not imperfect and rule_out == out:
                                imperfect_search[trial][sim] = {str(out): rule['rule']}
                                imperfect = True 
                    if exact:
                        break
                    if conjunct and imperfect: 
                        break
        with open('sim_results/exp_1_248_rulex_h_init_lam_' + str(lam) + '_sim_' + str(n_sim) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(h_init_search, f, ensure_ascii=False, indent=4)
        with open('sim_results/exp_1_248_exact_lam_' + str(lam) + '_sim_' + str(n_sim) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(exact_search, f, ensure_ascii=False, indent=4)
        with open('sim_results/exp_1_248_imperfect_lam_' + str(lam) + '_sim_' + str(n_sim) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(imperfect_search, f, ensure_ascii=False, indent=4)
        with open('sim_results/exp_1_248_conjunct_lam_' + str(lam) + '_sim_' + str(n_sim) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(conjunct_search, f, ensure_ascii=False, indent=4)
            
            
lams = [0.5, 0.75, 1, 3, 10]
simulations = [2000]
core = ["A", "B", "C", "D", "E"]
# core = ["A"]

params = list(itertools.product(lams, simulations, core))

print(params)
print(len(params))


if __name__ == '__main__':
    with Pool(25) as p:
        p.map(generate_rules_rulex, params)