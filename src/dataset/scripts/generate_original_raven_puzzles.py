#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate multiple RAVEN puzzles with different rules and configurations.

This script generates puzzles for all configurations and rule types,
saving them as PNG images.
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
from dataset.core.rules.constant import ConstantRule
from dataset.core.rules.arithmetic import ArithmeticRule
from dataset.core.rules.distribute_three import DistributeThreeRule
from dataset.build_tree import (build_distribute_four, build_distribute_nine, 
                              build_center_single, build_left_center_single_right_center_single,
                              build_up_center_single_down_center_single)

from dataset.rendering import render_panel

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate multiple RAVEN puzzles")
    
    # Rule options
    parser.add_argument("--puzzles-per-config", type=int, default=3,
                      help="Number of puzzles to generate per configuration")
    
    # Output options
    parser.add_argument("--output-dir", type=str, 
                      help="Output directory for the visualizations", 
                      default="/Users/andylee/Projects/raven-cvpr/output_puzzles")
    
    parser.add_argument("--seed", type=int, default=None,
                      help="Random seed for reproducibility")
    
    return parser.parse_args()

def get_all_configurations():
    """Get all available puzzle configurations."""
    configs = {
        "center_single": build_center_single,
        "distribute_four": build_distribute_four,
        "distribute_nine": build_distribute_nine,
        "left_right": build_left_center_single_right_center_single,
        "up_down": build_up_center_single_down_center_single
    }
    return configs

def get_random_rule(rule_type=None):
    """Get a random rule of the specified type."""
    attributes = ["Number", "Position", "Type", "Size", "Color"]
    attribute = random.choice(attributes)
    
    if rule_type is None:
        rule_type = random.choice(["Progression", "Constant", "Arithmetic", "DistributeThree"])
    
    if rule_type == "Progression":
        increment_value = random.choice([-2, -1, 1, 2])
        return ProgressionRule(attr=attribute, value=increment_value)

    elif rule_type == "Constant":
        return ConstantRule(attr=attribute)

    elif rule_type == "Arithmetic":
        value = random.choice([-1, 1])
        return ArithmeticRule(attr=attribute, value=value)

    elif rule_type == "DistributeThree":
        return DistributeThreeRule(attr=attribute)

    else:
        raise ValueError(f"Unknown rule type: {rule_type}")

def sample_rule_group(rule_type=None):
    """Sample a rule group of a specific type.
    
    Args:
        rule_type: Type of rule to sample (None for random)
        
    Returns:
        A list of rule groups
    """
    # For simplicity, we'll use a single rule
    left_rule = get_random_rule(rule_type)
    
    # For more complex puzzles, you can uncomment this to use multiple rules
    # right_rule = get_random_rule(rule_type)
    # return [[left_rule], [right_rule]]
    
    return [[left_rule]]

def generate_puzzle(config_name, config_builder, rule_type=None):
    """Generate a puzzle with the specified configuration and rule type.
    
    Args:
        config_name: Name of the configuration to use
        config_builder: Function to build the configuration
        rule_type: Type of rule to use (None for random)
        
    Returns:
        Dictionary with puzzle information or None if generation failed
    """
    # Build the configuration
    root = config_builder()
    
    # Sample a rule group
    rule_group = sample_rule_group(rule_type)
    first_rule = rule_group[0][0]

    # Generate valid tree w/ pruning
    new_root = root.prune(rule_group)

    # If pruning fails, return None
    if new_root is None:
        return None

    # Sample the tree to create the first panel
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
    return {
        'context': context, 
        'answer': row_3_3, 
        'attr': first_rule.attr, 
        'value': getattr(first_rule, 'value', None),
        'config': config_name,
        'rule_type': first_rule.name
    }

def visualize_puzzle(context, answer, output_file, title):
    """Visualize a puzzle and save as PNG.
    
    Args:
        context: Context panels
        answer: Answer panel
        output_file: Output filename
        title: Title for the visualization
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
    
    # Get all configurations
    configs = get_all_configurations()
    
    # Get all rule types
    rule_types = ["Progression", "Constant", "Arithmetic", "DistributeThree"]
    
    # Track counts
    total_generated = 0
    total_failures = 0
    
    # Generate puzzles for each configuration
    for config_name, config_builder in configs.items():
        config_dir = os.path.join(args.output_dir, config_name)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        print(f"\nGenerating puzzles for configuration: {config_name}")
        
        # Try to generate puzzles for each rule type
        for rule_type in rule_types:
            rule_dir = os.path.join(config_dir, rule_type)
            if not os.path.exists(rule_dir):
                os.makedirs(rule_dir)
                
            print(f"  Rule type: {rule_type}")
            
            # Generate specified number of puzzles per rule type
            success_count = 0
            attempt_count = 0
            
            while success_count < args.puzzles_per_config and attempt_count < args.puzzles_per_config * 5:
                attempt_count += 1
                
                # Generate the puzzle
                puzzle_data = generate_puzzle(config_name, config_builder, rule_type)
                
                # If puzzle generation fails, try again
                if puzzle_data is None:
                    total_failures += 1
                    continue
                
                # Extract the puzzle components
                context = puzzle_data['context']
                answer = puzzle_data['answer']
                attr = puzzle_data['attr']
                value = puzzle_data.get('value')
                
                # Create a title for the puzzle
                if value is not None:
                    title = f"{config_name}: {rule_type} Rule\nAttribute: {attr} Value: {'+' + str(value) if isinstance(value, int) and value > 0 else value}"
                else:
                    title = f"{config_name}: {rule_type} Rule\nAttribute: {attr}"
                
                # Create an output filename
                output_file = os.path.join(rule_dir, f"puzzle_{success_count+1}_{attr}.png")
                
                # Visualize and save the puzzle
                visualize_puzzle(context, answer, output_file, title)
                
                success_count += 1
                total_generated += 1
                
                print(f"Generated puzzle {success_count}/{args.puzzles_per_config}: {attr} (saved to {output_file})")
    
    print(f"\nCompleted generation: {total_generated} puzzles generated")
    print(f"Failed attempts: {total_failures}")
    print(f"All puzzles have been generated in {args.output_dir}")

if __name__ == "__main__":
    main()
