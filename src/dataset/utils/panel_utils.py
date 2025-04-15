import matplotlib.pyplot as plt
import os
import random

from dataset.core.aot.attributes import ATTRIBUTES, CONSTANTS
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.legacy.rendering import render_panel
from dataset.utils.entity_utils import sample_entity_tensor
from dataset.utils.sampling_utils import get_random_positions


def add_entities_to_panel(panel, n=1):
    """Return a panel with n entities added to it."""

    # validate entities within range
    target_entities = panel.total_entities + n
    if target_entities > CONSTANTS.MAX_ENTITIES.value:
        raise ValueError(f"Cannot increase panel to {target_entities} entities > {CONSTANTS.MAX_ENTITIES.value}")

    # sample empty positions to fill 
    new_panel = panel.clone()
    new_panel_tensor = new_panel.tensor
    empty_positions = new_panel.get_empty_positions()
    empty_positions_to_fill = random.sample(empty_positions, n)

    # fill empty positions with new random entities
    for pos in empty_positions_to_fill:
        new_panel_tensor[pos[0], pos[1], :] = sample_entity_tensor()
    return TensorPanel(new_panel_tensor)

        
def remove_entities_from_panel(panel, n=1):
    """Return a panel with n entities removed from it."""

    # validate entities within range
    target_entities = panel.total_entities - n
    if target_entities < CONSTANTS.MIN_ENTITIES.value:
        raise ValueError(f"Cannot decrease panel to {target_entities} entities < {CONSTANTS.MIN_ENTITIES.value}")
    
    # sample filled positions to remove
    new_panel = panel.clone()
    new_panel_tensor = new_panel.tensor
    filled_positions = new_panel.get_filled_positions()
    filled_positions_to_remove = random.sample(filled_positions, n)

    # remove entities from filled positions
    for pos in filled_positions_to_remove:
        new_panel_tensor[pos[0], pos[1], :] = 0
    return TensorPanel(new_panel_tensor)

# 
# Pre-generated panels 
# 

def get_random_panel(n_entities=None):
    """Generate a panel with random entities."""
    panel = TensorPanel()
    panel_tensor = panel.tensor
    
    positions = get_random_positions(n_entities)
    for row, col in positions:
        panel_tensor[row, col, :] = sample_entity_tensor()
    
    return TensorPanel(panel_tensor)

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

def perturb_attribute(panel, position=None, attribute_name=None):
    """Perturb a single attribute of an entity at the given position.
    
    Args:
        panel: The panel to modify
        position: (row, col) position of the entity to modify. If None, a random filled position is chosen.
        attribute_name: Specific attribute to modify. If None, a random attribute is chosen.
    
    Returns:
        A new panel with the attribute perturbed
    """
    # Clone to avoid modifying the original
    result = panel.clone()
    
    # If no position specified, choose a random filled position
    filled_positions = panel.get_filled_positions()
    if not filled_positions:
        raise ValueError("Panel has no entities to perturb")
        
    if position is None:
        position = random.choice(filled_positions)
    
    row, col = position
    
    # If no attribute specified, choose a random one (excluding 'exists')
    valid_attributes = ['type', 'size', 'angle', 'color']
    if attribute_name is None:
        attribute_name = random.choice(valid_attributes)
    
    # Get the attribute properties
    attribute = ATTRIBUTES[attribute_name]
    attribute_index = attribute.index
    min_val = attribute.min_val
    max_val = attribute.max_val
    
    # Get current value
    current_value = panel.tensor[row, col, attribute_index].item()
    
    # Generate a new value that's different from the current one
    possible_values = list(range(min_val, max_val + 1))
    if current_value in possible_values and len(possible_values) > 1:
        possible_values.remove(current_value)
    
    new_value = random.choice(possible_values)
    
    # Set the new value
    result.tensor[row, col, attribute_index] = new_value
    
    return result
