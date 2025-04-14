from abc import ABC, abstractmethod
from typing import List

from dataset.core.aot.attributes import ATTRIBUTES
from dataset.core.aot.tensor_panel import TensorPanel

class Rule(ABC):
    """Base class for all rules in RAVEN."""
    
    def __init__(self, attr_name, required_panels=1):
        """Initialize a rule."""

        if attr_name not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute name: {attr_name}")
        
        self.attr_name = attr_name
        self._attribute = ATTRIBUTES[attr_name]
        self.required_panels = required_panels

    @abstractmethod
    def apply(self, panels : List[TensorPanel]):
        """Apply this rule to transform source into target.
        
        Returns:
            Modified panel after rule application
        """
        pass

    @property
    def name(self):
        """Get the rule name (for compatibility with rule_constraint).
        
        Returns:
            Rule name without 'Rule' suffix
        """
        name = self.__class__.__name__
        if name.endswith("Rule"):
            name = name[:-4] + " " + self.attr_name
        return name
