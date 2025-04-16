import os
import unittest
import json
import matplotlib.pyplot as plt
import numpy as np

from dataset.core.rules import instantiate_rule
from dataset.core.rules.progression import ProgressionRule
from dataset.core.rules.spatial import RotationRule, ShiftRule
from dataset.core.rules.composite import CompositeRule
from dataset.utils.panel_utils import get_random_panel, get_uniform_triangle_panel
from dataset.utils.visualization_utils import visualize_comparison

class TestRules(unittest.TestCase):
    """Test suite for all rule implementations with visualization."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.output_dir = "output/rule_tests"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create panels for testing
        self.uniform_panel = get_uniform_triangle_panel(n_entities=5)
        self.random_panel = get_random_panel(n_entities=5)
        
    def _test_rule_with_visualization(self, rule, panel, rule_name, panel_name="random"):
        """Apply a rule and visualize before/after."""
        # Apply the rule
        result_panel = rule.apply([panel])
        
        # Visualize comparison
        visualize_comparison(
            panels=[panel, result_panel],
            titles=["Original", f"After {rule_name}"],
            filename=f"{panel_name}_{rule_name.replace(' ', '_')}.png",
            output_dir=self.output_dir
        )
        
        return result_panel
        
    def test_attribute_progression(self):
        """Test attribute progression rules."""
        # Test different attribute progressions
        attributes = ["type", "size", "color", "angle"]
        
        for attr in attributes:
            # Forward progression (step=1)
            rule_forward = ProgressionRule(attr, step=1)
            self._test_rule_with_visualization(
                rule_forward, 
                self.random_panel, 
                f"{attr} progression +1"
            )
            
            # Backward progression (step=-1)
            rule_backward = ProgressionRule(attr, step=-1)
            self._test_rule_with_visualization(
                rule_backward, 
                self.random_panel, 
                f"{attr} progression -1"
            )
    
    def test_rotation_rules(self):
        """Test rotation rules."""
        # Test different rotation steps and directions
        steps = [1, 2, 3]
        directions = [True, False]  # clockwise, counterclockwise
        
        for step in steps:
            for clockwise in directions:
                direction = "clockwise" if clockwise else "counterclockwise"
                rule = RotationRule(step=step, clockwise=clockwise)
                self._test_rule_with_visualization(
                    rule,
                    self.random_panel,
                    f"rotation step={step} {direction}"
                )
    
    def test_shift_rules(self):
        """Test shift rules."""
        # Test different shift directions and steps
        directions = ["right", "left", "up", "down", "diagonal"]
        steps = [1, 2]
        
        for direction in directions:
            for step in steps:
                rule = ShiftRule(direction=direction, step=step)
                self._test_rule_with_visualization(
                    rule,
                    self.random_panel,
                    f"shift {direction} step={step}"
                )
    
    def test_composite_rules(self):
        """Test composite rules."""
        # Create a composite rule: rotate then shift
        rotate_rule = RotationRule(step=1, clockwise=True)
        shift_rule = ShiftRule(direction="right", step=1)
        composite_rule = CompositeRule(rules=[rotate_rule, shift_rule])
        
        # Apply and visualize
        intermediate_panel = rotate_rule.apply([self.random_panel])
        final_panel = shift_rule.apply([intermediate_panel])
        
        # Visualize the sequence
        visualize_comparison(
            panels=[self.random_panel, intermediate_panel, final_panel],
            titles=["Original", "After Rotation", "After Rotation+Shift"],
            filename="composite_rotate_shift.png",
            output_dir=self.output_dir
        )
        
        # Test that the composite rule gives the same result
        composite_result = composite_rule.apply([self.random_panel])
        self.assertTrue(
            torch.all(torch.eq(composite_result.tensor, final_panel.tensor)),
            "Composite rule should produce the same result as sequential application"
        )
    
    def test_from_config(self):
        """Test instantiating and applying rules from configuration."""
        # Define a test configuration
        test_configs = [
            # Attribute progression config
            {
                "name": "Type Progression",
                "type": "attribute.progression",
                "parameters": {
                    "attribute_name": "type",
                    "step": 1
                }
            },
            # Spatial rotation config
            {
                "name": "90° Rotation",
                "type": "spatial.rotation",
                "parameters": {
                    "step": 1,
                    "clockwise": True
                }
            },
            # Composite rule config
            {
                "name": "Rotate and Change Color",
                "type": "composite",
                "rules": [
                    {
                        "type": "spatial.rotation",
                        "parameters": {
                            "step": 1,
                            "clockwise": True
                        }
                    },
                    {
                        "type": "attribute.progression",
                        "parameters": {
                            "attribute_name": "color",
                            "step": 2
                        }
                    }
                ]
            }
        ]
        
        # Test each configuration
        for config in test_configs:
            rule = instantiate_rule(config)
            self._test_rule_with_visualization(
                rule,
                self.random_panel,
                config["name"]
            )
            
            # Also save the config for reference
            config_path = os.path.join(
                self.output_dir, 
                f"config_{config['name'].replace(' ', '_')}.json"
            )
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
    
    def _create_rule_sequence_visualization(self, rule, panel, steps=5, rule_name="rule"):
        """Create a visualization of applying a rule multiple times in sequence."""
        panels = [panel]
        current_panel = panel
        
        # Apply the rule multiple times
        for i in range(steps):
            current_panel = rule.apply([current_panel])
            panels.append(current_panel)
        
        # Create titles
        titles = ["Original"] + [f"Step {i+1}" for i in range(steps)]
        
        # Visualize the sequence
        visualize_comparison(
            panels=panels,
            titles=titles,
            filename=f"sequence_{rule_name.replace(' ', '_')}.png",
            output_dir=self.output_dir
        )
    
    def test_rule_sequences(self):
        """Test applying rules multiple times in sequence."""
        # Test rotation sequence
        rotation_rule = RotationRule(step=1, clockwise=True)
        self._create_rule_sequence_visualization(
            rotation_rule,
            self.random_panel,
            steps=4,
            rule_name="rotation_90deg"
        )
        
        # Test shift sequence
        shift_rule = ShiftRule(direction="right", step=1)
        self._create_rule_sequence_visualization(
            shift_rule,
            self.random_panel,
            steps=3,
            rule_name="shift_right"
        )
        
        # Test color progression sequence
        color_rule = ProgressionRule("color", step=1)
        self._create_rule_sequence_visualization(
            color_rule,
            self.random_panel,
            steps=4,
            rule_name="color_progression"
        )

if __name__ == "__main__":
    import torch
    import sys
    
    def run_selected_tests():
        """Run selected tests from the command line."""
        # Create a test suite
        suite = unittest.TestSuite()
        
        # Add individual tests to the suite
        # Comment out any lines to skip those tests
        
        # Attribute progression tests
        suite.addTest(TestRules('test_attribute_progression'))
        
        # Spatial transformation tests
        suite.addTest(TestRules('test_rotation_rules'))
        suite.addTest(TestRules('test_shift_rules'))
        
        # Composite rule tests
        suite.addTest(TestRules('test_composite_rules'))
        
        # Configuration-based tests
        suite.addTest(TestRules('test_from_config'))
        
        # Rule sequence tests
        suite.addTest(TestRules('test_rule_sequences'))
        
        # Run the selected tests
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)
    
    # Check if specific tests were requested via command line
    if len(sys.argv) > 1:
        # Use unittest's built-in command line parsing
        unittest.main()
    else:
        # Run our custom test suite
        run_selected_tests()
