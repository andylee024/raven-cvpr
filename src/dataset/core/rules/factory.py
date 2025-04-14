from dataset.core.rules.progression import ProgressionRule
from dataset.core.rules.constant import ConstantRule
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.distribute_three import DistributeThreeRule
import random

class RuleFactory:
    """Factory for creating rule instances."""
    
    def create_from_config(self, rule_config):
        """Create a rule instance from a configuration dictionary.
        
        Args:
            rule_config: Dictionary with rule configuration (type, parameters)
            
        Returns:
            Rule instance
        """
        rule_type = rule_config["type"]
        parameters = rule_config["parameters"]
        
        # Convert from config format to factory format
        attr_name = parameters.get("attr_name")
        
        # Map config rule types to factory rule types
        type_map = {
            "progression": "Progression",
            "arithmetic": "Arithmetic", 
            "constant": "Constant",
            "distribute_three": "DistributeThree"
        }
        
        factory_rule_type = type_map.get(rule_type)
        if not factory_rule_type:
            raise ValueError(f"Unknown rule type: {rule_type}")
        
        # Create the rule with appropriate parameters
        return self.create_rule(factory_rule_type, attr_name, **parameters)
    
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
        step = kwargs.get('step', 1)  # Default to step=1
        return ProgressionRule(attr_name=attribute, step=step)
    
    def _create_constant_rule(self, attribute, **kwargs):
        """Create a constant rule."""
        return ConstantRule(attr_name=attribute)
    
    def _create_arithmetic_rule(self, attribute, **kwargs):
        """Create an arithmetic rule."""
        operation = kwargs.get('operation', 'add')
        return ArithmeticRule(attr_name=attribute, operation=operation)
    
    def _create_distribute_three_rule(self, attribute, **kwargs):
        """Create a distribute three rule."""
        return DistributeThreeRule(attr_name=attribute)
