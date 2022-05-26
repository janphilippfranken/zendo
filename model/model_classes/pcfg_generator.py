import abc
import numpy as np
import pandas as pd
import re
import random as rd

from model_classes.rules import Rules


class PCFGTemplate(Rules, metaclass=abc.ABCMeta):
     
    @abc.abstractmethod
    def probs_list(self) -> list:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def pd_options(self) -> dict:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def generate_res(self) -> dict:
        """ generate hypotheses by string rewriting.
          Args:
          Returns:
        """
        raise NotImplementedError()
        
        
class PCFG(PCFGTemplate):
    
    def probs_list(self, probs):
        """ See base class. """
        prod_l = []
        for key in probs.keys():
            if isinstance(probs[key], list): 
                prod_l.append(probs[key])
            elif isinstance(probs[key], dict):
                keys_nested = probs[key].keys()
                cover_list = []
                for key_nested in keys_nested:
                    cover_list.append(np.sum(probs[key][key_nested]))
                    prod_l.append(probs[key][key_nested])
                prod_l.append(cover_list)
        return prod_l
    
    def pd_options(self, pds):
        """ See base class. """
        keys = pds.keys()
        pd_opts = {}
        for i in keys:
            if isinstance(pds[i], list):   
                pd_opt = [0] * len(pds[i])
                pd_opts[i] = pd_opt
            elif isinstance(pds[i], dict):
                keys_nested = pds[i].keys()
                pd_opts_nested = {}
                for i_2 in keys_nested:
                    pd_opt_nested = [0] * len(pds[i][i_2])
                    pd_opts_nested[i_2] = pd_opt_nested
                pd_opts[i] = pd_opts_nested
        return pd_opts

    def generate_res(self, productions=None, start="S", prec=pd.DataFrame({"from": [], "to": [], "toix": [], "li": []}), bound_vars=[], feat_probs=[np.repeat(1/3, 3), np.repeat(1/3, 3), np.repeat(1/4, 4), np.repeat(1/2, 2)], Swin = np.repeat(1/3, 3), Awin = np.repeat(1/2, 2), Bwin = np.repeat(1/3, 3), Cwin = np.repeat(1/5, 5), Cwin2 = np.repeat(1/5, 5), Dwin = np.repeat(1/4, 4), Ewin = np.repeat(1, 1), Gwin = np.repeat(1/4, 4), Hwin = np.repeat(1, 1), Iwin = np.repeat(1, 1), Jwin = np.repeat(1/2, 2), Kwin = np.repeat(1/4, 4), Lwin = np.repeat(1/3, 3), Mwin = np.repeat(1/3, 3)):
        """ See base class. """
        rule = start
        probs = self.pd_options(productions)
        probs_ordered = {}
        while any([i for i in ["S", "A"] if(i in [char for char in rule])]):
            srule = [char for char in rule]
            for i in range(0, len(srule)):
                if srule[i] == 'S':
                    bound_vars.append(["x" + str(i) for i in range(1, len(bound_vars) + 2)])
                    Sk = [re.sub("N", str(len(bound_vars)), i) for i in productions["S"]]
                    Sw = Swin
                    ix = np.random.choice(np.arange(0, len(productions["S"])), 1, p = Sw)
                    replacement = Sk[int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "S", "to": productions["S"][int(ix)], "toix": ix, "li": Sw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["S"][int(ix)] += 1
                    if "S" in probs_ordered:
                        probs_ordered["S"].append(int(ix))
                    else:
                        probs_ordered["S"] = []
                        probs_ordered["S"].append(int(ix))
                if srule[i] == "A":
                    Aw = Awin
                    if len(bound_vars) >= 3:
                        Aw = [1,0]
                    ix = np.random.choice(np.arange(0, len(productions["A"])), 1, p = Aw)
                    replacement = productions["A"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "A", "to": replacement, "toix": ix, "li": Aw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["A"][int(ix)] += 1
                    if "A" in probs_ordered:
                        probs_ordered["A"].append(int(ix))
                    else:
                        probs_ordered["A"] = []
                        probs_ordered["A"].append(int(ix))
        while any([i for i in ["B", "C", "D", "E", "G", "H", "I", "J", "K", "L", "M"] if(i in [char for char in rule])]):
            srule = [char for char in rule]
            for i in range(0, len(srule)):
                """ for B"""
                if srule[i] == 'B':
                    Bw = Bwin
                    if np.sum(prec['from'] == 'B') > 10:
                        Bw = [1,0,0]
                    ix = np.random.choice(np.arange(0, len(productions["B"])), 1, p = Bw)
                    replacement = productions["B"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "B", "to": replacement, "toix": ix, "li": Bw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["B"][int(ix)] += 1
                    if "B" in probs_ordered:
                        probs_ordered["B"].append(int(ix))
                    else:
                        probs_ordered["B"] = []
                        probs_ordered["B"].append(int(ix))
                if srule[i] == 'C':
                    Cw = Cwin
                    if len(bound_vars) < 2:
                        Ck = ['Z.equal(x1, D)', 'K(x1, E)']
                        replacement = rd.choice(Ck)
                        Cw = [.5,.5]
                    elif len(bound_vars) >= 2:
                        Cw = Cwin2
                        reps = np.random.choice(np.arange(0, len(bound_vars)), 2)
                        bound_vars_d = list(range(1, len(bound_vars)+1))
                        rand_ind = bound_vars_d.index(rd.choice(bound_vars_d))
                        Ck = [re.sub("N", str(bound_vars_d[rand_ind]), i) for i in productions["C"]]
                        del(bound_vars_d[rand_ind])
                        rand_ind = bound_vars_d.index(rd.choice(bound_vars_d))
                        Ck = [re.sub("O", str(bound_vars_d[rand_ind]), i) for i in Ck]
                    ix = np.random.choice(np.arange(0, len(Ck)), 1, p = Cw)
                    replacement = Ck[int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "C", "to": Ck[int(ix)], "toix": ix, "li": Cw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["C"][int(ix)] += 1
                    if "C" in probs_ordered:
                        probs_ordered["C"].append(int(ix))
                    else:
                        probs_ordered["C"] = []
                        probs_ordered["C"].append(int(ix))
                if srule[i] == 'D':
                    Dw = Dwin
                    ix = np.random.choice(np.arange(0, len(productions["D"])), 1, p = Dw)
                    feature = list(productions["D"].keys())[int(ix)]
                    feat_probs_trial = feat_probs[int(ix)]
                    vix = np.random.choice(np.arange(0, len(productions["D"][feature])), 1, p=feat_probs_trial)
                    value = productions["D"][feature][int(vix)]
                    replacement = str(value) + "," + "'" + feature + "'"
                    prec = pd.concat([prec, pd.DataFrame({"from": "Ef", "to": feature, "toix": ix, "li": Dw[int(ix)]})])
                    prec = pd.concat([prec, pd.DataFrame({"from": "Ev", "to": value, "toix": vix, "li": 1/len(productions["D"][feature])})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["D"][feature][int(vix)] += 1
                    if "D" in probs_ordered:
                        probs_ordered["D"].append(int(ix))
                    else:
                        probs_ordered["D"] = []
                        probs_ordered["D"].append(int(ix))
                    if "D" + (str(ix[0])) in probs_ordered:
                        probs_ordered["D" + (str(ix[0]))].append(int(vix))
                    else:
                        probs_ordered["D" + (str(ix[0]))] = []
                        probs_ordered["D" + (str(ix[0]))].append(int(vix))
                if srule[i] == 'E':
                    Ew = Ewin
                    ix = np.random.choice(np.arange(0, len(productions["E"])), 1, p = Ew)
                    feature = list(productions["E"].keys())[int(ix)]
                    vix = np.random.choice(np.arange(0, len(productions["E"][feature])), 1, p=feat_probs[1])
                    value = productions["E"][feature][int(vix)]
                    replacement = str(value) + "," + "'" + feature + "'"
                    prec = pd.concat([prec, pd.DataFrame({"from": "Ef", "to": feature, "toix": ix, "li": Ew[int(ix)]})])
                    prec = pd.concat([prec, pd.DataFrame({"from": "Ev", "to": value, "toix": vix, "li": 1/len(productions["E"][feature])})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["E"][feature][int(vix)] += 1
                    if "E" in probs_ordered:
                        probs_ordered["E"].append(int(ix))
                    else:
                        probs_ordered["E"] = []
                        probs_ordered["E"].append(int(ix))
                    if "E" + (str(ix[0])) in probs_ordered:
                        probs_ordered["E" + (str(ix[0]))].append(int(vix))
                    else:
                        probs_ordered["E" + (str(ix[0]))] = []
                        probs_ordered["E" + (str(ix[0]))].append(int(vix))
                if srule[i] == 'G':
                    Gw = Gwin
                    ix = np.random.choice(np.arange(0, len(productions["G"])), 1, p = Gw)
                    replacement = productions["G"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "G", "to": productions["G"][int(ix)], "toix": ix, "li": Gw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["G"][int(ix)] += 1
                    if "G" in probs_ordered:
                        probs_ordered["G"].append(int(ix))
                    else:
                        probs_ordered["G"] = []
                        probs_ordered["G"].append(int(ix))
                if srule[i] == 'H':
                    Hw = Hwin
                    ix = np.random.choice(np.arange(0, len(productions["H"])), 1, p = Hw)
                    replacement = productions["H"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "H", "to": productions["H"][int(ix)], "toix": ix, "li": Hw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["H"][int(ix)] += 1
                    if "H" in probs_ordered:
                        probs_ordered["H"].append(int(ix))
                    else:
                        probs_ordered["H"] = []
                        probs_ordered["H"].append(int(ix))
                if srule[i] == 'I':
                    Iw = Iwin
                    ix = 0
                    replacement = productions["I"][ix]
                    prec = pd.concat([prec, pd.DataFrame({"from": "I", "to": productions["I"], "toix": ix, "li": Iw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["I"][int(ix)] += 1
                    if "I" in probs_ordered:
                        probs_ordered["I"].append(int(ix))
                    else:
                        probs_ordered["I"] = []
                        probs_ordered["I"].append(int(ix))
                if srule[i] == 'J':
                    Jw = Jwin
                    if len(productions["J"]) > 1:
                        ix = np.random.choice(np.arange(0, len(productions["J"])), 1, p = Jw)
                    else:
                        ix = 0
                    replacement = productions["J"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "J", "to": productions["J"][int(ix)], "toix": ix, "li": Jw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["J"][int(ix)] += 1
                    if "J" in probs_ordered:
                        probs_ordered["J"].append(int(ix))
                    else:
                        probs_ordered["J"] = []
                        probs_ordered["J"].append(int(ix))
                if srule[i] == 'K':
                    Kw = Kwin
                    ix = np.random.choice(np.arange(0, len(productions["K"])), 1, p = Kw)
                    replacement = productions["K"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "K", "to": productions["K"][int(ix)], "toix": ix, "li": Kw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["K"][int(ix)] += 1
                    if "K" in probs_ordered:
                        probs_ordered["K"].append(int(ix))
                    else:
                        probs_ordered["K"] = []
                        probs_ordered["K"].append(int(ix))
                if srule[i] == 'L':
                    Lw = Lwin
                    ix = np.random.choice(np.arange(0, len(productions["L"])), 1, p = Lw)
                    replacement = productions["L"][int(ix)]
                    prec = pd.concat([prec, pd.DataFrame({"from": "L", "to": productions["L"][int(ix)], "toix": ix, "li": Lw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["L"][int(ix)] += 1
                    if "L" in probs_ordered:
                        probs_ordered["L"].append(int(ix))
                    else:
                        probs_ordered["L"] = []
                        probs_ordered["L"].append(int(ix))
                if srule[i] == 'M':
                    Mw = Mwin
                    ix = np.random.choice(np.arange(0, len(productions["M"])), 1, p = Mw)
                    replacement = str(productions["M"][int(ix)])
                    prec = pd.concat([prec, pd.DataFrame({"from": "M", "to": productions["M"][int(ix)], "toix": ix, "li": Mw[int(ix)]})])
                    srule[i] = replacement
                    rule = "".join(srule)
                    probs["M"][int(ix)] += 1
                    if "M" in probs_ordered:
                        probs_ordered["M"].append(int(ix))
                    else:
                        probs_ordered["M"] = []
                        probs_ordered["M"].append(int(ix))
        return {"rule": rule, "prec": prec, "probs": probs, "prod_l": self.probs_list(probs), "prod_d": probs_ordered, "bv": bound_vars}