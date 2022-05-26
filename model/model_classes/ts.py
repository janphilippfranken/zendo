import abc
import random as rd
import copy
import numpy as np

from model_classes.tr import TR


class TSTemplate(TR, metaclass=abc.ABCMeta):
    '''hard-coded class that implements surgical proposals''' 
     
    @abc.abstractmethod
    def flattenList(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def insertList(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def tree_surgery(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    
class TS(TSTemplate):
    
    def flattenList(self, listToFlatten, outerList, LIST):
        """ See base class. """
        for item in listToFlatten:
            outerList.append(item)
        outerList.remove(listToFlatten)

    def insertList(self, listToFlatten, outerList, LIST, insind):
        """ See base class. """
        insind2 = 0
        for item in listToFlatten:
            outerList.insert(insind + insind2, item)
            insind2 += 1
        outerList.remove(listToFlatten)

    def tree_surgery(self, t, productions, rep, rep_n, non_terminal_list = ['S','A','C','B']):
        """ See base class. """
        replacements = copy.deepcopy(rep)
        replacements_new = copy.deepcopy(rep_n)
        t_rule = t['rule']
        t_bv = t['bv']
        t_prime_bv = t_bv
        t_prec = self.get_prec_recursively(self.string_to_list(t_rule))
        t_prime_bv = t_bv.copy()            
        t_list = self.string_to_list(t_rule) 
        ind_nested = self.get_inds(t_list)     
        t_prod = t_prec["from"]
        t_prod_inds = list(range(0, len(t_prod)))
        nt_inds = [index for index, prod in zip(t_prod_inds,t_prod) if prod in non_terminal_list]
        nt_ind = rd.choice(nt_inds)   
        nt = t_prod[nt_ind]
        new_inds = [index for index,prod in zip(t_prod_inds,t_prod) if prod in [nt]] 
        n_ind_select = new_inds.index(nt_ind)    
        all_inds = list(range(0, len(ind_nested)))
        nt_inds = [index for index, prod in zip(all_inds,ind_nested) if prod in replacements[nt]]
        spec_ind = ind_nested[nt_inds[n_ind_select]+1]
        spec_ind_l = [str([ind]) for ind in spec_ind]
        spec_ind_s = ''.join(spec_ind_l)
        t_prime_list = copy.deepcopy(t_list)
        t_component = eval('t_list' + spec_ind_s)
        replacements['B'] = ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater','Z.and_operator','Z.or_operator','Z.not_operator']
        replacements_new['B'] = ['C','J','Z.not_operator']
        replacements_new['C'] = ['Z.equal', 'K', 'Z.equal', 'K', 'Z.hor_operator']
        replacements['C'] = ['Z.equal', 'K', 'Z.equal', 'K', 'Z.hor_operator']
        replacements['K'] = ['Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']
        replacements['J'] = ['Z.and_operator','Z.or_operator']
        if len(t_bv) == 1:
            replacements['C'] = ['Z.equal', 'K']
            replacements_new['C'] = ['Z.equal', 'K']
        p_ind = rd.choice(list(range(0, len(replacements_new[nt]))))
        new_p = replacements_new[nt][p_ind]
        if nt == 'S':
            if np.random.rand() > 1/4: # to avoid getting trapped, regrow new proposal with prob 1/n_quantifiers + 1 
                t_prime_info = self.regrow_tree(t, productions, replacements, non_terminal_list=['S'])
                return t_prime_info
            exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
            if t_component in ['Z.exists','Z.forall'] and new_p in ['Z.exists','Z.forall'] or t_component in ['Z.atleast','Z.atmost','Z.exactly'] and new_p in ['Z.atleast','Z.atmost','Z.exactly']:
                t_prime_prec = self.get_prec_recursively(t_prime_list)
                t_prime_rule = self.list_to_string(t_prime_list)
                return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "t_prime_list": t_prime_list}
            elif t_component in ['Z.exists','Z.forall'] and new_p in ['Z.atleast','Z.atmost','Z.exactly']:
                if n_ind_select == 0:
                    t_prime_list[1][-1] = rd.choice(productions["M"])
                    t_prime_list[1].append('X')
                elif n_ind_select == 1:
                    t_prime_list[1][4][-1] = rd.choice(productions["M"])
                    t_prime_list[1][4].append('X')
                elif n_ind_select == 2:
                    t_prime_list[1][4][4][-1] = rd.choice(productions["M"])
                    t_prime_list[1][4][4].append('X')
                t_prime_prec = self.get_prec_recursively(t_prime_list)
                t_prime_rule = self.list_to_string(t_prime_list)
                return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "t_prime_list": t_prime_list}
            elif t_component in ['Z.atleast','Z.atmost','Z.exactly'] and new_p in ['Z.exists','Z.forall']:
                if n_ind_select == 0:
                    del(t_prime_list[1][-2])
                elif n_ind_select == 1:
                    del(t_prime_list[1][4][-2])
                elif n_ind_select == 2:
                    del(t_prime_list[1][4][4][-2])
                t_prime_prec = self.get_prec_recursively(t_prime_list)
                t_prime_rule = self.list_to_string(t_prime_list)
                return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "t_prime_list": t_prime_list}
        if nt == 'A':
            t_prime_info = self.regrow_tree(t, productions, replacements,non_terminal_list=['A'])
            return t_prime_info
        if nt == 'B':
            if t_component in ['Z.and_operator', 'Z.or_operator'] and new_p in ['J']:
                choices = ['Z.and_operator', 'Z.or_operator']
                t_component_ind = choices.index(t_component)
                del(choices[t_component_ind])
                new_p = choices[0]
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
                t_prime_rule = self.list_to_string(t_prime_list)
                t_prime_prec = self.get_prec_recursively(t_prime_list)
                return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": t_prime_prec, "t_prime_list": t_prime_list}
            if new_p in ['Z.not_operator'] and t_component in ['Z.and_operator', 'Z.or_operator']:
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
                spec_ind_l_2 = spec_ind.copy()
                spec_ind_l_2[-1] = spec_ind_l_2[-1] + 1
                spec_ind_l_2.append(spec_ind_l_2[-1] + 2)
                spec_ind_l_2 = [str([i]) for i in spec_ind_l_2[:len(spec_ind_l_2)-2]] + spec_ind_l_2[len(spec_ind_l_2)-2:]
                final_index = '[' + str(spec_ind_l_2[-2]) + ':' + str(spec_ind_l_2[-1]) + ']'
                spec_ind_l_2[len(spec_ind_l_2)-2:] = final_index
                spec_ind_s_2 = ''.join(spec_ind_l_2)
                new_list_ind = spec_ind[-1] + 1
                spec_ind_l = spec_ind_l[:len(spec_ind_l)-1]
                spec_ind_s = ''.join(spec_ind_l)
                exec('t_prime_list' + spec_ind_s + '.insert(new_list_ind,t_component)')
                exec('t_prime_list' +spec_ind_s_2+' = [t_prime_list' + spec_ind_s_2+']')
            elif new_p in ['Z.not_operator'] and t_component not in ['Z.and_operator', 'Z.or_operator']:
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
                spec_ind_l_2 = spec_ind.copy()
                spec_ind_l_2[-1] = spec_ind_l_2[-1] + 1
                spec_ind_l_2.append(spec_ind_l_2[-1] + 2)
                spec_ind_l_2 = [str([i]) for i in spec_ind_l_2[:len(spec_ind_l_2)-2]] + spec_ind_l_2[len(spec_ind_l_2)-2:]
                final_index = '[' + str(spec_ind_l_2[-2]) + ':' + str(spec_ind_l_2[-1]) + ']'
                spec_ind_l_2[len(spec_ind_l_2)-2:] = final_index
                spec_ind_s_2 = ''.join(spec_ind_l_2)
                new_list_ind = spec_ind[-1] + 1
                spec_ind_l = spec_ind_l[:len(spec_ind_l)-1]
                spec_ind_s = ''.join(spec_ind_l)
                exec('t_prime_list' + spec_ind_s + '.insert(new_list_ind,t_component)')
                exec('t_prime_list' +spec_ind_s_2+' = [t_prime_list' + spec_ind_s_2+']')
            elif t_component in ['Z.and_operator', 'Z.or_operator'] and new_p in ['C']:
                first_component = spec_ind_l.copy()
                first_component[-1] = str([spec_ind[-1] + 1])
                first_component.append('[0]')
                second_component = spec_ind_l.copy()
                second_component[-1] = str([spec_ind[-1] + 1])
                second_component.append('[2]')
                first_component_s = ''.join(first_component)
                second_component_s = ''.join(second_component)
                f_c = eval('t_list' + first_component_s)
                s_c = eval('t_list' + second_component_s)
                keep = rd.choice([1,2])
                if keep == 1:
                    spec_ind_2 = first_component_s[:-3]
                    exec('del(t_prime_list' + spec_ind_2 + '[2:])')
                    exec('del(t_prime_list' + spec_ind_s + ')')
                    spec_ind_2 = spec_ind_2[:-3]
                    spec_ind_3 = spec_ind_s
                    spec_ind_check = spec_ind_s[:-3]
                    if 'Z.not_operator' not in eval('t_prime_list' + spec_ind_check):
                        spec_ind_2 = spec_ind_s[:-3]
                        self.insertList(eval('t_prime_list' + spec_ind_s),eval('t_prime_list' + spec_ind_2),t_prime_list,int(spec_ind_s[-2]))
                    else:
                        ind_not = eval('t_prime_list' + spec_ind_check +  '.index("Z.not_operator")')
                        ind_item = int(spec_ind_s[-2:-1])
                        mid_obj_ind = spec_ind_s[:-3] + str([int(spec_ind_s[-2])-1])
                        if ind_item - 2 != ind_not or eval('t_prime_list'+mid_obj_ind) != 'Z.not_operator':
                            spec_ind_2 = spec_ind_s[:-3]
                            self.insertList(eval('t_prime_list' + spec_ind_s),eval('t_prime_list' + spec_ind_2),t_prime_list,int(spec_ind_s[-2]))
                elif keep == 2:
                    exec('t_prime_list' + spec_ind_s + '=' + 's_c')
                    spec_ind_2 = second_component_s[:-3]
                    exec('del(t_prime_list' + spec_ind_2 + '[:3])')
                    spec_ind_3 = spec_ind_2 + '[0]'
                    self.flattenList(eval('t_prime_list' + spec_ind_3),eval('t_prime_list' + spec_ind_2),t_prime_list)
            elif t_component in ['Z.equal', 'Z.hor_operator'] and new_p in ['C']:
                choices = replacements_new['C']
                t_component_ind = choices.index(t_component)
                del(choices[t_component_ind])
                new_p = rd.choice(choices)
                if new_p == 'Z.hor_operator':
                    exec('del(t_prime_list' + spec_ind_s+')')
                    new_p = 'Z.hor_operator(xN,xO,I)'
                if new_p == 'K':
                    size_check_ind = spec_ind_l.copy()
                    size_check_ind[-1] = str([spec_ind[-1] + 1])
                    size_check_ind_safe = size_check_ind.copy()
                    size_check_ind = size_check_ind + ['[2]']
                    size_check_ind_s = ''.join(size_check_ind)
                    if eval('t_prime_list' + size_check_ind_s) == 'size':
                        new_p = rd.choice(replacements['K'])
                    else:
                        choices = ['K(xN, E)', 'K(xN, xO, H)']
                        if len(t_bv) == 1:
                            new_p = choices[0]
                        else:
                            new_p = rd.choice(choices)
                        exec('del(t_prime_list' + spec_ind_s+')')
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
            elif t_component in replacements['K'] and new_p in ['C']:
                choices = replacements['C']
                new_p = rd.choice(choices)
                if new_p == 'K':
                    t_component_ind = replacements['K'].index(t_component)
                    del(replacements['K'][t_component_ind])
                    new_p = rd.choice(replacements['K'])
                if new_p == 'Z.hor_operator':
                    exec('del(t_prime_list' + spec_ind_s+')')
                    new_p = 'Z.hor_operator(xN,xO,I)'
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
            elif t_component in ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater'] and new_p in ['J']:
                new_p = rd.choice(replacements['J'])
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
                spec_ind_l_2 = spec_ind.copy()
                spec_ind_l_2[-1] = spec_ind_l_2[-1] + 1
                spec_ind_l_2.append(spec_ind_l_2[-1] + 3)
                spec_ind_l_2 = [str([i]) for i in spec_ind_l_2[:len(spec_ind_l_2)-2]] + spec_ind_l_2[len(spec_ind_l_2)-2:]
                final_index = '[' + str(spec_ind_l_2[-2]) + ':' + str(spec_ind_l_2[-1]) + ']'
                spec_ind_l_2[len(spec_ind_l_2)-2:] = final_index
                spec_ind_s_2 = ''.join(spec_ind_l_2)
                new_list_ind = spec_ind[-1] + 1
                spec_ind_l = spec_ind_l[:len(spec_ind_l)-1]
                spec_ind_s = ''.join(spec_ind_l)
                inser_index = spec_ind_l_2.copy()
                inser_index[-4] = int(inser_index[-4]) + 2
                exec('t_prime_list' + spec_ind_s + '.insert(new_list_ind,t_component)')
                exec('t_prime_list' + spec_ind_s + '.insert(inser_index[-4],"C")')
                exec('t_prime_list' +spec_ind_s_2+' = [t_prime_list' + spec_ind_s_2+']')
                t_prime_rule = self.list_to_string(t_prime_list)
            if t_component in ['Z.not_operator'] and new_p in ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater', 'Z.and_operator', 'Z.or_operator']:
                new_spec_ind = spec_ind.copy()
                new_spec_ind[-1] = new_spec_ind[-1] + 1
                new_spec_ind_2 = new_spec_ind.copy()
                new_spec_ind_2.append(1)
                new_spec_ind_l = [str([i]) for i in new_spec_ind]
                new_spec_ind_l_2 = [str([i]) for i in new_spec_ind_2]
                new_spec_ind_s = ''.join(new_spec_ind_l)
                new_spec_ind_s_2 = ''.join(new_spec_ind_l_2)
                t_prime_list2 = copy.deepcopy(t_prime_list)
                exec('del(t_prime_list' + spec_ind_s + ')')
                spec_ind_check = spec_ind_s[:-3]
                spec_ind_check_2 = spec_ind_check + '['+ str(int(spec_ind_check[-2])-2) + ']'
                if 'Z.not_operator' not in eval('t_prime_list' + spec_ind_check):
                    spec_ind_2 = spec_ind_s[:-3]
                    self.insertList(eval('t_prime_list' + spec_ind_s),eval('t_prime_list' + spec_ind_2),t_prime_list,int(spec_ind_s[-2]))
                elif 'Z.not_operator' in eval('t_prime_list' + spec_ind_check):
                    ind_not = eval('t_prime_list' + spec_ind_check +  '.index("Z.not_operator")')
                    ind_item = int(spec_ind_s[-2:-1])
                    if ind_item - 2 != ind_not and ind_item -1 != ind_not:
                        spec_ind_2 = spec_ind_s[:-3]
                        self.insertList(eval('t_prime_list' + spec_ind_s),eval('t_prime_list' + spec_ind_2),t_prime_list,int(spec_ind_s[-2]))
                    else:
                        spec_ind_check = spec_ind_s[:-3]
                        spec_ind_check_2 = spec_ind_check[:-3]
                        item = eval('t_prime_list' + spec_ind_s)
                        item_out = eval('t_prime_list' + spec_ind_check)
                        item_out_out = eval('t_prime_list' + spec_ind_check_2)
                        if item_out_out[item_out_out.index(item_out)-1] in ['Z.and_operator', 'Z.or_operator']:
                            ind_not = eval('t_prime_list' + spec_ind_check +  '.index("Z.not_operator")')
                            ind_item = int(spec_ind_s[-2:-1])
                            ind_other = item_out_out.index(item_out)-1
                            mid_obj_ind = spec_ind_s[:-3] + str([int(spec_ind_s[-2])-1])
                            if ind_item - 2 != ind_not or eval('t_prime_list'+mid_obj_ind) != 'Z.not_operator':
                                spec_ind_2 = spec_ind_s[:-3]
                                self.insertList(eval('t_prime_list' + spec_ind_s),eval('t_prime_list' + spec_ind_2),t_prime_list,int(spec_ind_s[-2]))
            check_B = self.list_to_string(t_prime_list)
        if nt == 'C':
            if t_component in ['Z.equal', 'Z.hor_operator'] and new_p in replacements['C']:
                choices = replacements_new['C']
                t_component_ind = choices.index(t_component)
                del(choices[t_component_ind])
                new_p = rd.choice(choices)
                if new_p == 'Z.hor_operator':
                    exec('del(t_prime_list' + spec_ind_s+')')
                    new_p = 'Z.hor_operator(xN,xO,I)'
                if new_p == 'K':
                    size_check_ind = spec_ind_l.copy()
                    size_check_ind[-1] = str([spec_ind[-1] + 1])
                    size_check_ind_safe = size_check_ind.copy()
                    size_check_ind = size_check_ind + ['[2]']
                    size_check_ind_s = ''.join(size_check_ind)
                    if eval('t_prime_list' + size_check_ind_s) == 'size':
                        new_p = rd.choice(replacements['K'])
                    else:
                        choices = ['K(xN, E)', 'K(xN, xO, H)']
                        if len(t_bv) == 1:
                            new_p = choices[0]
                        else:
                            new_p = rd.choice(choices)
                        exec('del(t_prime_list' + spec_ind_s+')')
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
            elif t_component in replacements['K'] and new_p in replacements_new['C']:
                choices = replacements['C']
                new_p = rd.choice(choices)
                if new_p == 'K':
                    t_component_ind = replacements['K'].index(t_component)
                    del(replacements['K'][t_component_ind])
                    new_p = rd.choice(replacements['K'])
                if new_p == 'Z.hor_operator':
                    exec('del(t_prime_list' + spec_ind_s+')')
                    new_p = 'Z.hor_operator(xN,xO,I)'
                exec('t_prime_list' + spec_ind_s + '=' + 'new_p')
        t_prime_rule = self.list_to_string(t_prime_list)
        bound_vars = list(range(1, len(t_bv)+1))
        for ch in ["N", "O"]:
            if ch in t_prime_rule:
                rand_ind = bound_vars.index(rd.choice(bound_vars))
                t_prime_rule = t_prime_rule.replace(ch, str(bound_vars[rand_ind]))
                if len(t_bv) >= 2:
                    del(bound_vars[rand_ind])
        return {"t_prime_rule": t_prime_rule, "t_prime_bv": t_prime_bv, "t_prime_prec": ['prec'], "t_prime_list": t_prime_list}