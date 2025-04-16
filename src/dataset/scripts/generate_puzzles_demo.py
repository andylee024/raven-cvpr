#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate sample puzzles using the progression_color.json configuration.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from dataset.core.generators.puzzle_generator import PuzzleGenerator
from dataset.core.visualization.puzzle_visualizer import PuzzleVisualizer

def main():
    """Generate sample progression color puzzles."""

    # user inputs
    config_path = os.path.join(project_root, "src/dataset/config/progression_shape.json")
    num_puzzles = 3
    highlight_solution = True
    
    # Settings
    output_dir = os.path.join(project_root, "output", "puzzle_generator_demo")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create puzzle generator and visualizer
    generator = PuzzleGenerator(config_path)
    visualizer = PuzzleVisualizer(output_dir)
    
    # Generate puzzles
    print(f"Generating {num_puzzles} puzzles...")
    puzzles = generator.generate(num_puzzles=num_puzzles)
    
    # Visualize puzzles
    print(f"Saving puzzles to {output_dir}...")
    output_files = visualizer.visualize_puzzles(puzzles, highlight_solution)
    
    # Print summary
    print("\nGenerated puzzles:")
    for i, puzzle_files in enumerate(output_files):
        if puzzle_files:
            print(f"Puzzle {i+1}:")
            print(f"  - Combined: {puzzle_files['combined']}")
            print(f"  - Metadata: {puzzle_files['metadata']}")
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main() 