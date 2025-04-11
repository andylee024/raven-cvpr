import random
import copy
import traceback

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
    
    def _generate_candidates(self, answer_panel, rule_groups, num_candidates=7):
        """Generate candidate answers including distractors.
        
        Args:
            answer_panel: The correct answer panel
            rule_groups: The rule groups used for the puzzle
            num_candidates: Number of distractor candidates to generate
            
        Returns:
            tuple: (candidates, target_idx) where candidates is list of panels and 
                  target_idx is the index of correct answer
        """
        from dataset.sampling import sample_attr_avail, sample_attr
        
        # Get modifiable attributes for the answer panel
        modifiable_attr = sample_attr_avail(rule_groups, answer_panel)
        
        # Create list of candidates starting with correct answer
        answer_AoT = copy.deepcopy(answer_panel)
        candidates = [answer_AoT]
        
        # Generate distractor candidates
        for _ in range(num_candidates):
            # Sample an attribute to modify
            component_idx, attr_name, min_level, max_level = sample_attr(modifiable_attr)
            
            # Create a new candidate by modifying the sampled attribute
            candidate = copy.deepcopy(answer_AoT)
            candidate.sample_new(component_idx, attr_name, min_level, max_level, answer_AoT)
            candidates.append(candidate)
        
        # Shuffle candidates and track correct answer
        correct_answer = candidates[0]
        random.shuffle(candidates)
        target_idx = candidates.index(correct_answer)
        
        return candidates, target_idx
    
    def _try_generate_puzzle(self, config_builder, rule_group, config_name):
        """Attempt to generate a puzzle with pruning and sampling."""

        # Create additional rule group for multi-component configurations
        if config_name in ["left_right", "up_down"]:
            # These configurations need two rule groups
            if len(rule_group) == 1:
                # Add a second rule with a different attribute
                first_rule = rule_group[0][0]
                available_attrs = ["Number", "Position", "Type", "Size", "Color"]
                available_attrs.remove(first_rule.attr)
                second_attr = random.choice(available_attrs)
                
                # Create second rule of same type but different attribute
                second_rule = self.rule_factory.create_rule(
                    first_rule.name, 
                    second_attr
                )
                
                # Add the second rule group
                rule_group.append([second_rule])
        
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
            panels = self._generate_panels(start_node, rule_group)
            
            # Generate candidate answers
            candidates, target_idx = self._generate_candidates(answer_panel=panels[-1], rule_groups=rule_group)
            
            # Package the result with all information
            return {
                'context': panels[:-1],  # First 8 panels
                'answer': panels[-1],    # Correct answer panel
                'candidates': candidates, # All candidate answers (including correct one)
                'target': target_idx,    # Index of correct answer in candidates
                'attr': rule_group[0][0].attr,
                'value': getattr(rule_group[0][0], 'value', None),
                'config': config_name,
                'rule_type': rule_group[0][0].name
            }
        except Exception as e:
            traceback.print_exc()  
            print(f"    Debug: Error generating panels: {e}")
            return None
    
    def _generate_panels(self, start_node, rule_groups):
        """Generate all panels for the 3x3 matrix."""
        try:
            # First row
            row_1_1 = copy.deepcopy(start_node)
            row_1_2 = copy.deepcopy(row_1_1)
            row_1_3 = copy.deepcopy(row_1_1)
            
            # Apply rules for each component
            for l in range(len(rule_groups)):
                rule_group = rule_groups[l]
                rule = rule_group[0]  # Get the primary rule
                
                # Apply the rule to generate panel 2
                if l == 0:
                    row_1_2 = rule.apply_rule(row_1_1)
                else:
                    # For subsequent components, merge the result
                    temp = rule.apply_rule(row_1_1)
                    self._merge_component(row_1_2, temp, l)
                
                # Apply the rule to generate panel 3
                if l == 0:
                    row_1_3 = rule.apply_rule(row_1_2)
                else:
                    temp = rule.apply_rule(row_1_2)
                    self._merge_component(row_1_3, temp, l)
            
            # Second row (variation of first row)
            row_2_1 = copy.deepcopy(start_node)
            row_2_1.resample(True)  # Create variation
            row_2_2 = copy.deepcopy(row_2_1)
            row_2_3 = copy.deepcopy(row_2_1)
            
            # Apply rules for each component
            for l in range(len(rule_groups)):
                rule_group = rule_groups[l]
                rule = rule_group[0]
                
                if l == 0:
                    row_2_2 = rule.apply_rule(row_2_1)
                else:
                    temp = rule.apply_rule(row_2_1)
                    self._merge_component(row_2_2, temp, l)
                    
                if l == 0:
                    row_2_3 = rule.apply_rule(row_2_2)
                else:
                    temp = rule.apply_rule(row_2_2)
                    self._merge_component(row_2_3, temp, l)
            
            # Third row (another variation)
            row_3_1 = copy.deepcopy(start_node)
            row_3_1.resample(True)  # Create second variation
            row_3_2 = copy.deepcopy(row_3_1)
            row_3_3 = copy.deepcopy(row_3_1)
            
            # Apply rules for each component
            for l in range(len(rule_groups)):
                rule_group = rule_groups[l]
                rule = rule_group[0]
                
                if l == 0:
                    row_3_2 = rule.apply_rule(row_3_1)
                else:
                    temp = rule.apply_rule(row_3_1)
                    self._merge_component(row_3_2, temp, l)
                    
                if l == 0:
                    row_3_3 = rule.apply_rule(row_3_2)
                else:
                    temp = rule.apply_rule(row_3_2)
                    self._merge_component(row_3_3, temp, l)
            
            return [row_1_1, row_1_2, row_1_3, 
                    row_2_1, row_2_2, row_2_3, 
                    row_3_1, row_3_2, row_3_3]
        except Exception as e:
            print(f"Error generating panels: {e}")
            raise
    
    def _merge_component(self, dst_aot, src_aot, component_idx):
        """Merge a component from src_aot into dst_aot."""
        try:
            src_component = src_aot.children[0].children[component_idx]
            dst_aot.children[0].children[component_idx] = src_component
        except Exception as e:
            print(f"Error merging component {component_idx}: {e}")
            # If merge fails, don't modify the destination
