#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility function to generate and visualize a distribute_nine panel.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Add project root to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dataset.core.puzzle_generator import PuzzleGenerator
from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.handlers.type_handler import TypeHandler
from dataset.rendering import render_panel

def generate_sample_panel():
    """Generate a distribute_nine panel using PuzzleGenerator.
    Returns:
        facade: An AoTFacade wrapping the generated panel
    """
    generator = PuzzleGenerator()
    puzzle = generator.generate("distribute_nine")
    panel = puzzle['context'][0]  # Take the first context panel
    facade = AoTFacade(panel)
    return facade

def visualize_panel(facade, output_path):
    """Visualize a single panel and save to file.
    
    Args:
        facade: AoTFacade containing the panel
        output_path: Path to save the visualization
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Render the panel
    rendered_image = render_panel(facade.raw)
    
    # Save visualization
    plt.figure(figsize=(8, 8))
    plt.imshow(rendered_image, cmap='gray')
    plt.axis('off')
    plt.title("Distribute Nine Panel")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Panel visualization saved to: {output_path}")
    

def print_shape_information(facade):
    """Print shape information for all entities in the panel."""
    # Create a type handler to work with shapes
    type_handler = TypeHandler()
    
    print("\nPanel Shape Information:")
    print("========================")
    
    entity_count = facade.get_entity_count()
    print(f"Panel has {entity_count} entities")
    
    # Print shape information for each entity
    for i in range(entity_count):
        # Get shape type value
        shape_value = type_handler.get_value(facade, entity_idx=i)
        
        # Get shape name
        shape_name = type_handler.get_shape_name(shape_value)
        
        print(f"Entity {i}: Shape Type = {shape_value} ({shape_name})")
    
    print("========================\n")


if __name__ == "__main__":
    # Generate and get a sample panel
    panel = generate_sample_panel()
    
    # Print panel summary from AoTFacade
    panel.print_summary()
    
    # Print shape information using TypeHandler
    print_shape_information(panel)
    
    # Visualize the panel
    visualize_panel(panel, "test_output/sample_panel.png")
