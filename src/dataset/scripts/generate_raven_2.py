#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate sample RAVEN puzzles for all configurations and rule types.
"""

import os
import argparse
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import traceback
import sys

from dataset.core.puzzle_generator import PuzzleGenerator
from dataset.rendering import render_panel

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate sample RAVEN puzzles")
    
    parser.add_argument("--output-dir", type=str, default="/Users/andylee/Projects/raven-cvpr/output_puzzles/demo_puzzles",
                        help="Output directory for puzzle visualizations")
    
    parser.add_argument("--puzzles-per-config", type=int, default=3,
                        help="Number of puzzles to generate per configuration")
    
    parser.add_argument("--max-attempts", type=int, default=30,
                        help="Maximum attempts per configuration/rule combination")
    
    return parser.parse_args()

def visualize_puzzle(puzzle, output_file):
    """Visualize a puzzle and save as PNG."""
    try:
        context = puzzle['context']
        candidates = puzzle['candidates']
        target_idx = puzzle['target']
        
        # Create figure with white background
        fig = plt.figure(figsize=(10, 12), facecolor='white')
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05, wspace=0.1, hspace=0.2)
        
        # Draw the 3x3 context grid
        render_context_grid(fig, context)
        
        # Draw the candidate choices
        render_candidate_choices(fig, candidates, target_idx)
        
        # Save figure without additional padding
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        return True
        
    except Exception as e:
        print(f"Error visualizing puzzle: {e}")
        traceback.print_exc()
        plt.close('all')
        return False

def render_context_grid(fig, context):
    """Render the 3x3 context grid of the puzzle.
    
    Args:
        fig: Matplotlib figure to draw on
        context: List of 8 context panels
    """
    # Main 3x3 grid for context panels
    for i, panel in enumerate(context):
        row = i // 3
        col = i % 3
        
        # Calculate position (in figure coordinates)
        left = 0.15 + col * 0.25
        bottom = 0.65 - row * 0.2
        width = 0.2
        height = 0.19
        
        # Create axis
        ax = fig.add_axes([left, bottom, width, height])
        ax.imshow(render_panel(panel), cmap='gray')
        
        # Add border
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1)
            
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Add question mark for missing panel
    ax = fig.add_axes([0.65, 0.25, 0.2, 0.19])
    ax.text(0.5, 0.5, '?', ha='center', va='center', fontsize=50)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1)
    ax.set_xticks([])
    ax.set_yticks([])

def render_candidate_choices(fig, candidates, target_idx):
    """Render the candidate choices with labels.
    
    Args:
        fig: Matplotlib figure to draw on
        candidates: List of 8 candidate panels
        target_idx: Index of the correct answer
    """
    # Letter labels for answers
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    # First row of candidates (A-D)
    for i in range(4):
        # Calculate position
        left = 0.15 + i * 0.2
        bottom = 0.175
        width = 0.17
        height = 0.17
        
        # Create axis
        ax = fig.add_axes([left, bottom, width, height])
        ax.imshow(render_panel(candidates[i]), cmap='gray')
        
        # Add border (red for correct answer)
        border_color = 'red' if i == target_idx else 'black'
        border_width = 2 if i == target_idx else 1
        
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(border_color)
            spine.set_linewidth(border_width)
            
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add letter label below
        fig.text(left + width/2, bottom - 0.03, labels[i], 
                ha='center', va='center', fontsize=16)
    
    # Second row of candidates (E-H)
    for i in range(4):
        # Calculate position
        left = 0.15 + i * 0.2
        bottom = 0.05
        width = 0.17
        height = 0.17
        
        # Create axis
        ax = fig.add_axes([left, bottom, width, height])
        ax.imshow(render_panel(candidates[i+4]), cmap='gray')
        
        # Add border (red for correct answer)
        border_color = 'red' if i+4 == target_idx else 'black'
        border_width = 2 if i+4 == target_idx else 1
        
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(border_color)
            spine.set_linewidth(border_width)
            
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add letter label below
        fig.text(left + width/2, bottom - 0.03, labels[i+4], 
                ha='center', va='center', fontsize=16)

def ensure_directory(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def visualize_and_save_puzzle(puzzle, output_base):
    """Visualize a puzzle and save context and choices as separate PNG files.
    
    Args:
        puzzle: Dictionary containing puzzle data
        output_base: Base filename without extension
        
    Returns:
        bool: True if visualization and saving succeeded
    """
    try:
        # Save context grid
        context_file = f"{output_base}_context.png"
        context_success = save_context_grid(puzzle['context'], context_file)
        
        # Save candidate choices
        choices_file = f"{output_base}_choices.png"
        choices_success = save_candidate_choices(puzzle['candidates'], puzzle['target'], choices_file)
        
        # Also save the complete puzzle (optional)
        complete_file = f"{output_base}.png"
        complete_success = save_complete_puzzle(puzzle, complete_file)
        
        # Return success only if both files were saved successfully
        return context_success and choices_success
        
    except Exception as e:
        print(f"Error visualizing puzzle: {e}")
        traceback.print_exc()
        return False

def save_context_grid(context, output_file):
    """Save the 3x3 context grid as a separate file."""
    try:
        # Create figure with white background
        fig = plt.figure(figsize=(7.5, 7.5), facecolor='white')
        
        # Draw the context grid
        render_context_grid(fig, context)
        
        # Save the figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        return True
    except Exception as e:
        print(f"Error saving context grid: {e}")
        traceback.print_exc()
        plt.close('all')
        return False

def save_candidate_choices(candidates, target_idx, output_file):
    """Save the candidate choices as a separate file."""
    try:
        # Create a figure with white background
        # Increase width and height to provide more space between panels
        fig = plt.figure(figsize=(10, 5), facecolor='white')
        
        # Use a modified version of render_candidate_choices with better spacing
        render_candidate_choices_separated(fig, candidates, target_idx)
        
        # Save the figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        return True
    except Exception as e:
        print(f"Error saving candidate choices: {e}")
        traceback.print_exc()
        plt.close('all')
        return False

def render_candidate_choices_separated(fig, candidates, target_idx):
    """Render the candidate choices with labels, ensuring they don't overlap.
    
    Args:
        fig: Matplotlib figure to draw on
        candidates: List of 8 candidate panels
        target_idx: Index of the correct answer
    """
    # Letter labels for answers
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    # Set up grid layout that ensures panels don't overlap
    # Use fixed positions with more spacing between panels
    
    # Calculate panel sizes and positions
    panel_width = 0.15   # Reduced from 0.17
    panel_height = 0.35  # Increased for better proportions
    horiz_space = 0.02   # Space between columns
    vert_space = 0.1     # Space between rows
    
    # Starting positions
    top_row_bottom = 0.55
    bottom_row_bottom = 0.1
    
    # First row of candidates (A-D)
    for i in range(4):
        # Calculate position with increased spacing
        left = 0.1 + i * (panel_width + horiz_space)
        bottom = top_row_bottom
        
        # Create axis
        ax = fig.add_axes([left, bottom, panel_width, panel_height])
        ax.imshow(render_panel(candidates[i]), cmap='gray')
        
        # Add border (red for correct answer)
        border_color = 'red' if i == target_idx else 'black'
        border_width = 2 if i == target_idx else 1
        
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(border_color)
            spine.set_linewidth(border_width)
            
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add letter label below
        fig.text(left + panel_width/2, bottom - 0.05, labels[i], 
                ha='center', va='center', fontsize=16)
    
    # Second row of candidates (E-H)
    for i in range(4):
        # Calculate position with increased spacing
        left = 0.1 + i * (panel_width + horiz_space)
        bottom = bottom_row_bottom
        
        # Create axis
        ax = fig.add_axes([left, bottom, panel_width, panel_height])
        ax.imshow(render_panel(candidates[i+4]), cmap='gray')
        
        # Add border (red for correct answer)
        border_color = 'red' if i+4 == target_idx else 'black'
        border_width = 2 if i+4 == target_idx else 1
        
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(border_color)
            spine.set_linewidth(border_width)
            
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add letter label below
        fig.text(left + panel_width/2, bottom - 0.05, labels[i+4], 
                ha='center', va='center', fontsize=16)

def save_complete_puzzle(puzzle, output_file):
    """Save the complete puzzle as a single file."""
    try:
        context = puzzle['context']
        candidates = puzzle['candidates']
        target_idx = puzzle['target']
        
        # Create a larger figure to accommodate the non-overlapping candidate layout
        fig = plt.figure(figsize=(10, 15), facecolor='white')
        
        # Add more vertical space for context and separated candidates
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05, hspace=0.4)
        
        # Draw context grid (positioned at the top of the figure)
        ax_context = fig.add_axes([0.05, 0.5, 0.9, 0.45])
        ax_context.axis('off')
        render_context_grid(fig, context)
        
        # Draw candidate choices (positioned at the bottom with more space)
        render_candidate_choices_separated(fig, candidates, target_idx)
        
        # Save figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        return True
    except Exception as e:
        print(f"Error saving complete puzzle: {e}")
        traceback.print_exc()
        plt.close('all')
        return False

def main():
    """Main function."""
    args = parse_args()
    
    # Create output directory
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Configurations to process
    configs = [
        # "center_single",
        # "distribute_four",
        "distribute_nine",
        # "left_right",
        # "up_down",
        # "in_out_center_single",
        # "in_out_distribute_four"
    ]
    
    # Rule types to generate
    rule_types = [
        "Progression",
        # "Constant",
        "Arithmetic",
        "DistributeThree"  
    ]
    
    # Create puzzle generator
    generator = PuzzleGenerator(max_attempts=10)
    
    # Track statistics
    total_attempts = 0
    total_successes = 0
    total_failures = 0
    failed_combos = []
    
    for config_name in configs:
        # Setup directory for this configuration
        config_dir = os.path.join(args.output_dir, config_name)
        ensure_directory(config_dir)
            
        print(f"\nGenerating puzzles for {config_name}:")
        
        # Generate for each rule type
        for rule_type in rule_types:
            # Setup directory for this rule type
            print(f"Rule type: {rule_type}")
            rule_dir = os.path.join(config_dir, rule_type)
            ensure_directory(rule_dir)
                
            # Generate specified number of puzzles
            success_count = 0
            failure_count = 0
            attempt_count = 0
            
            while success_count < args.puzzles_per_config and attempt_count < args.max_attempts:
                attempt_count += 1
                
                try:
                    # Generate puzzle
                    print(f"    Attempt {attempt_count}: ", end="", flush=True)
                    puzzle = generator.generate(config_name, rule_type)
                    
                    if puzzle:
                        # Create base output filename without extension
                        base_filename = f"puzzle_{success_count+1}_{puzzle['attr']}"
                        output_base = os.path.join(rule_dir, base_filename)
                        
                        # Visualize and save the puzzle components
                        vis_result = visualize_and_save_puzzle(puzzle, output_base)
                        
                        # Only count as success if visualization worked
                        if vis_result:
                            success_count += 1
                            print(f"Generated puzzle {success_count}/{args.puzzles_per_config}: {puzzle['attr']}")
                            print(f"    - Saved to: {output_base}_context.png and {output_base}_choices.png")
                        else:
                            failure_count += 1
                            print("Visualization failed - rendering issues detected")
                    else:
                        failure_count += 1
                        print("Generation failed")
                        
                except Exception as e:
                    failure_count += 1
                    print(f"Error: {e}")
                    print("Full stack trace:")
                    traceback.print_exc()
            
            # Update statistics
            total_attempts += attempt_count
            total_successes += success_count
            total_failures += failure_count
            
            # Record if we didn't meet the quota
            if success_count < args.puzzles_per_config:
                failed_combos.append((config_name, rule_type, success_count, failure_count))
    
    # Print summary
    print("\n=== Generation Summary ===")
    print(f"Total attempts: {total_attempts}")
    print(f"Total successful puzzles: {total_successes}")
    print(f"Total failed puzzles: {total_failures}")
    print(f"Success rate: {total_successes/(total_successes + total_failures):.1%}")
    
    if failed_combos:
        print("\nFailed to generate requested number of puzzles for:")
        for config, rule, success, failure in failed_combos:
            print(f"  - {config}/{rule}: Generated {success}/{args.puzzles_per_config} (Failures: {failure})")
    
    print("\nAll done! Puzzles saved to", args.output_dir)

if __name__ == "__main__":
    main()
