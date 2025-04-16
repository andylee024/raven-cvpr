from dataset.core.rules.registry import instantiate_rule, register_rule

class RuleFactory:
    """Factory for creating rule instances."""
    
def create_rule_from_config(config):
    """Create a rule from a configuration object.
    
    Args:
        config: Dictionary containing rule configuration
        
    Returns:
        Instantiated rule object
    """
    return instantiate_rule(config)

def register_custom_rule(rule_type, rule_class):
    """Register a custom rule class.
    
    Args:
        rule_type: String identifier for the rule type
        rule_class: Rule class to register
    """
    register_rule(rule_type, rule_class)