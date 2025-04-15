import torch
import random
from dataset.core.aot.attributes import ATTRIBUTES, CONSTANTS


def sample_entity_tensor(shape_type=None, size=None, angle=None, color=None):
    """Generate attribute values for an entity, sampling random values for unspecified attributes."""
    
    # Create tensor for [exists, type, size, angle, color]
    entity_tensor = torch.zeros(5, dtype=torch.int)
    
    # Always set exists to 1
    entity_tensor[ATTRIBUTES['exists'].index] = 1
    
    # Define attributes and their provided values
    attribute_values = {
        'type': shape_type,
        'size': size,
        'angle': angle,
        'color': color
    }
    
    # Set each attribute value
    for attr_name, value in attribute_values.items():
        attr = ATTRIBUTES[attr_name]
        index = attr.index
        
        if value is not None:
            entity_tensor[index] = value
        else:
            entity_tensor[index] = random.randint(attr.min_val, attr.max_val)
    
    return entity_tensor