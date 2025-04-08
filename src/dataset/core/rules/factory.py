from dataset.core.rules.progression import ProgressionRule
from dataset.core.rules.constant import ConstantRule
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.distribute_three import DistributeThreeRule
import random

class RuleFactory:
    """Factory for creating rule instances."""
    
    def create_rule(self, rule_type, attribute, **kwargs):
        """Create a rule instance of the specified type.
        
        Args:
            rule_type: Type of rule to create ('Progression', 'Constant', etc.)
            attribute: Attribute the rule applies to ('Number', 'Type', etc.)
            **kwargs: Additional parameters for specific rule types
            
        Returns:
            Rule instance
        """
        rule_map = {
            "Progression": self._create_progression_rule,
            "Constant": self._create_constant_rule,
            "Arithmetic": self._create_arithmetic_rule,
            "DistributeThree": self._create_distribute_three_rule
        }
        
        creator = rule_map.get(rule_type)
        if not creator:
            raise ValueError(f"Unknown rule type: {rule_type}")
            
        return creator(attribute, **kwargs)
    
    def _create_progression_rule(self, attribute, **kwargs):
        """Create a progression rule."""
        value = kwargs.get('value')
        if value is None:
            value = random.randint(-1, 1)  # Default progression values
        return ProgressionRule(attr=attribute, value=value)
    
    def _create_constant_rule(self, attribute, **kwargs):
        """Create a constant rule."""
        return ConstantRule(attr=attribute)
    
    def _create_arithmetic_rule(self, attribute, **kwargs):
        """Create an arithmetic rule."""
        value = kwargs.get('value')
        if value is None:
            value = random.choice([-2, -1, 0, 1, 2])  # Default arithmetic values
        return ArithmeticRule(attr=attribute, value=value)
    
    def _create_distribute_three_rule(self, attribute, **kwargs):
        """Create a distribute three rule."""
        return DistributeThreeRule(attr=attribute)
