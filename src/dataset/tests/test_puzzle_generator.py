#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate and visualize a tensor-based RAVEN puzzle.
This is a simplified test script for the new puzzle generator.
"""

from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import os
import random

from dataset.core.generators.puzzle_generator import TensorPuzzleGenerator
from dataset.utils.panel_utils import visualize_panel

def main():
    """Generate and visualize a tensor-based RAVEN puzzle."""
    # Create output directory
    output_dir = "output/puzzle_test"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating puzzle...")
    
    # Create the puzzle generator
    generator = TensorPuzzleGenerator()
    puzzle = generator.generate()
    grid = puzzle["grid"]
    
    # Visualize the puzzle
    output_file = os.path.join(output_dir, f"puzzle.png")
    visualize_puzzle_grid(grid, output_file)
    
    print(f"Puzzle generated and saved to: {output_file}")
    

def visualize_puzzle_grid(grid, output_file):
    """Visualize a 3×3 grid of panels and save as PNG.
    
    Args:
        grid: 3×3 grid of TensorPanels
        output_file: Path to save the visualization
    """
    # Create figure with white background
    fig = plt.figure(figsize=(10, 10), facecolor='white')
    
    # Create a grid layout with more spacing
    gs = GridSpec(3, 3, figure=fig)
    # Increase the spacing between panels
    gs.update(wspace=0.15, hspace=0.15)
    
    # Plot each panel
    for row in range(3):
        for col in range(3):
            # Create an axis for this panel
            ax = fig.add_subplot(gs[row, col])
            
            # Get the panel and convert to AoT for visualization
            panel = grid[row][col]
            aot_panel = panel.to_aot()
            
            # Render the panel
            from dataset.legacy.rendering import render_panel
            img = render_panel(aot_panel.raw)
            
            # Display the image
            ax.imshow(img, cmap='gray')
            ax.axis('on')  # Show the axis
            
            # Add prominent border
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color('black')
                spine.set_linewidth(2)  # Thicker border
            
            # Remove tick marks but keep the frame
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Add row/col numbers for easier reference
            ax.set_title(f"({row},{col})", fontsize=12)
    
    # Add grid lines at the figure level
    fig.tight_layout()
    
    # Add a dark background between panels for greater contrast
    fig.patch.set_facecolor('#e0e0e0')  # Light gray background
    
    # Save figure
    plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    return True

if __name__ == "__main__":
    main()