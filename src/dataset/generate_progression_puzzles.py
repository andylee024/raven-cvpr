#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a RAVEN puzzle with progression rules.

This script generates a RAVEN puzzle using progression rules with the distribute_four 
configuration, visualizes all 9 panels in a single image, and allows configuration
through command-line options.
"""

import os
import sys
import argparse
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Import from existing codebase
from Rule import Rule_Wrapper
from build_tree import build_distribute_four
from rendering import render_panel
from serialize import serialize_rules, serialize_aot


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate a RAVEN puzzle with progression rules")
    
    # Rule options
    parser.add_argument("--attr", type=str, default="Number",
                      choices=["Number", "Position", "Type", "Size", "Color"],
                      help="Attribute to apply progression to")
    
    parser.add_argument("--value", type=int, default=1,
                      choices=[-2, -1, 1, 2],
                      help="Progression value (positive or negative)")
    
    # Output options
    parser.add_argument("--output", type=str, default="output_puzzles/progression_puzzle.png",
                      help="Output filename for the visualization")
    
    parser.add_argument("--save-data", action="store_true",
                      help="Save puzzle data in NPZ format")
    
    parser.add_argument("--seed", type=int, default=None,
                      help="Random seed for reproducibility")
    
    return parser.parse_args()


def create_progression_rule(attr, value, component_idx=0):
    """Create a progression rule for the specified attribute.
    
    Args:
        attr (str): Attribute to apply progression to
        value (int): Progression value
        component_idx (int): Component index
        
    Returns:
        Rule: A progression rule
    """
    return Rule_Wrapper("Progression", attr, [value], component_idx)


def generate_puzzle(attr, value, seed=None):
    """Generate a puzzle with a progression rule.
    
    Args:
        attr (str): Attribute for progression
        value (int): Progression value
        seed (int, optional): Random seed
        
    Returns:
        tuple: (context, answer, rule_groups)
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Build the base AoT with distribute_four configuration
    root = build_distribute_four()
    
    # Create progression rules
    progression_rule = create_progression_rule(attr, value)
    
    # Add a secondary rule for a more interesting puzzle if primary rule is Number or Position
    secondary_rule = None
    if attr in ["Number", "Position"]:
        secondary_attrs = ["Type", "Size", "Color"]
        secondary_attr = random.choice(secondary_attrs)
        secondary_rule = create_progression_rule(secondary_attr, value)
    
    # Group rules
    rule_groups = [[progression_rule]]
    if secondary_rule:
        rule_groups[0].append(secondary_rule)
    
    # Prune the AoT to apply constraints
    new_root = root.prune(rule_groups)
    if new_root is None:
        # Try with opposite value if pruning failed
        progression_rule = create_progression_rule(attr, -value)
        rule_groups = [[progression_rule]]
        if secondary_rule:
            secondary_rule = create_progression_rule(secondary_attr, -value)
            rule_groups[0].append(secondary_rule)
        new_root = root.prune(rule_groups)
    
    # Sample the tree to create the first panel
    start_node = new_root.sample()
    
    # Generate the first row
    row_1_1 = copy.deepcopy(start_node)
    row_1_2 = progression_rule.apply_rule(row_1_1)
    row_1_3 = progression_rule.apply_rule(row_1_2)
    
    if secondary_rule:
        row_1_2 = secondary_rule.apply_rule(row_1_1, row_1_2)
        row_1_3 = secondary_rule.apply_rule(row_1_2, row_1_3)
    
    # Generate the second row
    row_2_1 = copy.deepcopy(start_node)
    row_2_1.resample(True)  # Resample to create variation
    row_2_2 = progression_rule.apply_rule(row_2_1)
    row_2_3 = progression_rule.apply_rule(row_2_2)
    
    if secondary_rule:
        row_2_2 = secondary_rule.apply_rule(row_2_1, row_2_2)
        row_2_3 = secondary_rule.apply_rule(row_2_2, row_2_3)
    
    # Generate the third row (with answer)
    row_3_1 = copy.deepcopy(start_node)
    row_3_1.resample(True)
    row_3_2 = progression_rule.apply_rule(row_3_1)
    row_3_3 = progression_rule.apply_rule(row_3_2)  # This is the answer
    
    if secondary_rule:
        row_3_2 = secondary_rule.apply_rule(row_3_1, row_3_2)
        row_3_3 = secondary_rule.apply_rule(row_3_2, row_3_3)
    
    # Create context (all panels except the answer)
    context = [row_1_1, row_1_2, row_1_3, row_2_1, row_2_2, row_2_3, row_3_1, row_3_2]
    
    return context, row_3_3, rule_groups, secondary_attr if secondary_rule else None


def visualize_puzzle(context, answer, output_file, rule_info):
    """Visualize a puzzle with its context and answer.
    
    Args:
        context (list): List of context panels
        answer (object): Answer panel
        output_file (str): Output filename
        rule_info (str): Information about the rules used
    """
    # Create a figure with a 3x3 grid
    fig = plt.figure(figsize=(10, 10))
    gs = GridSpec(4, 3, height_ratios=[1, 3, 3, 3])
    
    # Add a title with rule information
    title_ax = fig.add_subplot(gs[0, :])
    title_ax.text(0.5, 0.5, rule_info, ha='center', va='center', fontsize=12)
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
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Puzzle visualization saved to {output_file}")


def save_puzzle_data(context, answer, rule_groups, output_base):
    """Save puzzle data in NPZ format.
    
    Args:
        context (list): List of context panels
        answer (object): Answer panel
        rule_groups (list): List of rule groups
        output_base (str): Base name for output files
    """
    # Render images
    images = [render_panel(panel) for panel in context]
    images.append(np.zeros_like(images[0]))  # Empty panel for answer position
    answer_image = render_panel(answer)
    
    # Add the answer at the end
    all_images = images + [answer_image]
    
    # Create metadata
    meta_matrix, meta_target = serialize_rules(rule_groups)
    structure, meta_structure = serialize_aot(context[0])
    
    # Save as npz
    np.savez(f"{output_base}.npz", 
             image=all_images,
             target=8,  # Answer is always at index 8
             meta_matrix=meta_matrix,
             meta_target=meta_target,
             structure=structure,
             meta_structure=meta_structure)
    
    print(f"Puzzle data saved to {output_base}.npz")


def main():
    """Main function."""
    args = parse_args()
    
    # Generate puzzle
    context, answer, rule_groups, secondary_attr = generate_puzzle(
        args.attr, args.value, args.seed
    )
    
    # Create rule information string
    rule_info = f"Progression Puzzle (Distribute Four)\nPrimary Rule: {args.attr} Progression {args.value:+d}"
    if secondary_attr:
        rule_info += f"\nSecondary Rule: {secondary_attr} Progression {args.value:+d}"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Visualize puzzle
    visualize_puzzle(context, answer, args.output, rule_info)
    
    # Save puzzle data if requested
    # if args.save_data:
    #     output_base = os.path.splitext(args.output)[0]
    #     save_puzzle_data(context, answer, rule_groups, output_base)
    
    print(f"Successfully generated progression puzzle with {args.attr} progression {args.value:+d}")
    if secondary_attr:
        print(f"Added secondary {secondary_attr} progression {args.value:+d}")


if __name__ == "__main__":
    main()