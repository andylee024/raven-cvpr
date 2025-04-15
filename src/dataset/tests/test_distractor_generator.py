#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite for the DistractorGenerator component.
Tests all strategies individually and collectively with different difficulty levels.
"""

import unittest
import matplotlib.pyplot as plt
import os
import random
import torch
import sys

from dataset.core.generators.distractor_generator import DistractorGenerator
import dataset.utils.panel_utils as panel_utils

class TestDistractorGenerator(unittest.TestCase):
    """Test cases for DistractorGenerator."""
    
    def setUp(self):
        """Set up for each test."""
        self.output_dir = "output/distractor_test"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create distractor generators with different difficulty levels
        self.easy_generator = DistractorGenerator(difficulty="easy")
        self.medium_generator = DistractorGenerator(difficulty="medium")
        self.hard_generator = DistractorGenerator(difficulty="hard")
        
        # Default generator is medium difficulty
        self.generator = self.medium_generator
        
        # Create a random panel with enough entities for testing
        self.panel = panel_utils.get_random_panel(n_entities=6)
    
    def test_perturb_attribute(self):
        """Test perturbing attributes of entities."""
        print("Testing attribute perturbation...")
        
        # Apply the strategy
        perturbed_panel = self.generator._perturb_attribute(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, perturbed_panel], 
            ["Original", "Perturbed Attributes"],
            "attribute_perturb.png"
        )
        
        # Verify the distractor is different from the original
        self.assertFalse(torch.all(torch.eq(self.panel.tensor, perturbed_panel.tensor)))
    
    def test_swap_entity(self):
        """Test swapping entities."""
        print("Testing entity swapping...")
        
        # Apply the strategy
        swapped_panel = self.generator._swap_entity(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, swapped_panel], 
            ["Original", "Swapped Entities"],
            "entity_swap.png"
        )
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        swapped_count = (swapped_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, swapped_count)
    
    def test_remove_entity(self):
        """Test removing entities."""
        print("Testing entity removal...")
        
        # Apply the strategy
        removed_panel = self.generator._remove_entity(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, removed_panel], 
            ["Original", "Entity Removed"],
            "entity_remove.png"
        )
        
        # Verify an entity was removed
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        removed_count = (removed_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertLess(removed_count, original_count)
    
    def test_add_entity(self):
        """Test adding entities."""
        print("Testing entity addition...")
        
        # Apply the strategy
        added_panel = self.generator._add_entity(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, added_panel], 
            ["Original", "Entity Added"],
            "entity_add.png"
        )
        
        # Verify an entity was added
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        added_count = (added_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertGreater(added_count, original_count)
    
    def test_reflect_panel(self):
        """Test reflecting panel."""
        print("Testing panel reflection...")
        
        # Apply the strategy
        reflected_panel = self.generator._reflect_panel(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, reflected_panel], 
            ["Original", "Reflected Panel"],
            "reflect_panel.png"
        )
        
        # Verify the panel was changed
        self.assertFalse(torch.all(torch.eq(self.panel.tensor, reflected_panel.tensor)))
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        reflected_count = (reflected_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, reflected_count)
    
    def test_global_attribute_change(self):
        """Test global attribute change."""
        print("Testing global attribute change...")
        
        # Apply the strategy
        changed_panel = self.generator._global_attribute_change(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, changed_panel], 
            ["Original", "Global Attribute Change"],
            "global_attribute_change.png"
        )
        
        # Verify the panel was changed
        self.assertFalse(torch.all(torch.eq(self.panel.tensor, changed_panel.tensor)))
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        changed_count = (changed_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, changed_count)
    
    def test_rotate_all_entities(self):
        """Test rotating all entities."""
        print("Testing entity rotation...")
        
        # Apply the strategy
        rotated_panel = self.generator._rotate_all_entities(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, rotated_panel], 
            ["Original", "Rotated Entities"],
            "rotate_all_entities.png"
        )
        
        # Verify the panel was changed
        self.assertFalse(torch.all(torch.eq(self.panel.tensor, rotated_panel.tensor)))
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        rotated_count = (rotated_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, rotated_count)
    
    def test_scramble_positions(self):
        """Test scrambling entity positions."""
        print("Testing position scrambling...")
        
        # Apply the strategy
        scrambled_panel = self.generator._scramble_positions(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, scrambled_panel], 
            ["Original", "Scrambled Positions"],
            "scramble_positions.png"
        )
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        scrambled_count = (scrambled_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, scrambled_count)
    
    def test_swap_attributes(self):
        """Test swapping attributes between entities."""
        print("Testing attribute swapping...")
        
        # Apply the strategy
        swapped_attr_panel = self.generator._swap_attributes(self.panel.clone())
        
        # Visualize the original and distractor panels
        self._visualize_comparison(
            [self.panel, swapped_attr_panel], 
            ["Original", "Swapped Attributes"],
            "swap_attributes.png"
        )
        
        # Verify the number of entities remains the same
        original_count = (self.panel.tensor[:, :, 0] == 1).sum().item()
        swapped_count = (swapped_attr_panel.tensor[:, :, 0] == 1).sum().item()
        self.assertEqual(original_count, swapped_count)
    
    def test_difficulty_levels(self):
        """Test different difficulty levels."""
        print("Testing difficulty levels...")
        
        # Generate distractors with each difficulty level
        easy_distractors = self.easy_generator.generate(self.panel.clone(), count=1)
        medium_distractors = self.medium_generator.generate(self.panel.clone(), count=1)
        hard_distractors = self.hard_generator.generate(self.panel.clone(), count=1)
        
        # Visualize the panels
        self._visualize_comparison(
            [self.panel, easy_distractors[0], medium_distractors[0], hard_distractors[0]], 
            ["Original", "Easy Distractor", "Medium Distractor", "Hard Distractor"],
            "difficulty_levels.png"
        )
    
    def test_all_strategies_suite(self):
        """Run a sequential test of all strategies one by one."""
        print("\n===== RUNNING FULL STRATEGY TEST SUITE =====")
        
        # Test each strategy individually
        strategies = [
            ("attribute_perturb", "_perturb_attribute"),
            ("entity_swap", "_swap_entity"),
            ("entity_remove", "_remove_entity"),
            ("entity_add", "_add_entity"),
            ("reflect_panel", "_reflect_panel"),
            ("global_attribute_change", "_global_attribute_change"),
            ("rotate_all_entities", "_rotate_all_entities"),
            ("scramble_positions", "_scramble_positions"),
            ("swap_attributes", "_swap_attributes")
        ]
        
        # Create a multi-panel figure for the summary
        all_panels = [self.panel]
        all_titles = ["Original"]
        
        # Apply each strategy and collect results
        for strategy_name, method_name in strategies:
            print(f"Testing strategy: {strategy_name}")
            
            # Get the method to call
            method = getattr(self.generator, method_name)
            
            # Apply the strategy
            distractor = method(self.panel.clone())
            
            # Add to our collection for summary visualization
            all_panels.append(distractor)
            all_titles.append(strategy_name)
            
            # Verify panel was modified
            self.assertFalse(torch.all(torch.eq(self.panel.tensor, distractor.tensor)))
            
            # Print separator
            print("-" * 40)
        
        # Create a summary visualization of all strategies
        self._visualize_comparison(
            all_panels,
            all_titles,
            "all_strategies_summary.png"
        )
        
        print("\n===== ALL STRATEGY TESTS COMPLETED =====")
    
    def _visualize_comparison(self, panels, titles, filename):
        """Visualize panels side by side for comparison."""
        # Calculate grid dimensions
        n_panels = len(panels)
        if n_panels <= 4:
            n_cols = n_panels
            n_rows = 1
        else:
            n_cols = 4
            n_rows = (n_panels + 3) // 4  # Ceiling division
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 5*n_rows))
        
        # Handle case of single panel (which would make axes not iterable)
        if n_panels == 1:
            axes = np.array([axes])
        
        # Make axes a 2D array for consistent indexing
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        # Plot each panel
        for i, (panel, title) in enumerate(zip(panels, titles)):
            row, col = i // n_cols, i % n_cols
            ax = axes[row, col]
            
            # Convert to AoT for visualization
            aot_panel = panel.to_aot()
            
            # Render the panel
            from dataset.legacy.rendering import render_panel
            img = render_panel(aot_panel.raw)
            
            # Display the image
            ax.imshow(img, cmap='gray')
            ax.set_title(title)
            
            # Remove ticks but keep border
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color('black')
                spine.set_linewidth(2)
        
        # Hide any unused subplots
        for i in range(len(panels), n_rows * n_cols):
            row, col = i // n_cols, i % n_cols
            axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=150)
        plt.close()
        print(f"Saved comparison to {os.path.join(self.output_dir, filename)}")

def run_test_suite():
    """Run a complete test suite on all strategies."""
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add individual tests
    # suite.addTest(TestDistractorGenerator('test_perturb_attribute'))
    # suite.addTest(TestDistractorGenerator('test_swap_entity'))
    # suite.addTest(TestDistractorGenerator('test_remove_entity'))
    # suite.addTest(TestDistractorGenerator('test_add_entity'))
    # suite.addTest(TestDistractorGenerator('test_reflect_panel'))
    # suite.addTest(TestDistractorGenerator('test_global_attribute_change'))
    # suite.addTest(TestDistractorGenerator('test_rotate_all_entities'))
    # suite.addTest(TestDistractorGenerator('test_scramble_positions'))
    # suite.addTest(TestDistractorGenerator('test_swap_attributes'))
    # suite.addTest(TestDistractorGenerator('test_difficulty_levels'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    # Add numpy import for array handling in visualization
    import numpy as np
    
    print("Running individual tests: Use -v flag for verbose output")
    if len(sys.argv) > 1 and sys.argv[1] == '--suite':
        # Run the complete test suite
        run_test_suite()
    else:
        # Run tests individually with unittest's test discovery
        unittest.main()
