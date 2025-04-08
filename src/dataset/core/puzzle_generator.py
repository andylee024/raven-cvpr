import random
import copy

from dataset.core.aot.builders import AoTBuilder
from dataset.core.rules.factory import RuleFactory


class PuzzleGenerator:
    """
    Generates a single RAVEN puzzle with controlled rule application and state management.
    Responsible solely for puzzle generation logic, not visualization or storage.
    """
    
    def __init__(self, max_attempts=10):
        """Initialize the puzzle generator.
        
        Args:
            max_attempts: Maximum number of sampling attempts
        """
        self.max_attempts = max_attempts
        self.builder = AoTBuilder()
        self.rule_factory = RuleFactory()
        
    def generate(self, config_name, rule_type=None):
        """Generate a puzzle with the specified configuration and rule type.
        
        Args:
            config_name: Name of the configuration to use
            rule_type: Optional rule type (random if None)
            
        Returns:
            Dictionary with puzzle data or None if generation failed
        """
        # Get configuration builder
        config_builder = self._get_config_builder(config_name)
        if not config_builder:
            return None
            
        # Try multiple attempts
        for attempt in range(self.max_attempts):
            # Create a fresh rule
            rule = self._create_rule(rule_type)
            rule_group = [[rule]]
            
            # Try to generate the puzzle
            puzzle = self._try_generate_puzzle(config_builder, rule_group, config_name)
            if puzzle:
                return puzzle
                
        # Failed after max attempts
        return None
    
    def _get_config_builder(self, config_name):
        """Get the configuration builder function."""
        config_map = {
            "center_single": self.builder.build_center_single,
            "distribute_four": self.builder.build_distribute_four,
            "distribute_nine": self.builder.build_distribute_nine,
            "left_right": self.builder.build_left_center_single_right_center_single,
            "up_down": self.builder.build_up_center_single_down_center_single
        }
        return config_map.get(config_name)
    
    def _create_rule(self, rule_type=None):
        """Create a fresh rule instance."""
        if rule_type is None:
            rule_type = random.choice(["Progression", "Constant", "Arithmetic", "DistributeThree"])
            
        attribute = random.choice(["Number", "Position", "Type", "Size", "Color"])
        return self.rule_factory.create_rule(rule_type, attribute)
    
    def _try_generate_puzzle(self, config_builder, rule_group, config_name):
        """Attempt to generate a puzzle with pruning and sampling."""
        # Build configuration
        root = config_builder()
        
        # Prune based on rules
        pruned_root = root.prune(rule_group)
        if pruned_root is None:
            return None
            
        # Sample the first panel
        start_node = pruned_root.sample()
        
        # Generate all panels
        try:
            panels = self._generate_panels(start_node, rule_group[0][0])
            
            # Package the result
            return {
                'context': panels[:-1],  # First 8 panels
                'answer': panels[-1],    # Last panel
                'attr': rule_group[0][0].attr,
                'value': getattr(rule_group[0][0], 'value', None),
                'config': config_name,
                'rule_type': rule_group[0][0].name
            }
        except Exception as e:
            # Handle any errors during panel generation
            print(f"Error generating panels: {e}")
            return None
    
    def _generate_panels(self, start_node, rule):
        """Generate all panels for the 3x3 matrix."""
        # Fresh rule state for this puzzle
        rule_state = self._create_fresh_state(rule)
        
        # First row
        row_1_1 = copy.deepcopy(start_node)
        row_1_2 = self._apply_rule(rule, row_1_1, rule_state)
        row_1_3 = self._apply_rule(rule, row_1_2, rule_state)
        
        # Second row
        row_2_1 = copy.deepcopy(start_node)
        row_2_1.resample(True)  # Create variation
        row_2_2 = self._apply_rule(rule, row_2_1, rule_state)
        row_2_3 = self._apply_rule(rule, row_2_2, rule_state)
        
        # Third row
        row_3_1 = copy.deepcopy(start_node)
        row_3_1.resample(True)  # Create second variation
        row_3_2 = self._apply_rule(rule, row_3_1, rule_state)
        row_3_3 = self._apply_rule(rule, row_3_2, rule_state)
        
        return [row_1_1, row_1_2, row_1_3, 
                row_2_1, row_2_2, row_2_3, 
                row_3_1, row_3_2, row_3_3]
    
    def _create_fresh_state(self, rule):
        """Create fresh state for a rule based on its type."""
        # Simple version - just a dict with first_col flag
        # In a more complete implementation, this would be type-specific
        return {"first_col": True}
    
    def _apply_rule(self, rule, source, state):
        """Apply rule with basic state management."""
        # For now, just use the rule's apply_rule directly
        # In a more complete implementation, this would be type-specific
        result = rule.apply_rule(source)
        
        # Toggle first_col flag for next application
        if "first_col" in state:
            state["first_col"] = not state["first_col"]
            
        return result
