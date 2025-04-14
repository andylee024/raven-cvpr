import matplotlib.pyplot as plt
import os
import random
import torch

from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.aot.attributes import ATTRIBUTES
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.legacy.rendering import render_panel


def get_random_positions(n_entities=None):
    """Generate a list of random positions."""
    if n_entities is None:
        n_entities = random.randint(1, 9)
    return random.sample([(r, c) for r in range(3) for c in range(3)], n_entities)

def get_uniform_triangle_panel(n_entities=None):
    """Generate a panel with uniform triangles."""
    panel = TensorPanel()
    
    positions = get_random_positions(n_entities)
    for row, col in positions:
        panel.set_attr(row, col, 'exists', 1)       # exists = True
        panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
        panel.set_attr(row, col, 'size', 2)         # size = 3 (medium)
        panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
        panel.set_attr(row, col, 'color', 1)        # color = 1 (green)
    
    return panel

def get_gradient_triangle_panel(n_entities=None):
    """Generate a panel with triangles of gradient colors."""
    panel = TensorPanel()
    
    positions = get_random_positions(n_entities)
    for row, col in positions:
        panel.set_attr(row, col, 'exists', 1)       # exists = True
        panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
        panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
        panel.set_attr(row, col, 'size', 1)         # size = 3 (medium)
        panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
        panel.set_attr(row, col, 'color', row * 3 + col + 1)  # gradient colors 1-9
    
    return panel

def get_random_panel(n_entities=None):
    """Generate a panel with random entities."""
    panel = TensorPanel()
    
    positions = get_random_positions(n_entities)
    for row, col in positions:
        panel.set_attr(row, col, 'exists', 1)  # exists = True
        panel.set_attr(row, col, 'type', random.randint(1, 5))
        panel.set_attr(row, col, 'size', random.randint(1, 6))
        panel.set_attr(row, col, 'angle', random.randint(0, 7))
        panel.set_attr(row, col, 'color', random.randint(0, 9))
    
    return panel


def sample_entity(shape_type=None, size=None, angle=None, color=None):
    """Generate attribute values for an entity, sampling random values for unspecified attributes."""
    
    # Create tensor for [exists, type, size, angle, color]
    entity_tensor = torch.zeros(5, dtype=torch.int)
    
    exists_index = ATTRIBUTES['exists'].index
    type_index = ATTRIBUTES['type'].index
    size_index = ATTRIBUTES['size'].index
    angle_index = ATTRIBUTES['angle'].index
    color_index = ATTRIBUTES['color'].index

    entity_tensor[exists_index] = 1 # exists = 1 (b/c entity exists)
    entity_tensor[type_index] = shape_type if shape_type is not None else random.randint(1, 5)
    entity_tensor[size_index] = size if size is not None else random.randint(1, 6)
    entity_tensor[angle_index] = angle if angle is not None else random.randint(0, 7)
    entity_tensor[color_index] = color if color is not None else random.randint(0, 9)
    return entity_tensor

def visualize_panel(panel, output_path):
    """Visualize a single panel and save to file.
    
    Args:
        facade: AoTFacade containing the panel
        output_path: Path to save the visualization
    """
    if isinstance(panel, TensorPanel):
        panel = panel.to_aot()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Render the panel
    rendered_image = render_panel(panel.raw)
    
    # Save visualization
    plt.figure(figsize=(8, 8))
    plt.imshow(rendered_image, cmap='gray')
    plt.axis('off')
    plt.title("Distribute Nine Panel")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Panel visualization saved to: {output_path}")
