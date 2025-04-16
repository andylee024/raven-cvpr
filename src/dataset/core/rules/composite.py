"""Implementation of composite rules that combine multiple rules."""

from dataset.core.rules.base import Rule

class CompositeRule(Rule):
    """Rule that applies multiple rules in sequence."""
    
    def __init__(self, rules, name=None):
        """Initialize a composite rule.
        
        Args:
            rules: List of rules to apply in sequence
            name: Optional name for the rule (defaults to auto-generated)
        """
        # Create descriptive name if not provided
        if name is None:
            rule_names = [rule.name for rule in rules]
            name = f"Composite({', '.join(rule_names)})"
            
        super().__init__(rule_type="composite")
        self.rules = rules
        self._name = name
    
    def apply(self, panels):
        """Apply all rules in sequence.
        
        Args:
            panels: List of input panels
            
        Returns:
            Final panel after applying all rules
        """
        if not panels:
            raise ValueError("No panels provided to CompositeRule")
            
        result = panels[0].clone()
        
        for rule in self.rules:
            # Apply each rule, passing the result of the previous rule
            result = rule.apply([result])
            
        return result
    
    @property
    def name(self):
        """Get the composite rule name."""
        return self._name