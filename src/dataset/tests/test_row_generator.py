#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the RowGenerator component.
Generates and visualizes rows created by different rules.
"""

import matplotlib.pyplot as plt
import os
import random
import numpy as np

from dataset.core.generators.puzzle_generator import RowGenerator
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.progression import ProgressionRule
import dataset.utils.panel_utils as panel_utils

def main():
    """Test the RowGenerator with different rules and visualize results."""
    # Create output directory
    output_dir = "output/row_generator_test"
    os.makedirs(output_dir, exist_ok=True)
    
    # Test progression rule
    test_progression_rule(output_dir)

    # Test arithmetic rule
    test_arithmetic_rule(output_dir)
    
    # You can add more test functions here as you implement additional rules
    # test_arithmetic_rule(output_dir)
    print(f"Test results saved to: {output_dir}")

def test_progression_rule(output_dir):
    """Test RowGenerator with a progression rule."""
    print("Testing ProgressionRule...")
    
    # Create a progression rule
    rule1 = ProgressionRule("type", step=1)
    rule2 = ProgressionRule("color", step=2)
    rule3 = ProgressionRule("size", step=1)
    rule4 = ProgressionRule("angle", step=1)
    ruleset = [rule1, rule2, rule3, rule4]
    
    # Create row generator
    row_generator = RowGenerator(ruleset)
    
    # Create seed panel
    seed_panel = panel_utils.get_uniform_triangle_panel(3)
    # seed_panel = panel_utils.get_random_panel()
    
    # Generate row
    row = row_generator.generate([seed_panel])
    
    # Visualize row
    visualize_row(row, os.path.join(output_dir, "progression_type.png"))

def test_arithmetic_rule(output_dir):
    """Test RowGenerator with an arithmetic rule."""

    print("Testing ArithmeticRule...")
    
    # Create an arithmetic rule
    rule = ArithmeticRule(attr_name="size", operation="add")
    row_generator = RowGenerator([rule])
    
    # Create seed panel
    panel0 = panel_utils.get_uniform_triangle_panel(n_entities=3)
    panel1 = panel0.clone()
    
    # Generate row
    row = row_generator.generate([panel0, panel1])
    
    # Visualize row
    visualize_row(row, os.path.join(output_dir, "arithmetic_size.png"))
    

def visualize_row(row, output_file):
    """Visualize a row of 3 panels side by side.
    
    Args:
        row: List of 3 panels
        output_file: Path to save the visualization
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot each panel in the row
    for i, panel in enumerate(row):
        ax = axes[i]
        
        # Convert to AoT for visualization
        aot_panel = panel.to_aot()
        
        # Render the panel
        from dataset.legacy.rendering import render_panel
        img = render_panel(aot_panel.raw)
        
        # Display the image
        ax.imshow(img, cmap='gray')
        ax.set_title(f"Panel {i+1}")
        
        # Remove ticks but keep border
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(2)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()