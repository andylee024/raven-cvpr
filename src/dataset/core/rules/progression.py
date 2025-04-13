from dataset.core.rules.base import Rule

class ProgressionRule(Rule):
    """Rule that increments/decrements an attribute by a fixed step."""
    
    def __init__(self, attr_name, step=1):
        """Initialize progression rule.
        
        Args:
            attr_name: Attribute to modify ('type', 'size', etc.)
            step: Amount to increment/decrement (default: 1)
        """
        super().__init__(attr_name)
        self.step = step
    
    def apply(self, panel):
        """Apply progression to generate next panel."""
        
        result = panel.clone()
        attr = result._attributes[self.attr_name]
        
        for row in range(3):
            for col in range(3):
                if panel.exists(row, col):
                    current_value = panel.get_attr(row, col, self.attr_name)
                    next_value = attr.next_value(current_value, self.step)
                    result.set_attr(row, col, self.attr_name, next_value)
        
        return result
