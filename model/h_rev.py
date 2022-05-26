from tqdm import tqdm
import json 

from ib_sampler import IBSSampler
from transform_functions import get_production_probs_prototype
from tests import get_tests

from grammar import productions, replacements, rules_dict, ts_rep, ts_rep_new

ib_sampler = IBSSampler()

def ib_results_sampler(main_df,      
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
                       core):
    """ 
    """
    tr_counts = []
    ts_counts = []
    
    for i in tqdm(range(total_n_trials)):
        # rule details
        rule_name = main_df['rule_name'][i]
        h_init = main_df['prior_resp'][i]
        h_rev = main_df['post_resp'][i]
        bv_h_init = eval(main_df['bound_vars'][i])
        correct_rule = rules_dict[rule_name]
        
        # subj token
        token_id = main_df['token_id'][i]
          
        # data
        init_trials = eval(main_df['data_prior'][i])[:8]
        rev_trials =  eval(main_df['data_posterior'][i])[:8]
        full_data = init_trials + rev_trials 

        # feat and value probs
        prior_probs = get_production_probs_prototype(init_trials, 'prior', cond='1', feat_only=False)
        Dwin_prior = prior_probs[0]
        feat_probs_prior = prior_probs[1]

        post_probs = get_production_probs_prototype(full_data ,'post', cond='1', feat_only=False)
        Dwin_post = post_probs[0]
        feat_probs_post = post_probs[1]
        
        # tr sampler 
        tr_counts.append(ib_sampler.tr_ib_sampler(productions, 
                                                  replacements, 
                                                  data=full_data,
                                                  test_scenes=test_scenes,
                                                  bv=bv_h_init,
                                                  start=h_init,
                                                  end=h_rev,
                                                  Dwin=Dwin_post,
                                                  feat_probs=feat_probs_post,
                                                  epsilon=epsilon,
                                                  out_penalizer=out_penalizer,
                                                  lam=lam,
                                                  iterations=n_trials))
        # ts sampler
        ts_counts.append(ib_sampler.ts_ib_sampler(productions, 
                                                  rep=ts_rep,
                                                  rep_new=ts_rep_new,
                                                  data=full_data,
                                                  test_scenes=test_scenes,
                                                  bv=bv_h_init,
                                                  start=h_init,
                                                  end=h_rev,
                                                  Dwin=Dwin_post,
                                                  feat_probs=feat_probs_post,
                                                  epsilon=epsilon,
                                                  out_penalizer=out_penalizer,
                                                  lam=lam,
                                                  iterations=n_trials))
        
        with open('sim_results/exp_1_tr_248_ib_sampler_penalize_' + str(out_penalizer) + '_lambda_' + str(lam) + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(tr_counts, f, ensure_ascii=False, indent=4)

        with open('sim_results/exp_1_ts_248_ib_sampler_penalize_' + str(out_penalizer) + '_lambda_' + str(lam) + core + '.json', 'w', encoding='utf-8') as f:
            json.dump(ts_counts, f, ensure_ascii=False, indent=4)