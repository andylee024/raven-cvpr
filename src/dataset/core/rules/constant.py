from dataset.core.rules.base import Rule
import copy

class ConstantRule(Rule):
    """Rule that maintains attributes unchanged between panels."""
    
    def __init__(self, attr):
        super().__init__(attr=attr)
    
    def apply(self, panel):
        """Apply constant rule (no change)."""
        return copy.deepcopy(panel)
