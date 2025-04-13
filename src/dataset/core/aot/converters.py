import torch
from dataset.core.aot.aot_facade import AoTFacade
from dataset.legacy.AoT import Entity
import dataset.utils.bbox_utils as bbox_utils
from dataset.core.aot.entity_facade import EntityFacade
from dataset.utils.panel_utils import generate_sample_panel

def create_entity_facade(bbox, name="0"):
    """
    Create an EntityFacade with the given bbox and entity constraint.
    
    Args:
        bbox: Bbox coordinates for the entity
        name: Name for the entity (default: "0")
    
    Returns:
        EntityFacade object
    """
    # Get entity constraint from a template
    template = generate_sample_panel()
    entity_constraint = template._get_layout().entity_constraint
    
    # Create raw entity
    entity = Entity(
        name=str(name),
        bbox=bbox,
        entity_constraint=entity_constraint
    )
    
    # Wrap in EntityFacade
    return EntityFacade.wrap(entity)


def aot_to_tensor(aot_facade):
    """Convert AoTFacade to PyTorch tensor representation (3,3,5)."""
    # Initialize tensor with zeros - shape (3, 3, 5)
    # [exists, type, size, angle, color]
    tensor = torch.zeros((3, 3, 5), dtype=torch.int)
    
    # Get all entities from the panel
    entities = aot_facade.get_entities()
    
    # Populate tensor with entity data
    for entity in entities:

        # get index of entity
        tensor_coordinate = entity.get_tensor_coordinate()
        row, col = tensor_coordinate

        # Set exists flag to 1
        tensor[row, col, 0] = 1
            
        # Set attribute values
        tensor[row, col, 1] = entity.get_type()    # Type
        tensor[row, col, 2] = entity.get_size()    # Size
        tensor[row, col, 3] = entity.get_angle()   # Angle
        tensor[row, col, 4] = entity.get_color()   # Color
    
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
    entity_facade = create_entity_facade(bbox, name=str(position_idx))
    
    # Set attributes
    entity_facade.set_type(int(tensor_values[1]))
    entity_facade.set_size(int(tensor_values[2]))
    entity_facade.set_angle(int(tensor_values[3]))
    entity_facade.set_color(int(tensor_values[4]))
    
    return entity_facade

def tensor_to_aot(tensor):
    """
    Convert tensor representation to AoTFacade.
    
    Args:
        tensor: Tensor with shape (3, 3, 5) containing:
               [exists, type, size, angle, color]
        template_panel: Optional template panel to clone
        
    Returns:
        AoTFacade panel with entities from tensor
    """
    aot_panel = generate_sample_panel()
    aot_panel.clear_entities()

    for row in range(3):
        for col in range(3):
            if tensor[row, col, 0].item() == 1:
                entity_facade = tensor_to_entity_facade(
                    tensor_values=tensor[row, col],
                    position_idx=bbox_utils.tensor_coordinate_to_position_index(row, col)
                )
                aot_panel.add_entity(entity_facade)

    return aot_panel
