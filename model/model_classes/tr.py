import abc
import copy
import random as rd
import pandas as pd

from model_classes.reverse_rule import ReverseRule


class TRTemplate(ReverseRule, metaclass=abc.ABCMeta):
    '''hard-coded class that implements regeneration proposals''' 
    
    @abc.abstractmethod
    def regrow_tree(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    
class TR(TRTemplate):
    
    def regrow_tree(self, t, prod, replacements, non_terminal_list =  ['S','A','C','B']):
        """ See base class. """
        productions = copy.deepcopy(prod)
        t_rule = t['rule']        
        t_prec = t['prec']
        t_prod = t_prec['from']
        t_bv = t['bv']             
        t_prime_bv = t_bv.copy()   
        t_list = self.string_to_list(t_rule) 
        ind_nested = self.get_inds(t_list)  
        t_prod_inds = list(range(0, len(t_prod)))
        nt_inds = [index for index, prod in zip(t_prod_inds, t_prod) if prod in non_terminal_list]
        nt_ind = rd.choice(nt_inds)  
        nt = t_prod[nt_ind]
        if len(t_bv) == 1:
            productions["C"] = ['Z.equal(x1, D)', 'K(x1, E)']
        p_ind = rd.choice(list(range(0, len(productions[nt]))))
        new_p = productions[nt][p_ind]
        new_prod_prob = 1/len(productions[nt])
        cut = 0 
        if nt == "B" or nt == "C":
            b_inds = [index for index,prod in zip(t_prod_inds,t_prod) if prod in [nt]]
            n_b_select = b_inds.index(nt_ind)  
            all_inds = list(range(0, len(ind_nested)))
            b_inds = [index for index,prod in zip(all_inds,ind_nested) if prod in replacements[nt]]
            spec_ind = ind_nested[b_inds[n_b_select]+1]
            spec_ind_plus = spec_ind.copy()
            spec_ind_plus[len(spec_ind_plus)-1] += 1
            bound_vars = list(range(1, len(t_prime_bv)+1))
            for ch in ["N", "O"]:
                if ch in new_p:
                    rand_ind = bound_vars.index(rd.choice(bound_vars))
                    new_p = new_p.replace(ch, str(bound_vars[rand_ind]))
                    if len(t_bv) >= 2:
                        del(bound_vars[rand_ind])
            spec_ind_l = [str([ind]) for ind in spec_ind]
            spec_ind_plus_l = [str([ind]) for ind in spec_ind_plus]
            spec_ind_s = ''.join(spec_ind_l)
            spec_ind_plus_s = ''.join(spec_ind_plus_l)
            t_prime_list = copy.deepcopy(t_list)
            exec('t_prime_list' + spec_ind_s + '=' + 'new_p') # this is not ideal just temporary solution 
            del_in_prec = eval('t_prime_list' + spec_ind_plus_s) 
            exec('del(t_prime_list' + spec_ind_plus_s + ')')
            t_prec_to = list(t_prec['to'])
            t_prec_from = list(t_prec['from'])
            t_prime_rule = self.list_to_string(t_prime_list)
            t_prime_prec = t_prec
            t_prime_prec.at[nt_ind, 'from'] = nt
            t_prime_prec.at[nt_ind, 'to'] = new_p
            t_prime_prec.at[nt_ind, 'toix'] = float(p_ind)
            t_prime_prec.at[nt_ind, 'li'] = new_prod_prob
            del_in_prec = self.get_list(del_in_prec)
            del_in_prec_2 = [str(i) if isinstance(i, int) else "'" + i + "'" if isinstance(i, str) and '.' not in i else i for i in del_in_prec]
            del_in_prec = del_in_prec + del_in_prec_2
            prec_inds = list(range(0, len(t_prec['to'])))
            to_ind = 0
            for to in t_prec_to:
                for ch in ["("]:
                    if isinstance(to, str):
                        if ch in to:
                            cut = to.index(ch)
                            to = to[:cut]
                to_ind += 1
            drop_inds = [i for i,to in zip(prec_inds,t_prec_to) if to in del_in_prec and i > nt_ind]
            drop_inds_new = []
            for i in drop_inds:
                if t_prec_from[i] != "M":
                    drop_inds_new.append(i)
            drop_inds_new = list(set(drop_inds_new)) 
            if nt == "C" or "B":
                t_prime_prec = t_prime_prec.drop(drop_inds_new)
            return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "nt_ind": nt_ind, "nt": nt}
        elif nt == 'A':
            t_prime_list = t_list
            if nt_ind == 5:
                for ch in ["S"]:
                    if ch in new_p:
                        new_p = new_p.replace(ch, "B")
                t_prime_list[1][4][4][3] = new_p
                del(t_prime_list[1][4][4][4])
            elif nt_ind == 3:
                t_prime_bv = t_prime_bv[:2]
                t_prime_list[1][4][3] = new_p
                del(t_prime_list[1][4][4])
            elif nt_ind == 1:
                t_prime_bv = t_prime_bv[:1]
                t_prime_list[1][3] = new_p
                del(t_prime_list[1][4])
        elif nt == 'S':
            t_prime_list = t_list
            sum_s = sum([1 for a in t_prod if a in ["S"]])
            if nt_ind == 4:
                t_prime_bv = t_prime_bv[:3]
                for ch in ["A"]:
                    if ch in new_p:
                        new_p = new_p.replace(ch, "B")
                for ch in ["N"]:
                    if ch in new_p:
                        new_p = new_p.replace(ch, "3")
                t_prime_list[1][4][3] = new_p
                del(t_prime_list[1][4][4])
            elif nt_ind == 2:
                t_prime_bv = t_prime_bv[:2]
                for ch in ["N"]:
                    if ch in new_p:
                        new_p = new_p.replace(ch, "2")
                t_prime_list[1][3] = new_p
                del(t_prime_list[1][4])
            elif nt_ind == 0:
                t_prime_prec = pd.DataFrame({"from": [], "to": [], "toix": [], "li": []})
                t_prime_rule = "S"
                t_prime_bv = []
                t_prime_list[0] = "S"
                del(t_prime_list[1])
                return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "nt_ind": nt_ind, "nt": nt}
        t_prime_rule = self.list_to_string(t_prime_list)
        t_prime_prec = copy.deepcopy(t_prec)
        t_prime_prec.at[nt_ind, 'from'] = nt
        t_prime_prec.at[nt_ind, 'to'] = new_p
        t_prime_prec.at[nt_ind, 'toix'] = float(p_ind)
        t_prime_prec.at[nt_ind, 'li'] = new_prod_prob
        if nt == "S" or nt == "A":
            t_prime_rule = self.list_to_string(t_prime_list)
            t_prime_prec = t_prime_prec.loc[:nt_ind-cut:]
            return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "nt_ind": nt_ind, "nt": nt}
        return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "t_prime_list": t_prime_list}