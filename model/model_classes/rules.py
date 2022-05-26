import abc
import numpy as np


class RulesTemplate(metaclass=abc.ABCMeta):
     
    @abc.abstractmethod
    def exists(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def forall(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def exactly(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def atleast(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
        
    @abc.abstractmethod
    def atmost(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def and_operator(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def or_operator(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def hor_operator(self) -> bool:
        """
        Operator checks if objects touch each other. Note: y[dim] needs to be longer than 1
        to prevent self-comparison from counting as True.
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def not_operator(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def equal(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def grequal(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def lequal(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def greater(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def less(self) -> bool:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()

    
class Rules(RulesTemplate): 

    def exists(self, func, x):
        """See base class."""
        return any(list(map(func,x)))

    def forall(self, func, x):
        """See base class."""
        return all(list(map(func,x)))

    def exactly(self, func, n, x):
        """See base class."""
        return sum(list(map(func,x))) == n

    def atleast(self, func, n, x):
        """See base class."""
        return sum(list(map(func,x))) >= n

    def atmost(self, func, n, x):
        """See base class."""
        return sum(list(map(func,x))) <= n

    def and_operator(self, x, y):
        """See base class."""
        return x and y

    def or_operator(self, x, y):
        """See base class."""
        return x or y

    def hor_operator(self, x, y, dim):
        """See base class."""
        return x["id"] in y[dim] and len(y[dim]) > 1

    def not_operator(self, x):
        """See base class."""
        return not x

    def equal(self, x, y, dim):
        """See base class."""
        if x == y:
            return True
        if isinstance(y, dict) == False:
            return x[dim] == y
        else:
            return x[dim] == y[dim]

    def grequal(self, x, y, dim):
        """See base class."""
        if isinstance(y, dict) == False:
            return x[dim] >= y
        else:
            return x[dim] >= y[dim]

    def lequal(self, x, y, dim):
        """See base class."""
        if isinstance(y, dict) == False:
            return x[dim] <= y
        else:
            return x[dim] <= y[dim]

    def greater(self, x, y, dim):
        """See base class."""
        if x == y:
            return True
        if isinstance(y, dict) == False:
            return x[dim] > y
        else:
            return x[dim] > y[dim]

    def less(self, x, y, dim):
        """See base class."""
        if x == y:
            return True
        if isinstance(y, dict) == False:
            return x[dim] < y
        else:
            return x[dim] < y[dim]