#!/usr/bin/env python3

import json
import os
import unittest

from dataset.core.generators.constrained_panel_sampler import ConstrainedPanelSampler
from dataset.core.aot.attributes import ATTRIBUTES
from dataset.utils.panel_utils import visualize_panel
        

class TestConstrainedPanelSampler(unittest.TestCase):
    """Unit tests for ConstrainedPanelSampler."""
    
    def setUp(self):
        """Set up test cases."""
        config_path = "/Users/andylee/Projects/raven-cvpr/src/dataset/config/progression_color.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.constraints = config['constraints']
        self.sampler = ConstrainedPanelSampler(self.constraints)
        self.num_samples = 100

    def test_sample_panel_single(self):
        """Test sampling a single panel with very specific constraints."""
        
        specific_constraints = {
            "min_entities": 1,
            "max_entities": 1,  # Exactly 1 entity
            "attribute_ranges": {
                "type": {"min": 1, "max": 3},  # Triangle only
                "color": {"min": 1, "max": 1},  # Green only (color=1)
                "size": {"min": 2, "max": 2},   # Medium size only (size=2)
                "angle": {"min": 0, "max": 7}   # Any angle allowed
            }
        }
        
        specific_sampler = ConstrainedPanelSampler(specific_constraints)
        panel = specific_sampler.sample_panel()
        
        output_dir = "output/test_sampler_panels"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "constrained_single_triangle.png")
        
        # Visualize and save to file
        visualize_panel(panel, output_path)
        print(f"Panel visualization saved to: {output_path}")

    def test_sample_panel_for_entities(self):
        """Test that panel entity count fits within constraints."""
        min_entities = self.constraints["min_entities"]
        max_entities = self.constraints["max_entities"]

        print("Testing entity count constraints...")
        print("min_entities: ", min_entities)
        print("max_entities: ", max_entities)
        
        for _ in range(self.num_samples):
            panel = self.sampler.sample_panel()
            filled_positions = panel.get_filled_positions()
            entity_count = len(filled_positions)
            
            self.assertGreaterEqual(entity_count, min_entities, 
                                   f"Panel has {entity_count} entities, less than min {min_entities}")
            self.assertLessEqual(entity_count, max_entities, 
                                f"Panel has {entity_count} entities, more than max {max_entities}")
    
    def test_sample_panel_for_type(self):
        """Test that entity types fit within constraints."""
        attr_name = 'type'
        if attr_name in self.constraints["attribute_ranges"]:
            min_val = self.constraints["attribute_ranges"][attr_name]["min"]
            max_val = self.constraints["attribute_ranges"][attr_name]["max"]
            
            print(f"Testing {attr_name} constraints...")
            print(f"min_{attr_name}: {min_val}")
            print(f"max_{attr_name}: {max_val}")
            
            for _ in range(self.num_samples):
                panel = self.sampler.sample_panel()
                filled_positions = panel.get_filled_positions()
                
                for row, col in filled_positions:
                    value = panel.get_attr(row, col, attr_name)
                    self.assertGreaterEqual(value, min_val, 
                                          f"Type value {value} is less than min {min_val}")
                    self.assertLessEqual(value, max_val, 
                                       f"Type value {value} is more than max {max_val}")
    
    def test_sample_panel_for_size(self):
        """Test that entity sizes fit within constraints."""
        attr_name = 'size'
        if attr_name in self.constraints["attribute_ranges"]:
            min_val = self.constraints["attribute_ranges"][attr_name]["min"]
            max_val = self.constraints["attribute_ranges"][attr_name]["max"]
            
            print(f"Testing {attr_name} constraints...")
            print(f"min_{attr_name}: {min_val}")
            print(f"max_{attr_name}: {max_val}")
            
            for _ in range(self.num_samples):
                panel = self.sampler.sample_panel()
                filled_positions = panel.get_filled_positions()
                
                for row, col in filled_positions:
                    value = panel.get_attr(row, col, attr_name)
                    self.assertGreaterEqual(value, min_val, 
                                          f"Size value {value} is less than min {min_val}")
                    self.assertLessEqual(value, max_val, 
                                       f"Size value {value} is more than max {max_val}")
    
    def test_sample_panel_for_color(self):
        """Test that entity colors fit within constraints."""
        attr_name = 'color'
        if attr_name in self.constraints["attribute_ranges"]:
            min_val = self.constraints["attribute_ranges"][attr_name]["min"]
            max_val = self.constraints["attribute_ranges"][attr_name]["max"]
            
            print(f"Testing {attr_name} constraints...")
            print(f"min_{attr_name}: {min_val}")
            print(f"max_{attr_name}: {max_val}")
            
            for _ in range(self.num_samples):
                panel = self.sampler.sample_panel()
                filled_positions = panel.get_filled_positions()
                
                for row, col in filled_positions:
                    value = panel.get_attr(row, col, attr_name)
                    self.assertGreaterEqual(value, min_val, 
                                          f"Color value {value} is less than min {min_val}")
                    self.assertLessEqual(value, max_val, 
                                       f"Color value {value} is more than max {max_val}")
    
    def test_sample_panel_for_angle(self):
        """Test that entity angles fit within constraints."""
        attr_name = 'angle'
        if attr_name in self.constraints["attribute_ranges"]:
            min_val = self.constraints["attribute_ranges"][attr_name]["min"]
            max_val = self.constraints["attribute_ranges"][attr_name]["max"]
            
            print(f"Testing {attr_name} constraints...")
            print(f"min_{attr_name}: {min_val}")
            print(f"max_{attr_name}: {max_val}")
            
            for _ in range(self.num_samples):
                panel = self.sampler.sample_panel()
                filled_positions = panel.get_filled_positions()
                
                for row, col in filled_positions:
                    value = panel.get_attr(row, col, attr_name)
                    self.assertGreaterEqual(value, min_val, 
                                          f"Angle value {value} is less than min {min_val}")
                    self.assertLessEqual(value, max_val, 
                                       f"Angle value {value} is more than max {max_val}")
    
    def test_sample_entity_tensor(self):
        """Test that entity tensors fit within constraints."""
        print("Testing entity tensor sampling...")
        
        for _ in range(self.num_samples):
            entity = self.sampler.sample_entity_tensor()
            
            # Check exists is 1
            self.assertEqual(entity[0].item(), 1, "Entity 'exists' value is not 1")
            
            # Check type
            attr_name = 'type'
            if attr_name in self.constraints["attribute_ranges"]:
                min_val = self.constraints["attribute_ranges"][attr_name]["min"]
                max_val = self.constraints["attribute_ranges"][attr_name]["max"]
                value = entity[ATTRIBUTES[attr_name].index].item()
                self.assertGreaterEqual(value, min_val, f"Type value {value} is less than min {min_val}")
                self.assertLessEqual(value, max_val, f"Type value {value} is more than max {max_val}")
            
            # Check size
            attr_name = 'size'
            if attr_name in self.constraints["attribute_ranges"]:
                min_val = self.constraints["attribute_ranges"][attr_name]["min"]
                max_val = self.constraints["attribute_ranges"][attr_name]["max"]
                value = entity[ATTRIBUTES[attr_name].index].item()
                self.assertGreaterEqual(value, min_val, f"Size value {value} is less than min {min_val}")
                self.assertLessEqual(value, max_val, f"Size value {value} is more than max {max_val}")
            
            # Check color
            attr_name = 'color'
            if attr_name in self.constraints["attribute_ranges"]:
                min_val = self.constraints["attribute_ranges"][attr_name]["min"]
                max_val = self.constraints["attribute_ranges"][attr_name]["max"]
                value = entity[ATTRIBUTES[attr_name].index].item()
                self.assertGreaterEqual(value, min_val, f"Color value {value} is less than min {min_val}")
                self.assertLessEqual(value, max_val, f"Color value {value} is more than max {max_val}")
            
            # Check angle
            attr_name = 'angle'
            if attr_name in self.constraints["attribute_ranges"]:
                min_val = self.constraints["attribute_ranges"][attr_name]["min"]
                max_val = self.constraints["attribute_ranges"][attr_name]["max"]
                value = entity[ATTRIBUTES[attr_name].index].item()
                self.assertGreaterEqual(value, min_val, f"Angle value {value} is less than min {min_val}")
                self.assertLessEqual(value, max_val, f"Angle value {value} is more than max {max_val}")

if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_single"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_for_entities"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_for_type"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_for_size"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_for_color"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_panel_for_angle"))
    suite.addTest(TestConstrainedPanelSampler("test_sample_entity_tensor"))
    unittest.TextTestRunner().run(suite)
