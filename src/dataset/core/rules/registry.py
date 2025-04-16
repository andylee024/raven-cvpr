"""Rule registry for dynamically registering and instantiating rules."""

# Rule registry dictionary
RULE_REGISTRY = {}

def register_rule(rule_type, rule_class):
    """Register a rule class for a specific type.
    
    Args:
        rule_type: String identifier for the rule type (e.g., "spatial.rotation")
        rule_class: Rule class to register
    """
    RULE_REGISTRY[rule_type] = rule_class
    
def get_rule_class(rule_type):
    """Get the rule class for a specific type.
    
    Args:
        rule_type: String identifier for the rule type
        
    Returns:
        Rule class or None if not found
    """
    return RULE_REGISTRY.get(rule_type)

def instantiate_rule(rule_config):
    """Create a rule instance from a config dictionary.
    
    Args:
        rule_config: Dictionary containing rule configuration
        
    Returns:
        Instantiated rule object
        
    Raises:
        ValueError: If rule type is not recognized
    """
    rule_type = rule_config.get("type")
    parameters = rule_config.get("parameters", {})
    
    # Handle composite rules separately
    if rule_type == "composite":
        from dataset.core.rules.composite import CompositeRule
        subrules = [instantiate_rule(r) for r in rule_config.get("rules", [])]
        return CompositeRule(rules=subrules)
    
    # Look up rule class in registry
    rule_class = get_rule_class(rule_type)
    if rule_class:
        return rule_class(**parameters)
    else:
        raise ValueError(f"Unknown rule type: {rule_type}")
