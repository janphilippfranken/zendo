import abc
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter

from model_classes.bayesian_model import BayesianModel
from model_classes.pcfg_generator import PCFG
from model_classes.ts import TS 


Z = PCFG()
bm = BayesianModel()


class MCMCSampler(TS):
    
    def get_outlier(self, data, t, t_prime):
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
            res_t.append(eval(t["rule"]) != scene['follow_rule'])             
            res_t_prime.append(eval(t_prime["rule"]) != scene['follow_rule'])
        return np.sum(res_t), np.sum(res_t_prime)

    def generic_sampler(self, productions, replacements, data, start="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3),np.repeat(1/4, 4),np.repeat(1/2, 2)], out_penalizer=4, iterations=10):
        """ See base class."""
        t = Z.generate_res(productions=productions, start=start, prec=start_frame, bound_vars=[], Dwin=Dwin, feat_probs=feat_probs)
        t['prec'] = self.get_prec_recursively(self.string_to_list(t['rule']))
        rules = []
        for i in range(iterations):
            t_prime_info = self.regrow_tree(t, productions, replacements) 
            t_prime = Z.generate_res(productions, t_prime_info["t_prime_rule"], bound_vars=t_prime_info["t_prime_bv"], prec=t_prime_info["t_prime_prec"])
            t_prime['prec'] = self.get_prec_recursively(self.string_to_list(t_prime['rule']))
            out_t, out_t_prime = self.get_outlier(data, t, t_prime)
            deriv_t = np.array(t["prec"]["li"])
            deriv_t_prime = np.array(t_prime["prec"]["li"])
            ll_ratio = bm.ll_ratio(deriv_t, deriv_t_prime, out_t, out_t_prime, out_penalizer)
            if np.minimum(1, ll_ratio) > np.random.rand():
                t = t_prime
            rules.append(t['rule'])
        return dict(Counter(rules))
    
    def surgery_sampler(self, productions, rep, rep_new, data, start="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3),np.repeat(1/4, 4),np.repeat(1/2, 2)], out_penalizer=4, iterations=10):
        """ See base class."""
        t = Z.generate_res(productions=productions, start=start, prec=start_frame, bound_vars=[], Dwin=Dwin, feat_probs=feat_probs)
        t['prec'] = self.get_prec_recursively(self.string_to_list(t['rule']))
        rules = []
        for i in range(iterations):
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
            rules.append(t['rule'])
        return dict(Counter(rules))
    
    def tr_sampler(self, productions, replacements, data, bv, start="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3),np.repeat(1/4, 4),np.repeat(1/2, 2)], lam = 4, out_penalizer=4, iterations=10):
        """ See base class."""
        rules = []
        for i in range(iterations):
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
            rules.append(t['rule'])
        return dict(Counter(rules))
    
    def ts_sampler(self, productions, rep, rep_new, data, bv, start="S", start_frame=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), Dwin=np.repeat(1/4, 4), feat_probs=[np.repeat(1/3, 3),np.repeat(1/3, 3),np.repeat(1/4, 4),np.repeat(1/2, 2)], lam = 4, out_penalizer=4, iterations=10):
        """ See base class."""
        rules = []
        for i in range(iterations):
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
                out_t, out_t_prime = self.get_outlier(data, t, t_prime)
                deriv_t = np.array(t["prec"]["li"])
                deriv_t_prime = np.array(t_prime["prec"]["li"])
                ll_ratio = bm.ll_ratio(deriv_t, deriv_t_prime, out_t, out_t_prime, out_penalizer)                
                if np.minimum(1, ll_ratio) > np.random.rand():
                    t = t_prime
            rules.append(t['rule'])
        return dict(Counter(rules))