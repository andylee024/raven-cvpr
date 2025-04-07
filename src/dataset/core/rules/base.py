from abc import ABC, abstractmethod
import copy

class Rule(ABC):
    """Base class for all rules in RAVEN."""
    
    def __init__(self, attr, value=None, component_idx=0):
        """Initialize a rule.
        
        Args:
            attr: Attribute this rule applies to
            value: Optional parameter value
            component_idx: Index of the component this rule applies to
        """
        self.attr = attr
        self.value = value
        self.component_idx = component_idx
        self.state = {}
    
    @abstractmethod
    def apply(self, source, target=None):
        """Apply this rule to transform source into target.
        
        Returns:
            Modified panel after rule application
        """
        pass

    def apply_rule(self, source, target=None):
        """Legacy compatibility method - forwards to apply()."""
        return self.apply(source, target)
    
    @property
    def name(self):
        """Get the rule name (for compatibility with rule_constraint).
        
        Returns:
            Rule name without 'Rule' suffix
        """
        name = self.__class__.__name__
        if name.endswith("Rule"):
            name = name[:-4]
        return name
