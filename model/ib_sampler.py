import numpy as np
import pandas as pd

from model_classes.pcfg_generator import PCFG
from model_classes.bayesian_model import BayesianModel


from mcmc_sampler import MCMCSampler


Z = PCFG()
bm = BayesianModel()

class IBSSampler(MCMCSampler):   
    
    def check_labels(self, data, t, t_prime):
        res_t = []
        res_t_prime = []
        global X
        for scene in data:
            X = []                        
            for object_idx, object_id in enumerate(scene['ids']): 
                cone_object = {"id": object_id, 
                               "colour":  scene['colours'][object_idx], 
                               "size":  scene['sizes'][object_idx], 
                               "orientation":  scene['orientations'][object_idx],
                               "contact":  scene['contact'][object_idx], 
                               "grounded":  scene['grounded'][object_idx]}
                X.append(cone_object)   
            if eval(t["rule"]) != eval(t_prime["rule"]):
                return False
        return True
        
    def tr_ib_sampler(self, productions, replacements, data, test_scenes, bv, start="S", end="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3), np.repeat(1/4, 4), np.repeat(1/2, 2)], lam = 4, out_penalizer=4, epsilon = 100, iterations=10):
        """ See base class."""
        n_edits = {}
        h_rev = {"rule": end, "prec": self.get_prec_recursively(self.string_to_list(end))}
        for i in range(iterations):
            n_edits[i] = []
            for j in range(epsilon):
                found_h_rev = False
                t = {"rule": start, "prec": self.get_prec_recursively(self.string_to_list(start)), 'bv': bv}
                edits = np.random.poisson(lam = lam) + 1
                for edit in range(edits):
                    t_prime_info = self.regrow_tree(t, productions, replacements) 
                    t_prime = Z.generate_res(productions, t_prime_info["t_prime_rule"], bound_vars=t_prime_info["t_prime_bv"], prec=t_prime_info["t_prime_prec"])
                    t_prime['prec'] = self.get_prec_recursively(self.string_to_list(t_prime['rule']))
                    valid_rule = False
                    while valid_rule == False:
                        try:
                            out_t, out_t_prime = self.get_outlier(data, t, t_prime)
                            valid_rule = True
                        except:
                            print('tr rule not valid')
                            print(t_prime['rule'])
                            t_prime_info = self.regrow_tree(t, productions, replacements) 
                            t_prime = Z.generate_res(productions, t_prime_info["t_prime_rule"], bound_vars=t_prime_info["t_prime_bv"], prec=t_prime_info["t_prime_prec"])
                            t_prime['prec'] = self.get_prec_recursively(self.string_to_list(t_prime['rule']))
                    deriv_t = np.array(t["prec"]["li"])
                    deriv_t_prime = np.array(t_prime["prec"]["li"])
                    ll_ratio = bm.ll_ratio(deriv_t, deriv_t_prime, out_t, out_t_prime, out_penalizer)
                    if np.minimum(1, ll_ratio) > np.random.rand():
                        t = t_prime
                if self.check_labels(test_scenes, t, h_rev) is True:
                    n_edits[i].append(j)
                    found_h_rev = True
                    break
                elif j == epsilon - 1:
                    n_edits[i].append(epsilon)
        return n_edits
        
    
    def ts_ib_sampler(self, productions, rep, rep_new, data, test_scenes, bv, start="S", end="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3),np.repeat(1/4, 4),np.repeat(1/2, 2)], lam = 4, out_penalizer=4, epsilon = 100, iterations=10):
        """ See base class."""
        n_edits = {}
        h_rev = {"rule": end, "prec": self.get_prec_recursively(self.string_to_list(end))}
        for i in range(iterations):
            n_edits[i] = []
            for j in range(epsilon):
                found_h_rev = False
                t = {"rule": start, "prec": self.get_prec_recursively(self.string_to_list(start)), 'bv': bv}
                edits = np.random.poisson(lam = lam) + 1
                for edit in range(edits):
                    t_prime_info = self.tree_surgery(t, productions, rep, rep_new) 
                    t_prime = Z.generate_res(productions, t_prime_info["t_prime_rule"], bound_vars=t_prime_info["t_prime_bv"])
                    t_prime['prec'] = self.get_prec_recursively(self.string_to_list(t_prime['rule']))
                    valid_rule = False
                    while valid_rule == False:
                        try:
                            out_t, out_t_prime = self.get_outlier(data, t, t_prime)
                            valid_rule = True
                        except:
                            print('ts rule not valid')
                            print(t_prime['rule'])
                            t_prime_info = self.tree_surgery(t, productions, rep, rep_new) 
                            t_prime = Z.generate_res(productions, t_prime_info["t_prime_rule"], bound_vars=t_prime_info["t_prime_bv"])
                            t_prime['prec'] = self.get_prec_recursively(self.string_to_list(t_prime['rule']))
                    deriv_t = np.array(t["prec"]["li"])
                    deriv_t_prime = np.array(t_prime["prec"]["li"])
                    ll_ratio = bm.ll_ratio(deriv_t, deriv_t_prime, out_t, out_t_prime, out_penalizer)
                    if np.minimum(1, ll_ratio) > np.random.rand():
                        t = t_prime
                if self.check_labels(test_scenes, t, h_rev) is True:
                    n_edits[i].append(j)
                    found_h_rev = True
                    break
                elif j == epsilon - 1:
                    n_edits[i].append(epsilon)
        return n_edits

