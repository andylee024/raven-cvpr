from dataset.core.rules.base import Rule
import copy

class ConstantRule(Rule):
    """Rule that maintains attributes unchanged between panels."""
    
    def __init__(self, attr):
        super().__init__(attr=attr)
    
    def apply(self, source, target=None):
        """Apply constant rule (no change)."""
        if target is None:
            return copy.deepcopy(source)
        return target
