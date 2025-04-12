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


if __name__ == "__main__":
    # Run the test
    panel = generate_sample_panel()
    visualize_panel(panel, "test_output/sample_panel.png")
