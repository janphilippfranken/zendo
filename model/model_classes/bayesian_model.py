import abc
import numpy as np

class BayesianModelTemplate(metaclass=abc.ABCMeta):
     
    @abc.abstractmethod
    def deriv_prob(self) -> float:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def semantic_prob(self) -> float:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
        
    @abc.abstractmethod
    def ll(self) -> float:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def ll_ratio(self) -> float:
        """
          Args:
          Returns:
        """
        raise NotImplementedError()
    
    
class BayesianModel(BayesianModelTemplate): 
        
    def deriv_prob(self, production_probs: np.array):
        """See base class."""
        return np.prod(production_probs)
      
    def semantic_prob(self, deriv_prob, kappa=0.48629891):
        return deriv_prob**kappa

    def ll(self, outlier_count: int, out_penalizer: int):
        """See base class."""
        return np.exp(-(out_penalizer * outlier_count))

    def ll_ratio(self, p_h: np.array, p_h_prime: np.array, out_h: int, out_h_prime: int, out_penalizer: int):
        """See base class."""
        return self.semantic_prob(self.deriv_prob(p_h_prime)) / self.semantic_prob(self.deriv_prob(p_h)) * self.ll(out_h_prime, out_penalizer) / self.ll(out_h, out_penalizer)
