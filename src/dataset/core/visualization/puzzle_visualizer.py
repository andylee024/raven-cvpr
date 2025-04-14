import os
import json
import time
from PIL import Image
import matplotlib.pyplot as plt

from dataset.legacy.rendering import render_panel

class PuzzleVisualizer:
    """Visualizes Raven's Progressive Matrix puzzles."""
    
    def __init__(self, output_dir="output/puzzles"):
        """Initialize the puzzle visualizer."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def visualize_puzzles(self, puzzles, highlight_solution=False):
        """Visualize multiple puzzles and save to disk.
        
        Args:
            puzzles: List of puzzles to visualize
            highlight_solution: Whether to highlight the correct answer
            
        Returns:
            List of paths to saved visualizations
        """
        output_files = []
        
        for i, puzzle in enumerate(puzzles):
            # Create output filename
            timestamp = int(time.time())
            puzzle_name = puzzle['metadata']['name'].lower().replace(' ', '_')
            output_base = os.path.join(self.output_dir, f"{puzzle_name}_{i+1}_{timestamp}")
            
            # Save the puzzle components
            output_files.append(self._visualize_and_save_puzzle(puzzle, output_base, highlight_solution))
        
        return output_files
    
    def _visualize_and_save_puzzle(self, puzzle, output_base, highlight_solution=False):
        """Visualize a puzzle and save as separate files.
        
        Args:
            puzzle: Puzzle data
            output_base: Base filename without extension
            highlight_solution: Whether to highlight the correct answer
            
        Returns:
            Dict with paths to saved files
        """
        try:
            # Import visualization components
            
            # Save context grid
            context_file = f"{output_base}_context.png"
            self._save_context_grid(puzzle['context'], context_file)
            
            # Save candidate choices
            choices_file = f"{output_base}_choices.png"
            self._save_candidate_choices(puzzle['candidates'], puzzle['target'], choices_file, highlight_solution)
            
            # Save combined image
            combined_file = f"{output_base}_combined.png"
            self._combine_images(context_file, choices_file, combined_file)
            
            # Save metadata
            metadata_file = f"{output_base}.json"
            self._save_puzzle_metadata(puzzle, metadata_file, combined_file)
            
            # Return paths to all saved files
            return {
                'context': context_file,
                'choices': choices_file,
                'combined': combined_file,
                'metadata': metadata_file
            }
            
        except Exception as e:
            print(f"Error visualizing puzzle: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _save_context_grid(self, context, output_file):
        """Save the 3x3 context grid as a separate file."""
        from dataset.legacy.rendering import render_panel
        
        # Create figure with white background
        fig = plt.figure(figsize=(7.5, 7.5), facecolor='white')
        
        # Draw the 3x3 grid (8 panels + question mark)
        for i, panel in enumerate(context):
            row = i // 3
            col = i % 3
            
            if row == 2 and col == 2:
                continue  # Skip bottom right as it's the answer
                
            # Calculate position
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
        
        # Save the figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        
        return output_file
    
    def _save_candidate_choices(self, candidates, target_idx, output_file, highlight_solution=False):
        """Save the candidate choices as a separate file."""
        from dataset.legacy.rendering import render_panel
        
        # Letter labels for answers
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        # Create a figure with white background
        fig = plt.figure(figsize=(10, 5), facecolor='white')
        
        # Calculate panel sizes and positions
        panel_width = 0.15
        panel_height = 0.35
        horiz_space = 0.02
        
        # Starting positions
        top_row_bottom = 0.55
        bottom_row_bottom = 0.1
        
        # First row of candidates (A-D)
        for i in range(4):
            # Calculate position with spacing
            left = 0.1 + i * (panel_width + horiz_space)
            bottom = top_row_bottom
            
            # Create axis
            ax = fig.add_axes([left, bottom, panel_width, panel_height])
            ax.imshow(render_panel(candidates[i]), cmap='gray')
            
            # Add border (red for correct answer if highlight_solution is True)
            border_color = 'red' if (i == target_idx and highlight_solution) else 'black'
            border_width = 2 if (i == target_idx and highlight_solution) else 1
            
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
            # Calculate position with spacing
            left = 0.1 + i * (panel_width + horiz_space)
            bottom = bottom_row_bottom
            
            # Create axis
            ax = fig.add_axes([left, bottom, panel_width, panel_height])
            ax.imshow(render_panel(candidates[i+4]), cmap='gray')
            
            # Add border (red for correct answer if highlight_solution is True)
            border_color = 'red' if (i+4 == target_idx and highlight_solution) else 'black'
            border_width = 2 if (i+4 == target_idx and highlight_solution) else 1
            
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color(border_color)
                spine.set_linewidth(border_width)
                
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Add letter label below
            fig.text(left + panel_width/2, bottom - 0.05, labels[i+4], 
                    ha='center', va='center', fontsize=16)
        
        # Save the figure
        plt.savefig(output_file, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        
        return output_file
    
    def _combine_images(self, context_file, choices_file, output_file):
        """Combine context and choices images into a single file."""
        # Open the images
        context_img = Image.open(context_file)
        choices_img = Image.open(choices_file)
        
        # Get the dimensions
        context_width, context_height = context_img.size
        choices_width, choices_height = choices_img.size
        
        # Create a new image with enough height for both
        width = max(context_width, choices_width)
        height = context_height + choices_height
        
        # Create new image with white background
        combined_img = Image.new('RGB', (width, height), (255, 255, 255))
        
        # Paste the images
        combined_img.paste(context_img, ((width - context_width) // 2, 0))
        combined_img.paste(choices_img, ((width - choices_width) // 2, context_height))
        
        # Save the combined image
        combined_img.save(output_file, 'PNG')
        
        return output_file
    
    def _save_puzzle_metadata(self, puzzle, output_path, combined_image_path):
        """Save puzzle metadata as JSON."""
        # Get the answer letter (A-H)
        answer_idx = puzzle['target']
        answer_letter = chr(65 + answer_idx)  # Convert 0-7 to A-H
        
        # Create metadata dictionary
        metadata = {
            "image_path": combined_image_path,
            "answer": answer_letter,
            "rule_type": puzzle['rule_type'],
            "attribute": puzzle['attr'],
            "value": puzzle['value'],
            "config": puzzle['config'],
            "description": puzzle['metadata']['description'],
            "difficulty": puzzle['metadata']['difficulty']
        }
        
        # Save as JSON
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return output_path
