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
    
    parser.add_argument("--puzzles-per-config", type=int, default=5,
                        help="Number of puzzles to generate per configuration")
    
    parser.add_argument("--max-attempts", type=int, default=30,
                        help="Maximum attempts per configuration/rule combination")
    
    return parser.parse_args()

def visualize_puzzle(puzzle, output_file):
    """Visualize a puzzle and save as PNG."""
    try:
        context = puzzle['context']
        answer = puzzle['answer']
        
        # Create a title based on puzzle data
        title = f"{puzzle['config']}: {puzzle['rule_type']} Rule\n"
        title += f"Attribute: {puzzle['attr']}"
        if puzzle['value'] is not None:
            title += f" Value: {'+' + str(puzzle['value']) if isinstance(puzzle['value'], int) and puzzle['value'] > 0 else puzzle['value']}"
        
        # Create a figure with a 3x3 grid
        fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(4, 3, height_ratios=[1, 3, 3, 3])
        
        # Add the title
        title_ax = fig.add_subplot(gs[0, :])
        title_ax.text(0.5, 0.5, title, ha='center', va='center', fontsize=12)
        title_ax.axis('off')
        
        # Render context panels
        for i, panel in enumerate(context):
            row = (i // 3) + 1
            col = i % 3
            ax = fig.add_subplot(gs[row, col])
            ax.imshow(render_panel(panel), cmap='gray')
            
            # Add border
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color('black')
                spine.set_linewidth(2)
                
            ax.axis('on')
            ax.set_xticks([])
            ax.set_yticks([])
        
        # Render answer panel
        ax = fig.add_subplot(gs[3, 2])
        ax.imshow(render_panel(answer), cmap='gray')
        
        # Add red border
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('red')
            spine.set_linewidth(3)
        
        ax.axis('on')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Save figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        return True
    except Exception as e:
        print(f"Error visualizing puzzle: {e}")
        traceback.print_exc()
        print(f"Error rendering context panel {i}: {e}")
        print(f"Rule attribute: {puzzle['attr']}, type: {puzzle['rule_type']}")
        plt.close('all')  # Make sure to close any open figures
        return False
    

def ensure_directory(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

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
        # "Progression",
        # "Constant",
        # "Arithmetic",
        "DistributeThree"  # TODO: debug why this is not working
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
            print(f"  Rule type: {rule_type}")
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
                        # Create output filename
                        puzzle_name = f"puzzle_{success_count+1}_{puzzle['attr']}.png"
                        output_file = os.path.join(rule_dir, puzzle_name)
                        
                        # Visualize and save
                        vis_result = visualize_puzzle(puzzle, output_file)
                        
                        # Only count as success if both visualization worked
                        if vis_result:
                            success_count += 1
                            print(f"Generated puzzle {success_count}/{args.puzzles_per_config}: {puzzle['attr']}")
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
