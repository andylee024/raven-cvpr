#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the DistractorGenerator component.
Generates and visualizes distractor panels created using different strategies.
"""

import unittest
import matplotlib.pyplot as plt
import os
import random
import torch

from dataset.core.generators.distractor_generator import DistractorGenerator
import dataset.utils.panel_utils as panel_utils

class TestDistractorGenerator(unittest.TestCase):
    """Test cases for DistractorGenerator."""
    
    def setUp(self):
        """Set up for each test."""
        self.output_dir = "output/distractor_test"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create distractor generator
        self.generator = DistractorGenerator()
        
        # Create a random panel with enough entities for testing
        self.panel = panel_utils.get_random_panel(n_entities=6)
    
    @unittest.skip("Skipping attribute perturbation test")
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
    
    def _visualize_comparison(self, panels, titles, filename):
        """Visualize panels side by side for comparison."""
        fig, axes = plt.subplots(1, len(panels), figsize=(5*len(panels), 5))
        
        # Handle case of single panel (which would make axes not iterable)
        if len(panels) == 1:
            axes = [axes]
        
        # Plot each panel
        for i, (panel, title) in enumerate(zip(panels, titles)):
            ax = axes[i]
            
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
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=150)
        plt.close()
        print(f"Saved comparison to {os.path.join(self.output_dir, filename)}")

if __name__ == "__main__":
    unittest.main()
