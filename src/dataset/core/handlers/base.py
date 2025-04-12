from abc import ABC, abstractmethod


class AttributeHandler(ABC):
    """Base class for attribute handlers. 
    
    Handles the generation of attributes for a layout."""
    @abstractmethod
    def get_value(self, layout):
        pass
        
    @abstractmethod
    def set_value(self, layout, value):
        pass
        
    @abstractmethod
    def apply_constraints(self, layout, constraints):
        pass