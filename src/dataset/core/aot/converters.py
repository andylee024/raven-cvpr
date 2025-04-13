import torch

import dataset.utils.bbox_utils as bbox_utils

from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.aot.attributes import ATTRIBUTES
from dataset.core.aot.entity_facade import EntityFacade
from dataset.legacy.AoT import Entity

def create_entity_facade(position_idx, name=None):
    """Create an EntityFacade at the specified position in the grid."""
    # Get bbox for position
    bbox = bbox_utils.position_index_to_bbox(position_idx)
    
    # Use position index as name if not provided
    if name is None:
        name = str(position_idx)
    
    # Create minimal entity constraint
    entity_constraint = {
        "Type": [ATTRIBUTES['type'].min_val, ATTRIBUTES['type'].max_val],
        "Size": [ATTRIBUTES['size'].min_val, ATTRIBUTES['size'].max_val],
        "Color": [ATTRIBUTES['color'].min_val, ATTRIBUTES['color'].max_val],
        "Angle": [ATTRIBUTES['angle'].min_val, ATTRIBUTES['angle'].max_val]
    }
    
    # Create raw entity
    entity = Entity(
        name=str(name),
        bbox=bbox,
        entity_constraint=entity_constraint
    )
    
    return EntityFacade.wrap(entity)


def aot_to_tensor(aot_facade):
    """Convert AoTFacade to PyTorch tensor representation (3,3,5).
    
    Uses ATTRIBUTES dictionary to ensure correct attribute indices and validation.
    
    Args:
        aot_facade: AoTFacade object containing entities
        
    Returns:
        PyTorch tensor with shape (3, 3, 5) containing entity attributes
    """
    # Initialize tensor with zeros - shape (3, 3, 5)
    tensor = torch.zeros((3, 3, 5), dtype=torch.int)
    
    # Get all entities from the panel
    entities = aot_facade.get_entities()
    
    # Populate tensor with entity data
    for entity in entities:
        # Get entity position in the grid
        tensor_coordinate = entity.get_tensor_coordinate()
        row, col = tensor_coordinate

        # Set exists flag to 1 using the 'exists' attribute
        exists_idx = ATTRIBUTES['exists'].index
        tensor[row, col, exists_idx] = 1
            
        # Set attribute values using attribute indices from ATTRIBUTES
        # This ensures correct positioning even if attribute order changes
        type_idx = ATTRIBUTES['type'].index
        size_idx = ATTRIBUTES['size'].index
        angle_idx = ATTRIBUTES['angle'].index
        color_idx = ATTRIBUTES['color'].index
        
        # Get values from entity and validate them against attribute constraints
        type_value = entity.get_type()
        size_value = entity.get_size()
        angle_value = entity.get_angle()
        color_value = entity.get_color()
        
        # Validate and set values (optional validation step)
        if type_value < ATTRIBUTES['type'].min_val or type_value > ATTRIBUTES['type'].max_val:
            raise ValueError(f"Entity type value {type_value} is outside valid range "
                           f"[{ATTRIBUTES['type'].min_val}, {ATTRIBUTES['type'].max_val}]")
            
        if size_value < ATTRIBUTES['size'].min_val or size_value > ATTRIBUTES['size'].max_val:
            raise ValueError(f"Entity size value {size_value} is outside valid range "
                           f"[{ATTRIBUTES['size'].min_val}, {ATTRIBUTES['size'].max_val}]")
            
        if angle_value < ATTRIBUTES['angle'].min_val or angle_value > ATTRIBUTES['angle'].max_val:
            raise ValueError(f"Entity angle value {angle_value} is outside valid range "
                           f"[{ATTRIBUTES['angle'].min_val}, {ATTRIBUTES['angle'].max_val}]")
            
        if color_value < ATTRIBUTES['color'].min_val or color_value > ATTRIBUTES['color'].max_val:
            raise ValueError(f"Entity color value {color_value} is outside valid range "
                           f"[{ATTRIBUTES['color'].min_val}, {ATTRIBUTES['color'].max_val}]")
        
        # Set values at the correct indices
        tensor[row, col, type_idx] = type_value
        tensor[row, col, size_idx] = size_value
        tensor[row, col, angle_idx] = angle_value
        tensor[row, col, color_idx] = color_value
    
    return tensor

def tensor_to_entity_facade(tensor_values, position_idx):
    """
    Convert tensor values to an EntityFacade object at a specified position.
    
    Args:
        tensor_values: Tensor values [exists, type, size, angle, color]
        position_idx: Position index (0-8) for the entity
        
    Returns:
        EntityFacade object configured with specified attributes
    """
    # Get bbox for this position
    bbox = bbox_utils.position_index_to_bbox(position_idx)
    
    # Create entity facade
    entity_facade = create_entity_facade(position_idx, name=str(position_idx))
    
    # Set attributes
    entity_facade.set_type(int(tensor_values[1]))
    entity_facade.set_size(int(tensor_values[2]))
    entity_facade.set_angle(int(tensor_values[3]))
    entity_facade.set_color(int(tensor_values[4]))
    
    return entity_facade


def tensor_to_aot(tensor):
    """Convert tensor to AoT"""
    # Import here to avoid circular import
    
    aot = AoTFacade()
    aot.clear_entities()
    
    # Add entities from tensor
    for row in range(3):
        for col in range(3):
            position_idx = row * 3 + col
            
            exists_idx = ATTRIBUTES['exists'].index
            if tensor[row, col, exists_idx].item() == 1:  # exists
                type_idx = ATTRIBUTES['type'].index
                size_idx = ATTRIBUTES['size'].index
                angle_idx = ATTRIBUTES['angle'].index
                color_idx = ATTRIBUTES['color'].index
                
                type_val = tensor[row, col, type_idx].item()
                size_val = tensor[row, col, size_idx].item()
                angle_val = tensor[row, col, angle_idx].item()
                color_val = tensor[row, col, color_idx].item()
                
                entity = create_entity_facade(position_idx)
                entity.set_type(type_val)
                entity.set_size(size_val)
                entity.set_angle(angle_val)
                entity.set_color(color_val)
                
                aot.add_entity(entity)
    
    return aot
