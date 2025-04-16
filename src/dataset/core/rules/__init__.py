"""Rule module for RAVEN dataset."""

# Import and register all rules
from dataset.core.rules.registry import register_rule, instantiate_rule
from dataset.core.rules.base import Rule
from dataset.core.rules.composite import CompositeRule
from dataset.core.rules.progression import ProgressionRule
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.constant import ConstantRule
from dataset.core.rules.spatial import RotationRule, ShiftRule

# Register rules with the registry
register_rule("attribute.progression", ProgressionRule)
register_rule("attribute.arithmetic", ArithmeticRule)
register_rule("attribute.constant", ConstantRule)
register_rule("spatial.rotation", RotationRule)
register_rule("spatial.shift", ShiftRule)
register_rule("composite", CompositeRule)

# Export key functions and classes
__all__ = [
    'Rule',
    'CompositeRule',
    'AttributeProgressionRule',
    'ArithmeticRule',
    'ConstantRule',
    'RotationRule',
    'ShiftRule',
    'DistributeThreeRule',
    'register_rule',
    'instantiate_rule'
]
