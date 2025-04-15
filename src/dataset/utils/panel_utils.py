import matplotlib.pyplot as plt
import os
import random
import torch

from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.aot.attributes import ATTRIBUTES, CONSTANTS
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
        panel.set_attr(row, col, 'type', random.randint(CONSTANTS.TYPE_MIN.value, CONSTANTS.TYPE_MAX.value))
        panel.set_attr(row, col, 'size', random.randint(CONSTANTS.SIZE_MIN.value, CONSTANTS.SIZE_MAX.value))
        panel.set_attr(row, col, 'angle', random.randint(CONSTANTS.ANGLE_MIN.value, CONSTANTS.ANGLE_MAX.value))
        panel.set_attr(row, col, 'color', random.randint(CONSTANTS.COLOR_MIN.value, CONSTANTS.COLOR_MAX.value))
    
    return panel


def sample_entity(shape_type=None, size=None, angle=None, color=None):
    """Generate attribute values for an entity, sampling random values for unspecified attributes."""
    
    # Create tensor for [exists, type, size, angle, color]
    entity_tensor = torch.zeros(5, dtype=torch.int)

    exists_attr = ATTRIBUTES['exists']
    shape_type_attr = ATTRIBUTES['type']
    size_attr = ATTRIBUTES['size']
    angle_attr = ATTRIBUTES['angle']
    color_attr = ATTRIBUTES['color']

    entity_tensor[exists_attr.index] = 1 # exists = 1 (b/c entity exists)

    if shape_type is not None:
        entity_tensor[shape_type_attr.index] = shape_type
    else:
        entity_tensor[shape_type_attr.index] = random.randint(shape_type_attr.min_val, shape_type_attr.max_val)

    if size is not None:
        entity_tensor[size_attr.index] = size
    else:
        entity_tensor[size_attr.index] = random.randint(size_attr.min_val, size_attr.max_val)

    if angle is not None:
        entity_tensor[angle_attr.index] = angle
    else:
        entity_tensor[angle_attr.index] = random.randint(angle_attr.min_val, angle_attr.max_val)

    if color is not None:
        entity_tensor[color_attr.index] = color
    else:
        entity_tensor[color_attr.index] = random.randint(color_attr.min_val, color_attr.max_val)
    return entity_tensor

def sample_random_attribute_index_and_value():
    """Sample a random value for an attribute."""
    all_attribute_names = list(ATTRIBUTES.keys())
    all_attribute_names.remove('exists')

    random_attribute_name = random.sample(all_attribute_names, 1)
    random_attribute_index = ATTRIBUTES[random_attribute_name].index
    random_attribute_min = ATTRIBUTES[random_attribute_name].min
    random_attribute_max = ATTRIBUTES[random_attribute_name].max
    random_attribute_value = random.randint(random_attribute_min, random_attribute_max)
    return random_attribute_index, random_attribute_value

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
        Tuple of (attribute_index, new_value) that was changed
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
