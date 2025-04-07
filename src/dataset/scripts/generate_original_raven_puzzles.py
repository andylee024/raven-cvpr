#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate multiple RAVEN puzzles with progression rules.

This script generates a specified number of puzzles using progression rules,
saving them as PNG images.

TODO: 
- The loop is getting stuck after 1st iteration, i don't know why though.
"""

import os
import argparse
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Import from existing codebase
from dataset.core.rules.progression import ProgressionRule
from dataset.build_tree import (build_distribute_four, build_distribute_nine, 
                              build_center_single, build_left_center_single_right_center_single,
                              build_up_center_single_down_center_single)
from dataset.legacy.Rule import Rule_Wrapper
from dataset.rendering import render_panel

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate multiple RAVEN puzzles")
    
    # Rule options
    parser.add_argument("--count", type=int, default=10,
                      help="Number of puzzles to generate")
    
    # Output options
    parser.add_argument("--output-dir", type=str, default="output_puzzles",
                      help="Output directory for the visualizations")
    
    parser.add_argument("--seed", type=int, default=None,
                      help="Random seed for reproducibility")
    
    return parser.parse_args()

def get_random_root():
    """Get a random puzzle configuration."""
    configs = {
        "center_single": build_center_single,
        "distribute_four": build_distribute_four,
        "distribute_nine": build_distribute_nine,
        "left_right": build_left_center_single_right_center_single,
        "up_down": build_up_center_single_down_center_single
    }
    
    config_name = random.choice(list(configs.keys()))
    root = configs[config_name]()
    return config_name, root

def get_random_rule_group():
    """Get a random rule configuration."""
    attributes = ["Number", "Position", "Type", "Size", "Color"]
    attribute = random.choice(attributes)
    increment_value = random.choice([-2, -1, 1, 2])

    # TODO : add the ability to sample multiple rules
    left_rule = ProgressionRule(attr=attribute, value=increment_value)
    right_rule = ProgressionRule(attr=attribute, value=increment_value)

    # the number of rules dictates the configuration
    return [[left_rule]] # TODO : add the ability to sample multiple rules
    # return [[left_rule], [right_rule]]

def get_random_puzzle_root():
    """Build a valid root for a puzzle configuration and rule groups."""
    _, root = get_random_root()
    rule_group = get_random_rule_group()

    new_root = root.prune(rule_group)
    if new_root is None:
        print("Pruning failed! The rule is not compatible with this configuration.")
        return None

    start_node = new_root.sample()
    return start_node, rule_group


def generate_puzzle():
    """Generate a puzzle with a progression rule.
    
    Args:
        root: The base AoT configuration
        attr: Optional attribute for progression
        value: Optional progression value
        
    Returns:
        tuple: (context, answer, attr, value, secondary_attr)
    """
    # randomly sample configuration
    _, root = get_random_root()

    # randomly sample rule
    rule_group = get_random_rule_group()
    first_rule = rule_group[0][0]

    # generate valid tree w/ pruning
    new_root = root.prune(rule_group)

    # pruning is failing! 
    if new_root is None:
        return None

    # sample the tree to create the first panel
    start_node = new_root.sample()
    
    # Generate the first row
    row_1_1 = copy.deepcopy(start_node)
    row_1_2 = first_rule.apply_rule(row_1_1)
    row_1_3 = first_rule.apply_rule(row_1_2)
    
    # Generate the second row
    row_2_1 = copy.deepcopy(start_node)
    row_2_1.resample(True)  # Resample to create variation
    row_2_2 = first_rule.apply_rule(row_2_1)
    row_2_3 = first_rule.apply_rule(row_2_2)
    
    # Generate the third row (with answer)
    row_3_1 = copy.deepcopy(start_node)
    row_3_1.resample(True)
    row_3_2 = first_rule.apply_rule(row_3_1)
    row_3_3 = first_rule.apply_rule(row_3_2)  # This is the answer
    
    # Create context (all panels except the answer)
    context = [row_1_1, row_1_2, row_1_3, row_2_1, row_2_2, row_2_3, row_3_1, row_3_2]
    return {'context': context, 
            'answer': row_3_3, 
            'attr': first_rule.attr, 
            'value': first_rule.value} 

def visualize_puzzle(context, answer, output_file, title):
    """Visualize a puzzle and save as PNG.
    
    Args:
        context (list): Context panels
        answer (object): Answer panel
        output_file (str): Output filename
        title (str): Title for the visualization
    """
    # Create a figure with a 3x3 grid
    fig = plt.figure(figsize=(10, 10))
    gs = GridSpec(4, 3, height_ratios=[1, 3, 3, 3])
    
    # Add a title
    title_ax = fig.add_subplot(gs[0, :])
    title_ax.text(0.5, 0.5, title, ha='center', va='center', fontsize=12)
    title_ax.axis('off')
    
    # Render all context panels
    for i, panel in enumerate(context):
        row = (i // 3) + 1
        col = i % 3
        ax = fig.add_subplot(gs[row, col])
        ax.imshow(render_panel(panel), cmap='gray')
        
        # Add a black border around each panel
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(2)
            
        ax.axis('on')
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Render the answer in the bottom right
    ax = fig.add_subplot(gs[3, 2])
    ax.imshow(render_panel(answer), cmap='gray')
    
    # Mark the answer position with a red border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('red')
        spine.set_linewidth(3)
    
    ax.axis('on')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Save the figure
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()


def main():
    """Main function."""
    args = parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Generate multiple puzzles
    for i in range(args.count):

        # Generate the puzzle 
        puzzle_return = generate_puzzle()

        # If puzzle generation fails, try again w/ new combo
        if puzzle_return is None:
            print(f"Generated puzzle {i+1}/{args.count} : pruning failed")
            continue
        
        # Extract the puzzle components
        context = puzzle_return['context']
        answer = puzzle_return['answer']
        attr = puzzle_return['attr']
        value = puzzle_return['value']
        
        # Create a title for the puzzle
        title = f"Puzzle {i+1}: \n{attr} Progression {value:+d}"
        
        # Create an output filename
        output_file = os.path.join(args.output_dir, f"puzzle_{i+1}_{attr}_{value:+d}.png")
        
        # Visualize and save the puzzle
        visualize_puzzle(context, answer, output_file, title)
        
        print(f"Generated puzzle {i+1}/{args.count} : with {attr} progression {value:+d}")
    
    print(f"All {args.count} puzzles have been generated in {args.output_dir}")


if __name__ == "__main__":
    main()
