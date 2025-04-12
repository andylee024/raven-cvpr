from abc import ABC, abstractmethod

class Operation(ABC):
    """Base class for operations"""
    @abstractmethod
    def apply(self, first_value, second_value):
        pass
        
    @abstractmethod
    def adjust_constraints(self, constraints, first_value):
        pass