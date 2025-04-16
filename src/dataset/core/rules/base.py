from abc import ABC, abstractmethod
from typing import List

from dataset.core.aot.tensor_panel import TensorPanel

class Rule(ABC):
    """Base class for all rules in RAVEN."""
    
    def __init__(self, rule_type, required_panels=1):
        """Initialize a rule.
        
        Args:
            rule_type: Type of rule ("attribute", "spatial", "combined", etc.)
            required_panels: Number of panels required to apply the rule
        """
        self.rule_type = rule_type
        self.required_panels = required_panels

    @abstractmethod
    def apply(self, panels: List[TensorPanel]) -> TensorPanel:
        """Apply this rule to transform panels.
        
        Args:
            panels: List of input panels
            
        Returns:
            Modified panel after rule application
        """
        pass

    @property
    def name(self):
        """Get the rule name (for compatibility with rule_constraint)."""
        name = self.__class__.__name__
        if name.endswith("Rule"):
            name = name[:-4]
        return f"{name} {self.rule_type}"