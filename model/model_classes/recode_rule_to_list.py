import abc


class RuleTranslatorTemplate(metaclass=abc.ABCMeta):
    '''hard-coded class that reverts a rule into a list and vice versa'''
    
    @abc.abstractmethod
    def string_to_list(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def list_to_string(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def flatten(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_inds(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_list(self):
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
        
class RuleTranslator(RuleTranslatorTemplate):

    def string_to_list(self, char_string):
        """ See base class. """
        c_list= list(char_string)      
        c_string = [''.join("',[" if c == '(' else ']' if c == ')' else "'X'" if c == "X" else ",':'," if c == ":" else c for c in char) for char in c_list]
        c_string = [''.join("'Z" if c == "Z" else c for c in char) for char in c_string]
        c_string = ''.join(c_string)
        for ch in ['x1', 'x2', 'x3']:
            if ch in c_string:
                    c_string=c_string.replace(ch,"'"+ch+"'")
        for ch in ["lambda"]:
            if ch in c_string:
                c_string=c_string.replace(ch,"'lambda',")
        index_missing = 0
        for ch in ["r'Z"]:
            if ch in c_string:
                index_missing = c_string.index(ch)
                next_closing_index = c_string[index_missing:].index("]")
                c_string = c_string[:index_missing+next_closing_index] + "]" + c_string[index_missing+next_closing_index:]
                c_string=c_string.replace(ch,"r',['Z")
        for ch in [",',"]:
            if ch in c_string:
                c_string=c_string.replace(ch,",")  
        return list(eval(c_string))

    def list_to_string(self, char_list):
        """ See base class. """
        c_string = str(char_list)[1:len(str(char_list))-2]
        c_string = [''.join("(" if c == "[" else '),' if c == ']' else ':' if c == ",':'," else c for c in char) for char in c_string]
        c_string = ''.join(c_string)
        for ch in ["'Z.exactly'", "'Z.atmost'", "'Z.atleast'", "'Z.exists'", "'Z.forall'", # quantifiers
                   "'Z.or_operator'", "'Z.and_operator'", "'Z.not_operator'", "'Z.equal'", # booleans
                    "'Z.lequal'", "'Z.grequal'", "'Z.less'", "'Z.greater'", "'Z.hor_operator'", # comparison
                   "'lambda'", "':'", "'X'"]: # other stuff
            if ch in c_string:
                c_string=c_string.replace(ch, eval(ch))
        for ch in ["'x1'", "'x2'", "'x3'"]: 
            if ch in c_string:
                c_string=c_string.replace(ch, eval(ch)+",")
        for ch in [", ("]:
            if ch in c_string:
                c_string=c_string.replace(ch, "(")
        for ch in [", "]:
            if ch in c_string:
                c_string=c_string.replace(ch, " ")
        for ch in [", :"]:
            if ch in c_string:
                c_string=c_string.replace(ch, ":")
        c_string = c_string + ")"
        for ch in [",)"]:
            if ch in c_string:
                c_string=c_string.replace(ch, ")")
        for ch in ["1 X", "2 X", "3 X"]:
            if ch in c_string:
                c_string=c_string.replace(ch, ch[0] + "," + " X")
        for ch in ["'colour'", "'size'", "'orientation'", "'grounded'", "D", "E"]:
            if ch in c_string:
                c_string=c_string.replace(ch, "," + ch)
        for ch in [" ,", " ,"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ",")
        for ch in [" "]:     
            if ch in c_string:
                c_string=c_string.replace(ch, "")
        for ch in ["lambda", ":"]:      
            if ch in c_string:
                c_string=c_string.replace(ch, ch + " ")
        for ch in [",X))"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ",X)")
        for ch in ["xN", "xO"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ch + ",")
        for ch in ["x1x1","x1x2","x2x1","x1x3","x3x1","x2x3","x3x2","x2x2","x3x3"]:       # groƒunded
            if ch in c_string:
                c_string=c_string.replace(ch, ch[:2] + "," + ch[2:] + ",")
        for ch in ["'Z", "'L", "'X", "'K", "'C", "'J", "'1","'2","'3"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ch[1])
        for ch in ["'B"]:      
            if ch in c_string:
                c_string=c_string.replace(ch, ch[1] + ",")
        for ch in ["'S)", "'S"]:      
            if ch in c_string:
                c_string=c_string.replace(ch, ch[1])
        for ch in [")X","CX", "SX","S1","S2","S3","C1","C2","C3",")1",")2",")3","CZ"]:       # groƒunded
            if ch in c_string:
                c_string=c_string.replace(ch, ch[0] + "," + ch[1])
        for ch in ["C'"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ch[0])
        for ch in ["B)Z","D)Z","E)Z","G)Z","H)Z","I)Z"]:    
            if ch in c_string:
                c_string=c_string.replace(ch, ch[:2] + ',' + ch[2])
        for ch in ["B)'","E)'","H)'","D)'","I)'", "G)'"]:     
            if ch in c_string:
                c_string=c_string.replace(ch, ch[:2])
        for ch in [",,"]:       
            if ch in c_string:
                c_string=c_string.replace(ch, ",")
        return c_string


    def flatten(self, l):
        """ See base class. """
        stack = [enumerate(l)]
        path = [None]
        while stack:
            for path[-1], x in stack[-1]:
                if isinstance(x, list):
                    stack.append(enumerate(x))
                    path.append(None)
                else:
                    yield x, tuple(path)
                break
            else:
                stack.pop()
                path.pop()

    def get_inds(self, l):
        """ See base class. """
        all_ind = []
        for entry in self.flatten(l):
            all_ind.append(entry[0])
            all_ind.append(list(entry[1]))
        return  all_ind

    def get_list(self, l):
        """ See base class. """
        flat_list = []
        for entry in self.flatten(l):
            flat_list.append(entry[0])
        return flat_list