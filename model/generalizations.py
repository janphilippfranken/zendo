import pandas as pd 
from tqdm import tqdm
import json 

from mcmc_sampler import MCMCSampler
from transform_functions import get_production_probs_prototype

from grammar import productions, replacements, rules_dict, ts_rep, ts_rep_new

mcmc = MCMCSampler()

def generate_rule_bags(main_df,      
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
                       core):
    """ 
    """
    norm_rules_prior = []
    norm_rules_post = []
    tr_rules = []
    ts_rules = []
    
    for i in tqdm(range(total_n_trials)):
        rule_name = main_df['rule_name'][i]
        correct_rule = rules_dict[rule_name]
        # subj token
        token_id = main_df['token_id'][i] 
        # data
        init_trials = eval(main_df['data'][i])[:8]
        rev_trials =  eval(main_df['partner_data'][i])[:8]
        full_data = init_trials + rev_trials 
        # feat and value probs
        prior_probs = get_production_probs_prototype(init_trials, 'prior', cond='1', feat_only=False)
        Dwin_prior = prior_probs[0]
        feat_probs_prior = prior_probs[1]
        post_probs = get_production_probs_prototype(full_data ,'post', cond='1', feat_only=False)
        Dwin_post = post_probs[0]
        feat_probs_post = post_probs[1]

        # note - can run them separately (eg only normative first on the grid for 5 * 1 b and then tr and ts on the 5 *5 grid for b and lambda)
        # norm prior 
        print('prior')
        norm_rules_prior.append(mcmc.generic_sampler(productions, 
                                                     replacements, 
                                                     data=init_trials,
                                                     Dwin=Dwin_prior,
                                                     feat_probs=feat_probs_prior,
                                                     out_penalizer=out_penalizer,
                                                     iterations=n_trials_norm))
    
        # norm posterior 
        print('running post')
        norm_rules_post.append(mcmc.generic_sampler(productions, 
                                                    replacements, 
                                                    data=full_data,
                                                    Dwin=Dwin_post,
                                                    feat_probs=feat_probs_post,
                                                    out_penalizer=out_penalizer,
                                                    iterations=n_trials_norm))
        
        # tr simulations 
        tr_rules.append(mcmc.tr_sampler(productions, 
                                        replacements, 
                                        data=full_data,
                                        bv=bv_h_init,
                                        start=h_init,
                                        Dwin=Dwin_post,
                                        feat_probs=feat_probs_post,
                                        out_penalizer=out_penalizer,
                                        lam=lam,
                                        iterations=n_trials_process))

        # ts simulations 
        ts_rules.append(mcmc.ts_sampler(productions, 
                                        rep=ts_rep,
                                        rep_new=ts_rep_new,
                                        data=full_data,
                                        bv=bv_h_init,
                                        start=h_init,
                                        Dwin=Dwin_post,
                                        feat_probs=feat_probs_post,
                                        out_penalizer=out_penalizer,
                                        lam=lam,
                                        iterations=n_trials_process))   

        with open('sim_results/INSERT_EXP_rules_init_INSERT_TRIALS_penalize_' + str(out_penalizer) + '.json', 'w', encoding='utf-8') as f:
            json.dump(norm_rules_prior, f, ensure_ascii=False, indent=4)

        with open('sim_results/INSERT_EXP_normative_rules_rev_INSERT_TRIALS_penalize_' + str(out_penalizer) + '.json', 'w', encoding='utf-8') as f:
            json.dump(norm_rules_post, f, ensure_ascii=False, indent=4)

        with open('sim_result/INSERT_EXP_tr_rules_init_INSERT_TRIALS_penalize_' + str(out_penalizer) + '_lambda_' + str(lam) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(tr_rules, f, ensure_ascii=False, indent=4)

        with open('sim_results/INSERT_EXP_ts_rules_rev_INSERT_TRIALS_penalize_' + str(out_penalizer) + '_lambda_' + str(lam) + '_' + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(ts_rules, f, ensure_ascii=False, indent=4)