import abc 
import numpy as np
import pandas as pd
import copy

from model_classes.recode_rule_to_list import RuleTranslator
from model_classes.grammar import productions, probs


class ReverseRuleTemplate(RuleTranslator, metaclass=abc.ABCMeta):
    '''hard-coded class that reverts a string rule into production components and prior derivation probabilities'''
    
    @abc.abstractmethod
    def get_prec_recursively(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    

class ReverseRule(ReverseRuleTemplate):
    
    def get_prec_recursively(self, l):
        """ See base class. """
        flist = self.get_inds(l)
        quant_count = 0
        quant_idx_check = []
        to = {}
        for k in productions.keys():
            to[k] = []
        to["Ef"] = []
        to["Ev"] = []
        from_nt = []
        to_nt =[]
        li = []
        flist_copy = copy.deepcopy(flist)
        probabilities = copy.deepcopy(probs)
        if flist.count('lambda') == 1:
            probabilities["C"] = {'D': 1/2, 'E': 1/2}
        while any([i for i in flist if(i in ['Z.exists', 'Z.forall', 'Z.atleast', 'Z.atmost', 'Z.exactly'])]):
            for i in flist:
                if i in ['Z.exists', 'Z.forall', 'Z.atleast', 'Z.atmost', 'Z.exactly']:
                    quant_count += 1
                    if quant_count == 3: 
                        probabilities["A"]["B"] = 1
                    if flist[flist.index(i) + 8 * max(1, len(to["S"]))] in ['Z.exists', 'Z.forall', 'Z.atleast', 'Z.atmost', 'Z.exactly']:
                        if quant_count == 3:
                            to["B"].append(["S", 1])
                            li.append(1)
                        else:
                            to["A"].append(["S", probabilities["A"]["S"]])
                            li.append(probabilities["A"]["S"])
                    else:
                        to["A"].append(["B", probabilities["A"]["B"]])
                        li.append(probabilities["A"]["B"])
                if i in ['Z.exists', 'Z.forall']:
                    to["S"].append([i, probabilities["S"][i]])
                    to_nt.append(to["A"][len(to["A"])-1][0])
                    from_nt.append("S")
                    from_nt.append("A")
                    to_nt.append(i)
                    li.append(probabilities["S"][i])
                if i in ['Z.atleast', 'Z.atmost', 'Z.exactly']:
                    to["S"].append(["L", probabilities["S"]["L"]])
                    to["L"].append([i, probabilities["L"][i]])
                    from_nt.append("S")
                    from_nt.append("A")
                    from_nt.append("L")
                    to_nt.append('L')
                    to_nt.append(i)
                    li.append(probabilities["S"]["L"])
                    li.append(probabilities["L"][i])
                    to_nt.append(to["A"][len(to["A"])-1][0])
                if i in [1, 2, 3]:
                    quant_indices = [j for j, x in enumerate(flist) if x == i]
                    for idx in quant_indices:
                        if flist[idx + 2] == "size":
                            quant_indices.remove(idx)         
                    for idx in quant_indices: 
                        if flist[idx + 2] == "X":
                            if idx not in quant_idx_check:
                                to["M"].append([i, probabilities["M"][str(i)]])
                                from_nt.append("M")
                                to_nt.append(i)
                                li.append(probabilities["M"][str(i)])
                                quant_idx_check.append(idx)
            break
        while any([i for i in flist if(i in ['Z.and_operator', 'Z.or_operator', 'Z.not_operator'])]):
            for i in flist:
                if i in ['Z.and_operator', 'Z.or_operator']:
                    if len(to["B"]) == 0:
                        to["A"].append(["B", probabilities["A"]["B"]])
                    to['B'].append(["J(B,B)", probabilities['B']["J(B,B)"]])
                    li.append(probabilities["B"]["J(B,B)"])
                    from_nt.append("B")
                    from_nt.append("J")
                    to_nt.append('J(B,B)')
                    if i == 'Z.and_operator':
                        to['J'].append(['Z.and_operator', probabilities['J']["Z.and_operator"]])
                        to_nt.append('Z.and_operator')
                        li.append(probabilities["J"][i])
                    if i == 'Z.or_operator':
                        to['J'].append(['Z.or_operator', probabilities['J']["Z.or_operator"]])
                        to_nt.append('Z.or_operator')
                        li.append(probabilities["J"][i])
                if i in ['Z.not_operator']:
                    from_nt.append("B")
                    to_nt.append('not_operator(B)')
                    li.append(probabilities["B"][i])
                    if len(to["B"]) == 0:
                        to["A"].append(["B", probabilities["A"]["B"]])
                    to['B'].append(['Z.not_operator', probabilities['B']['Z.not_operator']])
            break
        while any([i for i in flist if(i in ['Z.equal','Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater','Z.hor_operator'])]):
            for i in flist:
                if from_nt.count("B") > 10:
                    probabilities["B"]["C"] = 1
                if i in ['Z.equal']:
                    from_nt.append("B")
                    from_nt.append("C")
                    to_nt.append("C")
                    li.append(probabilities["B"]["C"])
                    to["B"].append(["C", probabilities["B"]["C"]])
                    if flist[flist.index(i)+4] not in ['x1', 'x2', 'x3']: 
                        to["C"].append(["D", probabilities["C"]["D"]])
                        to_nt.append('Z.equal(xN,D)')
                        li.append(probabilities["C"]["D"])
                    else:
                        to["C"].append(["G", probabilities["C"]["G"]])
                        to_nt.append('Z.equal(xN,xO,G)')
                        li.append(probabilities["C"]["G"])
                if i in ['Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']:
                    li.append(probabilities["B"]["C"])
                    to_nt.append("C")
                    from_nt.append("K")
                    to_nt.append(i)
                    from_nt.append("B")
                    from_nt.append("C")
                    to["B"].append(["C", probabilities["B"]["C"]])
                    to["K"].append([i, probabilities["K"][i]])
                    if flist[flist.index(i)+4] not in ['x1', 'x2', 'x3']:
                        to["C"].append(["E", probabilities["C"]["E"]])
                        to_nt.append('K(xN, E)')
                        li.append(probabilities["C"]["E"])
                        li.append(probabilities["K"][i])
                    else:
                        to["C"].append(["H", probabilities["C"]["H"]])
                        to_nt.append('K(xN, xO, H)')
                        li.append(probabilities["C"]["H"])
                        li.append(probabilities["K"][i])
                if i in ['Z.hor_operator']:
                    li.append(probabilities["B"]["C"])
                    li.append(probabilities["C"]["I"])
                    to_nt.append("C")
                    li.append(probabilities["I"]["contact"])
                    to_nt.append("Z.hor_operator(xN,xO,I)")
                    from_nt.append("B")
                    from_nt.append("C")
                    to["B"].append(["C", probabilities["B"]["C"]])
                    to["C"].append(["I", probabilities["C"]["I"]])
                    to["I"].append([productions["I"], probabilities["I"]["contact"]])
                    to_nt.append('contact')
                    from_nt.append('Ef')
            break
        while any([i for i in flist if(i in ['colour', 'size','xpos', 'ypos', 'rotation', 'orientation', 'grounded'])]):
            for i in flist:
                if i in ['colour','size','xpos', 'ypos', 'rotation', 'orientation','grounded']:
                    if flist[flist.index(i)-2] not in ['x1', 'x2', 'x3']:
                        if flist[flist.index(i)-6] in ['Z.equal']:
                            to["Ef"].append([i, probabilities["D"][i]['feat']])
                            to["Ev"].append([flist[flist.index(i)-2], probabilities["D"][i]['values'][str(flist[flist.index(i)-2])]])
                            li.append(probabilities["D"][i]["feat"])
                            from_nt.append("Ef")
                            from_nt.append("Ev")
                            to_nt.append(i)
                            to_nt.append(flist[flist.index(i)-2])
                            li.append(probabilities["D"][i]["values"][str(flist[flist.index(i)-2])])
                        if flist[flist.index(i)-6] in ['Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']:
                            li.append(probabilities["E"][i]["feat"])
                            to["Ef"].append([i, probabilities["E"][i]['feat']])
                            to["Ev"].append([flist[flist.index(i)-2], probabilities["E"][i]['values'][str(flist[flist.index(i)-2])]])
                            li.append(probabilities["E"][i]["values"][str(flist[flist.index(i)-2])])
                            from_nt.append("Ef")
                            from_nt.append("Ev")
                            to_nt.append(i)
                            to_nt.append(flist[flist.index(i)-2])
                    if flist[flist.index(i)-2] in ['x1', 'x2', 'x3']:
                        if flist[flist.index(i)-6] in ['Z.equal']:
                            to["Ef"].append([i, probabilities["G"][i]])
                            li.append(probabilities["G"][i])
                            from_nt.append("Ef")
                            to_nt.append(i)
                        if flist[flist.index(i)-6] in ['Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']:
                            to["Ef"].append([i, probabilities["H"][i]])
                            from_nt.append("Ef")
                            li.append(probabilities["H"][i])
                            to_nt.append(i)
                    flist.remove(i)
            break
        return pd.DataFrame({"from": from_nt, "to": to_nt, "li": li})