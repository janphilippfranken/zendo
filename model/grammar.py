# grammar
S = ['Z.exists(lambda xN: A,X)', 'Z.forall(lambda xN: A,X)', 'L(lambda xN: A,M,X)']
A = ['B', 'S']
B = ['C', 'J(B,B)', 'Z.not_operator(B)']
C = ['Z.equal(xN, D)', 'K(xN, E)', 'Z.equal(xN,xO,G)', 'K(xN, xO, H)', 'Z.hor_operator(xN, xO, I)']
D = {"colour": ["'red'", "'blue'", "'green'"], "size": [1, 2, 3], "orientation": ["'upright'", "'lhs'", "'rhs'", "'strange'"], "grounded": ["'no'", "'yes'"]}
E = {"size": [1, 2, 3]}
G = ["'colour'", "'size'", "'orientation'", "'grounded'"]
H = ["'size'"]
I = ["'contact'"]
J = ['Z.and_operator', 'Z.or_operator']
K = ['Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']
L = ['Z.atleast', 'Z.atmost', 'Z.exactly']
M = [1, 2, 3]

productions = {"S": S, "A": A, "B": B, "C": C, "D": D, "E": E, "G": G, "H": H, "I": I, "J": J, "K": K, "L": L, "M": M}

# replacements
replacements = {"S": ["S"],
                "A": ['Z.exists','Z.forall','Z.atleast','Z.atmost','Z.exactly'],
                "B": ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater','Z.and_operator','Z.or_operator','Z.not_operator'],
                "C": ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']}

# experiment rules 
there_is_a_red = "Z.exists(lambda x1: Z.equal(x1,'red','colour'),X)"
nothing_is_upright = "Z.forall(lambda x1: Z.not_operator(Z.equal(x1,'upright','orientation')),X)"
one_is_blue = "Z.exactly(lambda x1: Z.equal(x1,'blue','colour'),1,X)"
there_is_a_blue_and_small = "Z.exists(lambda x1: Z.and_operator(Z.equal(x1,1,'size'),Z.equal(x1,'blue','colour')),X)"
all_are_blue_or_small = "Z.forall(lambda x1: Z.or_operator(Z.equal(x1,1,'size'),Z.equal(x1,'blue','colour')),X)"
all_are_the_same_size = "ob.forall(lambda x1: ob.forall(lambda x2: ob.equal(x1,x2,'size'), X), X)"
contact = "ob.exists(lambda x1: ob.exists(lambda x2: ob.hor_operator(x1,x2,'contact'), X), X)"
blue_to_red_contact = "ob.exists(lambda x1: ob.exists(lambda x2: ob.and_operator(ob.and_operator(ob.equal(x1, 'blue','colour'), ob.equal(x2 , 'red', 'colour')), ob.hor_operator(x1,x2,'contact')), X), X)"
red_bigger_than_all_nonred = "ob.exists(lambda x1: ob.forall(lambda x2: ob.or_operator(ob.and_operator(ob.equal(x1,'red','colour'), ob.greater(x1,x2,'size')), ob.equal(x2, 'red', 'colour')), X), X)"
stacked = "ob.exists(lambda x1: ob.exists(lambda x2: ob.and_operator(ob.and_operator(ob.and_operator(ob.and_operator(ob.and_operator(ob.equal(x1,'upright','orientation'),ob.equal(x1,'yes','grounded')),ob.equal(x2,'upright','orientation')),ob.equal(x2,'no','grounded')),ob.equal(x1,x2,'xpos')),ob.hor_operator(x1,x2,'contact')),X),X)"

rules_dict = {'Zeta': there_is_a_red,
              'Upsilon': nothing_is_upright,
              'Iota': one_is_blue,
              'Kappa': there_is_a_blue_and_small,
              'Omega': all_are_blue_or_small,
              'Phi': all_are_the_same_size,
              'Nu': contact,
              'Xi': blue_to_red_contact,
              'Mu': red_bigger_than_all_nonred,
              'Psi': stacked}


# grammar with production probabilities (for reverse rule class):
Swin = {'Z.exists': 1/3, 'Z.forall': 1/3, 'L': 1/3}
Awin = {"B": 1/2, "S": 1/2}
Bwin = {'C': 1/3, 'J(B,B)': 1/3, 'Z.not_operator': 1/3}
Cwin = {'D': 1/5, 'E': 1/5, 'G': 1/5, 'H': 1/5, 'I': 1/5}
Dwin =  {"colour": {"feat": 1/4, "values": {"red": 1/3, "blue": 1/3, "green": 1/3}},
         "size": {"feat": 1/4, "values": {"1": 1/3, "2": 1/3, "3": 1/3}},
         "orientation": {"feat": 1/4, "values": {"upright": 1/4, "lhs": 1/4, "rhs": 1/4, "strange": 1/4}},
         "grounded": {"feat": 1/4, "values": {"no": 1/2, "yes": 1/2}}}
Ewin = {"size": {"feat": 1/1, "values": {"1": 1/3, "2": 1/3, "3": 1/3}}}
Gwin = {'colour': 1/4, 'size': 1/4, 'orientation': 1/4, 'grounded': 1/4}
Hwin = {"size": 1/1}
Iwin = {"contact": 1/1}
Jwin =  {"Z.and_operator": 1/2, "Z.or_operator": 1/2}
Kwin =  {'Z.lequal': 1/4, 'Z.grequal': 1/4, 'Z.less': 1/4, 'Z.greater': 1/4}
Lwin =  {'Z.atleast': 1/3, 'Z.atmost': 1/3, 'Z.exactly': 1/3}
Mwin = {"1": 1/3, "2": 1/3, "3": 1/3}

# summarizing probs in dictionary
probs = {"S": Swin, "A": Awin, "B": Bwin, "C": Cwin, "D": Dwin, 
                 "E": Ewin, "G": Gwin, "H": Hwin, "I": Iwin, "J": Jwin, 
                 "K": Kwin, "L": Lwin, "M": Mwin}


# specific input dics for ts 
ts_rep = {"S": ['Z.exists','Z.forall','Z.atleast','Z.atmost','Z.exactly'],
                    "L": ['Z.atleast','Z.atmost','Z.exactly'],
                    "J": ['and_operator', 'or_operator'],
                    "M": [1,2,3],
                    "A": ['Z.exists','Z.forall','Z.atleast','Z.atmost','Z.exactly'],
                    "B": ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater','Z.and_operator','Z.or_operator','Z.not_operator'],
                    "C": ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']}

ts_rep_new = {"S": ['Z.exists','Z.forall','Z.atleast','Z.atmost','Z.exactly'],
                    "L": ['Z.atleast','Z.atmost','Z.exactly'],
                    "J": ['and_operator', 'or_operator'],
                    "M": [1,2,3],
                    "A": ['Z.exists','Z.forall','Z.atleast','Z.atmost','Z.exactly'],
                    "B": [["'(xN, D)'","'(xN,xO,G)'"], ["'(xN,xO,I)'","'(xN,xO,I)'"], ["'(xN,xO,H)'","'(xN, E)'"], ["'(xN,xO,H)'","'(xN, E)'"], ["'(xN,xO,H)'","'(xN, E)'"], ["'(xN,xO,H)'","'(xN, E)'"],'Z.and_operator','Z.or_operator','Z.not_operator'],
                    "C": ['Z.equal', 'Z.hor_operator', 'Z.lequal', 'Z.grequal', 'Z.less', 'Z.greater']}

