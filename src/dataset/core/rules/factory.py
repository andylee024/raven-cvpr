from dataset.core.rules.progression import ProgressionRule
from dataset.core.rules.constant import ConstantRule
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.distribute_three import DistributeThreeRule

class RuleFactory:
    """Factory for creating rule instances."""
    
    @staticmethod
    def create_rule(rule_type, **kwargs):
        """Create a rule of the specified type with given parameters.
        
        Args:
            rule_type: Type of rule to create (progression, constant, etc.)
            **kwargs: Parameters for the rule
            
        Returns:
            An instance of the requested rule
        """
        rule_map = {
            "progression": ProgressionRule,
            "constant": ConstantRule,
            "arithmetic": ArithmeticRule,
            "distribute_three": DistributeThreeRule
        }
        
        if rule_type.lower() not in rule_map:
            raise ValueError(f"Unknown rule type: {rule_type}")
            
        return rule_map[rule_type.lower()](**kwargs)
    
    @staticmethod
    def from_legacy(name, attr, param, component_idx=0):
        """Create a rule from legacy parameters."""
        if name == "Constant":
            return ConstantRule(attr=attr)
        elif name == "Progression":
            return ProgressionRule(attr=attr, value=param)
        elif name == "Arithmetic":
            return ArithmeticRule(attr=attr, value=param)
        elif name == "Distribute_Three":
            return DistributeThreeRule(attr=attr)
        else:
            raise ValueError(f"Unsupported Rule: {name}")
