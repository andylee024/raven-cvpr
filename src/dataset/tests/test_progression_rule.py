import os
import sys
import unittest
import copy
import numpy as np

from dataset.legacy.Rule import Rule_Wrapper
from dataset.core.rules.progression import ProgressionRule

# Import needed utilities
from dataset.build_tree import build_distribute_four, build_center_single


class TestProgressionRule(unittest.TestCase):
    """Test suite for comparing old and new progression rule implementations."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Set a fixed random seed for reproducibility
        np.random.seed(42)
        
        # Build and initialize a proper test AoT
        root = build_distribute_four()
        
        # Create a simple progression rule for pruning
        progression_rule = Rule_Wrapper("Progression", "Number", [1], 0)
        
        # Prune the AoT
        pruned_root = root.prune([[progression_rule]])
        
        # Sample to get a concrete panel
        self.test_aot_four = pruned_root.sample() if pruned_root else None
    
    def test_number_value_progression(self):
        """Test that number values progress correctly."""
        # Create source panel with initial number value
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_number = initial_layout.number.get_value()
        
        # # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Number", [1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_number = old_layout.number.get_value()

        # Apply progression with new rule
        new_rule = ProgressionRule("Number", 1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_number = new_layout.number.get_value()

        # Verify both implementations progress the number correctly
        self.assertEqual(old_number, initial_number + 1, "Old rule didn't increment number correctly")
        self.assertEqual(new_number, initial_number + 1, "New rule didn't increment number correctly")
        self.assertEqual(old_number, new_number, "Rules produced different number values")
        
    
    @unittest.skip("Skipping")
    def test_negative_number_progression(self):
        """Test that number values progress correctly with negative values."""
        # Use distribute_four which has more entities to allow decreasing
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_number = initial_layout.number.get_value()
        
        # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Number", [-1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_number = old_layout.number.get_value()
        
        # Apply progression with new rule
        new_rule = ProgressionRule("Number", -1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_number = new_layout.number.get_value()
        
        # Verify both implementations decrease the number correctly
        self.assertEqual(old_number, initial_number - 1, "Old rule didn't decrement number correctly")
        self.assertEqual(new_number, initial_number - 1, "New rule didn't decrement number correctly")
        self.assertEqual(old_number, new_number, "Rules produced different number values")
        
        # Test entity count matches the number attribute
        self.assertEqual(len(old_layout.children), old_number, 
                         "Old rule: Entity count doesn't match number value")
        self.assertEqual(len(new_layout.children), new_number, 
                         "New rule: Entity count doesn't match number value")
    
    @unittest.skip("Skipping")
    def test_position_progression(self):
        """Test that position values progress correctly."""
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_pos_idx = initial_layout.position.get_value_idx()
        initial_positions = [entity.bbox for entity in initial_layout.children]
        
        # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Position", [1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_pos_idx = old_layout.position.get_value_idx()
        old_positions = [entity.bbox for entity in old_layout.children]
        
        # Apply progression with new rule
        new_rule = ProgressionRule("Position", 1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_pos_idx = new_layout.position.get_value_idx()
        new_positions = [entity.bbox for entity in new_layout.children]
        
        # Check position index progression
        expected_pos_idx = (initial_pos_idx + 1) % len(initial_layout.position.values)
        self.assertEqual(old_pos_idx, expected_pos_idx, "Old rule didn't update position index correctly")
        self.assertEqual(new_pos_idx, expected_pos_idx, "New rule didn't update position index correctly") 
        self.assertEqual(old_pos_idx, new_pos_idx, "Rules produced different position indices")
        
        # Check if entity positions changed
        self.assertNotEqual(initial_positions, old_positions, "Old rule didn't change entity positions")
        self.assertNotEqual(initial_positions, new_positions, "New rule didn't change entity positions")
        self.assertEqual(old_positions, new_positions, "Rules produced different entity positions")
    
    @unittest.skip("Skipping")
    def test_type_progression(self):
        """Test that type values progress correctly."""
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_type = initial_layout.children[0].type.get_value_level()
        
        # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Type", [1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_type = old_layout.children[0].type.get_value_level()
        
        # Apply progression with new rule
        new_rule = ProgressionRule("Type", 1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_type = new_layout.children[0].type.get_value_level()
        
        # Check type progression
        expected_type = initial_type + 1
        self.assertEqual(old_type, expected_type, "Old rule didn't increment type correctly")
        self.assertEqual(new_type, expected_type, "New rule didn't increment type correctly")
        self.assertEqual(old_type, new_type, "Rules produced different type values")
        
        # Check if all entities have the same type (uniformity)
        for entity in old_layout.children:
            self.assertEqual(entity.type.get_value_level(), old_type, 
                             "Old rule: Not all entities have the same type")
        
        for entity in new_layout.children:
            self.assertEqual(entity.type.get_value_level(), new_type, 
                             "New rule: Not all entities have the same type")
    
    @unittest.skip("Skipping")
    def test_size_progression(self):
        """Test that size values progress correctly."""
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_size = initial_layout.children[0].size.get_value_level()
        
        # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Size", [1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_size = old_layout.children[0].size.get_value_level()
        
        # Apply progression with new rule
        new_rule = ProgressionRule("Size", 1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_size = new_layout.children[0].size.get_value_level()
        
        # Check size progression
        expected_size = initial_size + 1
        self.assertEqual(old_size, expected_size, "Old rule didn't increment size correctly")
        self.assertEqual(new_size, expected_size, "New rule didn't increment size correctly")
        self.assertEqual(old_size, new_size, "Rules produced different size values")
        
        # Check if all entities have the same size (uniformity)
        for entity in old_layout.children:
            self.assertEqual(entity.size.get_value_level(), old_size, 
                             "Old rule: Not all entities have the same size")
        
        for entity in new_layout.children:
            self.assertEqual(entity.size.get_value_level(), new_size, 
                             "New rule: Not all entities have the same size")
    
    @unittest.skip("Skipping")
    def test_color_progression(self):
        """Test that color values progress correctly."""
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_color = initial_layout.children[0].color.get_value_level()
        
        # Apply progression with old rule
        old_rule = Rule_Wrapper("Progression", "Color", [1], 0)
        old_result = old_rule.apply_rule(source_panel)
        old_layout = old_result.children[0].children[0].children[0]
        old_color = old_layout.children[0].color.get_value_level()
        
        # Apply progression with new rule
        new_rule = ProgressionRule("Color", 1, 0)
        new_result = new_rule.apply(copy.deepcopy(source_panel))
        new_layout = new_result.children[0].children[0].children[0]
        new_color = new_layout.children[0].color.get_value_level()
        
        # Check color progression
        expected_color = initial_color + 1
        self.assertEqual(old_color, expected_color, "Old rule didn't increment color correctly")
        self.assertEqual(new_color, expected_color, "New rule didn't increment color correctly")
        self.assertEqual(old_color, new_color, "Rules produced different color values")
        
        # Check if all entities have the same color (uniformity)
        for entity in old_layout.children:
            self.assertEqual(entity.color.get_value_level(), old_color, 
                             "Old rule: Not all entities have the same color")
        
        for entity in new_layout.children:
            self.assertEqual(entity.color.get_value_level(), new_color, 
                             "New rule: Not all entities have the same color")
    
    @unittest.skip("Skipping")
    def test_sequential_number_progression(self):
        """Test that sequential applications of number progression work correctly."""
        source_panel = copy.deepcopy(self.test_aot_four)
        initial_layout = source_panel.children[0].children[0].children[0]
        initial_number = initial_layout.number.get_value()
        
        # Apply old rule twice
        old_rule = Rule_Wrapper("Progression", "Number", [1], 0)
        old_result1 = old_rule.apply_rule(source_panel)
        old_result2 = old_rule.apply_rule(old_result1)
        
        old_layout1 = old_result1.children[0].children[0].children[0]
        old_layout2 = old_result2.children[0].children[0].children[0]
        old_number1 = old_layout1.number.get_value()
        old_number2 = old_layout2.number.get_value()
        
        # Apply new rule twice
        new_rule = ProgressionRule("Number", 1, 0)
        new_source = copy.deepcopy(source_panel)
        new_result1 = new_rule.apply(new_source)
        new_result2 = new_rule.apply(new_result1)
        
        new_layout1 = new_result1.children[0].children[0].children[0]
        new_layout2 = new_result2.children[0].children[0].children[0]
        new_number1 = new_layout1.number.get_value()
        new_number2 = new_layout2.number.get_value()
        
        # Check first application
        self.assertEqual(old_number1, initial_number + 1, "Old rule first application incorrect")
        self.assertEqual(new_number1, initial_number + 1, "New rule first application incorrect")
        self.assertEqual(old_number1, new_number1, "First application produced different values")
        
        # Check second application
        self.assertEqual(old_number2, old_number1 + 1, "Old rule second application incorrect")
        self.assertEqual(new_number2, new_number1 + 1, "New rule second application incorrect")
        self.assertEqual(old_number2, new_number2, "Second application produced different values")
        
        # Check entity counts
        self.assertEqual(len(old_layout1.children), old_number1, "Old rule: Entity count mismatch after first application")
        self.assertEqual(len(old_layout2.children), old_number2, "Old rule: Entity count mismatch after second application")
        self.assertEqual(len(new_layout1.children), new_number1, "New rule: Entity count mismatch after first application")
        self.assertEqual(len(new_layout2.children), new_number2, "New rule: Entity count mismatch after second application")


if __name__ == "__main__":
    unittest.main()
