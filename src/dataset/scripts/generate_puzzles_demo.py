#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a RAVEN puzzle with progression rules.

This script generates puzzles using both old and new progression rule 
implementations, saving them as separate images for visual comparison.
"""

import os
import argparse
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# Import from existing codebase
from dataset.legacy.Rule import Rule_Wrapper
from dataset.legacy.build_tree import build_distribute_four
from dataset.legacy.rendering import render_panel

# Import from new implementation
from dataset.core.rules.progression import ProgressionRule

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate puzzles with old and new progression rules")
    
    # Rule options
    parser.add_argument("--attr", type=str, default="Number",
                      choices=["Number", "Position", "Type", "Size", "Color"],
                      help="Attribute to apply progression to")
    
    parser.add_argument("--value", type=int, default=1,
                      choices=[-2, -1, 1, 2],
                      help="Progression value (positive or negative)")
    
    # Output options
    parser.add_argument("--output-dir", type=str, default="/Users/andylee/Projects/raven-cvpr/output_puzzles",
                      help="Output directory for the visualizations")
    
    parser.add_argument("--seed", type=int, default=None,
                      help="Random seed for reproducibility")
    
    return parser.parse_args()


def generate_old_implementation(attr, value, start_node, secondary_attr=None):
    """Generate a puzzle using the old rule implementation.
    
    Args:
        attr (str): Attribute for progression
        value (int): Progression value
        start_node: Starting panel node
        secondary_attr: Optional secondary attribute
        
    Returns:
        tuple: (context, answer)
    """
    # Create progression rules
    progression_rule = Rule_Wrapper("Progression", attr, [value], 0)
    secondary_rule = None
    if secondary_attr:
        secondary_rule = Rule_Wrapper("Progression", secondary_attr, [value], 0)
    
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
    
    return context, row_3_3


def generate_new_implementation(attr, value, start_node, secondary_attr=None):
    """Generate a puzzle using the new rule implementation.
    
    Args:
        attr (str): Attribute for progression
        value (int): Progression value
        start_node: Starting panel node
        secondary_attr: Optional secondary attribute
        
    Returns:
        tuple: (context, answer)
    """
    # Create progression rules
    progression_rule = ProgressionRule(attr, value)
    secondary_rule = None
    if secondary_attr:
        secondary_rule = ProgressionRule(secondary_attr, value)
    
    # Generate the first row
    row_1_1 = copy.deepcopy(start_node)
    row_1_2 = progression_rule.apply(row_1_1)
    row_1_3 = progression_rule.apply(row_1_2)
    
    if secondary_rule:
        row_1_2 = secondary_rule.apply(row_1_1, row_1_2)
        row_1_3 = secondary_rule.apply(row_1_2, row_1_3)
    
    # Generate the second row
    row_2_1 = copy.deepcopy(start_node)
    row_2_1.resample(True)  # Resample to create variation
    row_2_2 = progression_rule.apply(row_2_1)
    row_2_3 = progression_rule.apply(row_2_2)
    
    if secondary_rule:
        row_2_2 = secondary_rule.apply(row_2_1, row_2_2)
        row_2_3 = secondary_rule.apply(row_2_2, row_2_3)
    
    # Generate the third row (with answer)
    row_3_1 = copy.deepcopy(start_node)
    row_3_1.resample(True)
    row_3_2 = progression_rule.apply(row_3_1)
    row_3_3 = progression_rule.apply(row_3_2)  # This is the answer
    
    if secondary_rule:
        row_3_2 = secondary_rule.apply(row_3_1, row_3_2)
        row_3_3 = secondary_rule.apply(row_3_2, row_3_3)
    
    # Create context (all panels except the answer)
    context = [row_1_1, row_1_2, row_1_3, row_2_1, row_2_2, row_2_3, row_3_1, row_3_2]
    
    return context, row_3_3


def visualize_puzzle(context, answer, output_file, title):
    """Visualize a puzzle.
    
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
    
    print(f"Puzzle visualization saved to {output_file}")


def main():
    """Main function."""
    args = parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    
    # Build the base AoT with distribute_four configuration
    root = build_distribute_four()
    
    # Create progression rules for pruning
    progression_rule = Rule_Wrapper("Progression", args.attr, [args.value], 0)
    
    # Add a secondary rule for a more interesting puzzle if primary rule is Number or Position
    secondary_rule = None
    secondary_attr = None
    if args.attr in ["Number", "Position"]:
        secondary_attrs = ["Type", "Size", "Color"]
        secondary_attr = random.choice(secondary_attrs)
        secondary_rule = Rule_Wrapper("Progression", secondary_attr, [args.value], 0)
    
    # Group rules for pruning
    rule_groups = [[progression_rule]]
    if secondary_rule:
        rule_groups[0].append(secondary_rule)
    
    # Prune the AoT to apply constraints
    new_root = root.prune(rule_groups)
    if new_root is None:
        # Try with opposite value if pruning failed
        args.value = -args.value
        print(f"Changed progression value to {args.value} due to pruning constraints")
        
        # Update rules with new value
        progression_rule = Rule_Wrapper("Progression", args.attr, [args.value], 0)
        rule_groups = [[progression_rule]]
        
        if secondary_attr:
            secondary_rule = Rule_Wrapper("Progression", secondary_attr, [args.value], 0)
            rule_groups[0].append(secondary_rule)
        
        new_root = root.prune(rule_groups)
    
    # Sample the tree to create the first panel
    start_node = new_root.sample()
    
    # Create rule information strings
    old_title = f"Original Implementation: {args.attr} Progression {args.value:+d}"
    new_title = f"New Implementation: {args.attr} Progression {args.value:+d}"
    
    if secondary_attr:
        old_title += f"\nSecondary Rule: {secondary_attr} Progression {args.value:+d}"
        new_title += f"\nSecondary Rule: {secondary_attr} Progression {args.value:+d}"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Generate and save puzzles using old implementation
    old_context, old_answer = generate_old_implementation(args.attr, args.value, start_node, secondary_attr)
    old_output = os.path.join(args.output_dir, f"old_puzzle_{args.attr}_{args.value:+d}.png")
    visualize_puzzle(old_context, old_answer, old_output, old_title)
    
    # Generate and save puzzles using new implementation
    new_context, new_answer = generate_new_implementation(args.attr, args.value, start_node, secondary_attr)
    new_output = os.path.join(args.output_dir, f"new_puzzle_{args.attr}_{args.value:+d}.png")
    visualize_puzzle(new_context, new_answer, new_output, new_title)
    
    print(f"Generated puzzles with {args.attr} progression {args.value:+d}")
    print(f"Old implementation saved to: {old_output}")
    print(f"New implementation saved to: {new_output}")


if __name__ == "__main__":
    main()
