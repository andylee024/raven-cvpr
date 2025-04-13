
import matplotlib.pyplot as plt
import os
import random

from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.legacy.rendering import render_panel

def get_uniform_triangle_panel():
    """Generate a panel with uniform triangles."""
    panel = TensorPanel()
    
    for row in range(3):
        for col in range(3):
            panel.set_attr(row, col, 'exists', 1)       # exists = True
            panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
            panel.set_attr(row, col, 'size', 3)         # size = 3 (medium)
            panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
            panel.set_attr(row, col, 'color', 1)        # color = 1 (green)
    
    return panel

def get_gradient_triangle_panel():
    """Generate a panel with triangles of gradient colors."""
    panel = TensorPanel()
    
    for row in range(3):
        for col in range(3):
            panel.set_attr(row, col, 'exists', 1)       # exists = True
            panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
            panel.set_attr(row, col, 'size', 3)         # size = 3 (medium)
            panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
            panel.set_attr(row, col, 'color', row * 3 + col + 1)  # gradient colors 1-9
    
    return panel

def get_random_panel(n_entities):
    """Generate a panel with random entities."""
    panel = TensorPanel()
    
    if n_entities is None:
        n_entities = random.randint(1, 9)
    
    positions = random.sample([(r, c) for r in range(3) for c in range(3)], n_entities)
    for row, col in positions:
        panel.set_attr(row, col, 'exists', 1)  # exists = True
        panel.set_attr(row, col, 'type', random.randint(1, 5))
        panel.set_attr(row, col, 'size', random.randint(1, 6))
        panel.set_attr(row, col, 'angle', random.randint(0, 7))
        panel.set_attr(row, col, 'color', random.randint(0, 9))
    
    return panel


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
