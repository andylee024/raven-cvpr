
import matplotlib.pyplot as plt
import os

from dataset.core.puzzle_generator import PuzzleGenerator
from dataset.core.aot.aot_facade import AoTFacade
from dataset.legacy.rendering import render_panel

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
